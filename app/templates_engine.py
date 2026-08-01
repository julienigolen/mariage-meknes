import re
from pathlib import Path

from fastapi.templating import Jinja2Templates

from app.config import settings

_BASE = Path(__file__).parent
_STATIC = _BASE / "static"

templates = Jinja2Templates(directory=str(_BASE / "templates"))


def asset(path: str) -> str:
    """Renvoie une URL statique horodatée : /static/img/hero.webp?v=<mtime>.

    Sans ça, le navigateur d'un invité garde en cache l'ancienne version d'une image
    remplacée (constaté le 2026-07-27 : la façade rognée restait affichée après
    restauration du fichier). L'horodatage change à chaque écriture du fichier, donc
    l'URL change, donc le cache est contourné — et reste efficace tant que rien ne bouge.
    """
    rel = path.lstrip("/").removeprefix("static/")
    f = _STATIC / rel
    url = f"/static/{rel}"
    try:
        return f"{url}?v={int(f.stat().st_mtime)}"
    except OSError:
        # Fichier absent (ex. photo pas encore livrée) : on renvoie l'URL nue,
        # le `onerror` du template retire alors l'élément.
        return url


def ireplace(text: str | None, old: str, new: str) -> str:
    """Remplace `old` par `new` dans `text`, insensible à la casse -- les placeholders
    [lien du groupe]/[Prénom] (app/templates/partials/whatsapp_table.html) sont du texte
    libre retapé par le Patron, la casse exacte n'est pas garantie (constaté 2026-08-01 :
    "[Lien du groupe]" ne matchait pas "[lien du groupe]"). Remplacement par une fonction,
    pas une chaîne : `new` peut contenir des "\\" (URL, nom) que re.sub interpréterait
    sinon comme des groupes de capture."""
    if text is None:
        return ""
    return re.sub(re.escape(old), lambda _m: new, text, flags=re.IGNORECASE)


templates.env.globals["asset"] = asset
templates.env.globals["settings"] = settings
# wa.me n'accepte que des chiffres (pas de "+", espaces, tirets) -- app/routers/whatsapp.py.
templates.env.filters["digits_only"] = lambda s: re.sub(r"\D", "", s or "")
templates.env.filters["ireplace"] = ireplace
