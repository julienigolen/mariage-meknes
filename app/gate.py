"""Porte d'entrée : code commun (ou numéro de téléphone connu) → cookie signé 90 jours.

Second cookie (household) : reconnaît le foyer identifié, pour que la home et le
RSVP sachent qu'un invité est déjà connu sans lui redemander son numéro à chaque
visite (feedback Patron 2026-07-29). Posé à l'entrée par téléphone (gate.py) et
au RSVP (lookup/submit) — pas seulement à la porte.
"""
from fastapi import Request
from fastapi.responses import RedirectResponse
from itsdangerous import BadSignature, SignatureExpired, TimestampSigner

from app.config import settings

_signer = TimestampSigner(settings.secret_key)


def make_gate_cookie() -> str:
    return _signer.sign(b"ok").decode()


def has_gate(request: Request) -> bool:
    raw = request.cookies.get(settings.gate_cookie_name)
    if not raw:
        return False
    try:
        _signer.unsign(raw, max_age=settings.gate_max_age)
        return True
    except (BadSignature, SignatureExpired):
        return False


def code_matches(submitted: str) -> bool:
    norm = lambda s: "".join(s.split()).lower()
    return norm(submitted) == norm(settings.access_code)


def gate_redirect(request: Request) -> RedirectResponse | None:
    """À utiliser au début de chaque route protégée."""
    if has_gate(request):
        return None
    return RedirectResponse("/entree", status_code=303)


def make_household_cookie(household_id: int) -> str:
    return _signer.sign(str(household_id).encode()).decode()


def known_household_id(request: Request) -> int | None:
    """Foyer reconnu via le cookie household — None si absent, invalide ou expiré."""
    raw = request.cookies.get(settings.household_cookie_name)
    if not raw:
        return None
    try:
        value = _signer.unsign(raw, max_age=settings.gate_max_age)
        return int(value)
    except (BadSignature, SignatureExpired, ValueError):
        return None


def set_household_cookie(response, household_id: int) -> None:
    response.set_cookie(
        settings.household_cookie_name,
        make_household_cookie(household_id),
        max_age=settings.gate_max_age,
        httponly=True,
        samesite="lax",
        secure=settings.env == "prod",
    )
