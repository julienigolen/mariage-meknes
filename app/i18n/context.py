"""Résolution de la langue active à partir du cookie — cf. charte_graphique.md §4.4.

dir se déduit de lang, jamais un état à part. « ar » n'est pas encore dans
SUPPORTED_LANGS (translations.py) : dir restera "ltr" tant qu'il n'y est pas.
"""
from fastapi import Request

from app.i18n.translations import DEFAULT_LANG, SUPPORTED_LANGS, get_texts

LANG_COOKIE = "lang"


def resolve_lang(request: Request) -> str:
    cookie_lang = request.cookies.get(LANG_COOKIE)
    return cookie_lang if cookie_lang in SUPPORTED_LANGS else DEFAULT_LANG


def lang_context(request: Request) -> dict:
    lang = resolve_lang(request)
    return {
        "lang": lang,
        "dir": "rtl" if lang == "ar" else "ltr",
        "texts": get_texts(lang),
    }
