"""Auth admin — version light (Patron 2026-07-28) : « on récupère la mécanique d'OWP ou on
fait plus léger ? » -> plus léger. OWP porte des sessions serveur, verrouillage de compte,
tokens de vérification/reset par email — dimensionné pour un produit multi-utilisateurs avec
inscription publique. Ici il y a deux utilisateurs connus (Kenza & Julien), pas d'inscription,
pas d'infra email. On réutilise le pattern déjà en place pour la porte/le foyer (gate.py) :
cookie signé itsdangerous, pas de table de sessions. Le mot de passe reste hashé (bcrypt) —
seule concession non négociable même en version light (§ frontière système, jamais de clair).

Pas de « mot de passe oublié » par email : en cas de blocage, reset via scripts/create_admin.py
directement en base. Pas de rôles/permissions, inutile à deux.
"""
import time

import bcrypt
from fastapi import Request
from fastapi.responses import RedirectResponse
from itsdangerous import BadSignature, SignatureExpired, TimestampSigner
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import AdminUser

_signer = TimestampSigner(settings.secret_key, salt="admin")

ADMIN_COOKIE_NAME = "kj_admin"
ADMIN_COOKIE_MAX_AGE = 7 * 24 * 3600  # 7 jours — plus court que la porte (§ accès sensible, données invités)

# Throttle en mémoire, pas en base (mono-process, deux comptes) : après N échecs pour un
# email donné dans la fenêtre, on bloque temporairement. Repart à zéro au redémarrage du
# process — acceptable pour ce volume d'usage.
_MAX_ATTEMPTS = 5
_WINDOW_SECONDS = 15 * 60
_failed_attempts: dict[str, list[float]] = {}


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), password_hash.encode("utf-8"))


# Hash bcrypt valide d'un mot de passe bidon, calculé une fois au chargement — sert de
# comparaison dans authenticate() quand l'email n'existe pas (cf. plus bas : timing).
_DUMMY_HASH = hash_password("timing-safety-guard-not-a-real-password")


def is_locked_out(email: str) -> bool:
    now = time.monotonic()
    attempts = [t for t in _failed_attempts.get(email.lower(), []) if now - t < _WINDOW_SECONDS]
    _failed_attempts[email.lower()] = attempts
    return len(attempts) >= _MAX_ATTEMPTS


def record_failed_attempt(email: str) -> None:
    _failed_attempts.setdefault(email.lower(), []).append(time.monotonic())


def clear_failed_attempts(email: str) -> None:
    _failed_attempts.pop(email.lower(), None)


def make_admin_cookie(admin_id: int) -> str:
    return _signer.sign(str(admin_id).encode()).decode()


def current_admin_id(request: Request) -> int | None:
    raw = request.cookies.get(ADMIN_COOKIE_NAME)
    if not raw:
        return None
    try:
        value = _signer.unsign(raw, max_age=ADMIN_COOKIE_MAX_AGE)
        return int(value)
    except (BadSignature, SignatureExpired, ValueError):
        return None


def current_admin(request: Request, db: Session) -> AdminUser | None:
    admin_id = current_admin_id(request)
    if admin_id is None:
        return None
    return db.get(AdminUser, admin_id)


def admin_redirect(request: Request) -> RedirectResponse | None:
    """À utiliser au début de chaque route /admin/* protégée."""
    if current_admin_id(request) is not None:
        return None
    return RedirectResponse("/admin/login", status_code=303)


def set_admin_cookie(response, admin_id: int) -> None:
    response.set_cookie(
        ADMIN_COOKIE_NAME,
        make_admin_cookie(admin_id),
        max_age=ADMIN_COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=settings.env == "prod",
    )


def clear_admin_cookie(response) -> None:
    response.delete_cookie(ADMIN_COOKIE_NAME)


def authenticate(db: Session, email: str, password: str) -> AdminUser | None:
    if is_locked_out(email):
        return None
    user = db.execute(select(AdminUser).where(AdminUser.email == email.lower().strip())).scalar_one_or_none()
    # Comparaison bcrypt même si l'utilisateur n'existe pas (contre un hash factice) : évite
    # qu'un email invalide réponde plus vite qu'un mauvais mot de passe (timing).
    ok = verify_password(password, user.password_hash if user else _DUMMY_HASH)
    if user is None or not ok:
        record_failed_attempt(email)
        return None
    clear_failed_attempts(email)
    return user
