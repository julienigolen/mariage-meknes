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


def make_household_cookie(household_id: int, member_id: int | None = None) -> str:
    """Charge utile « <foyer> » ou « <foyer>:<membre> ».

    Le membre a été ajouté le 2026-07-31 (bug Patron) : la porte et le lookup RSVP
    identifient la BONNE personne par son téléphone, mais seul l'id du foyer était
    conservé. `/rsvp` retombait alors sur `household.members[0]` et accueillait le
    2ᵉ contact d'un foyer sous le nom du 1ᵉʳ.
    """
    payload = f"{household_id}:{member_id}" if member_id is not None else str(household_id)
    return _signer.sign(payload.encode()).decode()


def known_household(request: Request) -> tuple[int | None, int | None]:
    """(foyer, membre) reconnus via le cookie — (None, None) si absent/invalide/expiré.

    Le membre vaut None pour les cookies émis avant le 2026-07-31 (charge utile sans
    « : ») : ils restent valides, l'appelant retombe simplement sur son comportement
    d'avant. Aucun invité n'est déconnecté par ce changement de format.
    """
    raw = request.cookies.get(settings.household_cookie_name)
    if not raw:
        return None, None
    try:
        value = _signer.unsign(raw, max_age=settings.gate_max_age).decode()
    except (BadSignature, SignatureExpired):
        return None, None
    hh, _, mem = value.partition(":")
    try:
        return int(hh), (int(mem) if mem else None)
    except ValueError:
        return None, None


def known_household_id(request: Request) -> int | None:
    """Foyer seul — pour les appelants qui n'ont pas besoin du membre (home)."""
    return known_household(request)[0]


def set_household_cookie(response, household_id: int, member_id: int | None = None) -> None:
    response.set_cookie(
        settings.household_cookie_name,
        make_household_cookie(household_id, member_id),
        max_age=settings.gate_max_age,
        httponly=True,
        samesite="lax",
        secure=settings.env == "prod",
    )
