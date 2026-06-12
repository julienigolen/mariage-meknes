"""Porte d'entrée : code commun → cookie signé 90 jours."""
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
