"""Sélecteur de langue — cf. charte_graphique.md §4.4, pattern repris d'OWP à l'identique."""
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.config import settings
from app.i18n.context import LANG_COOKIE
from app.i18n.translations import DEFAULT_LANG, SUPPORTED_LANGS

router = APIRouter()


@router.get("/set-lang")
def set_lang(lang: str = DEFAULT_LANG, next: str = "/"):
    """GET /set-lang?lang=<fr|en>&next=<url> — pose le cookie lang et redirige.

    Langue inconnue -> repli DEFAULT_LANG (pas d'erreur). `next` doit commencer par
    "/" (protection open-redirect) sinon repli sur "/".
    """
    safe_lang = lang if lang in SUPPORTED_LANGS else DEFAULT_LANG
    safe_next = next if next.startswith("/") else "/"

    response = RedirectResponse(url=safe_next, status_code=303)
    response.set_cookie(
        key=LANG_COOKIE,
        value=safe_lang,
        max_age=settings.gate_max_age,
        httponly=False,  # accessible en JS si besoin, comme sur OWP
        samesite="lax",
        path="/",
    )
    return response
