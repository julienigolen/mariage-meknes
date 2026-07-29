"""Site mariage Kenza & Julien — Meknès, 23 octobre 2026.

S0 : porte à code commun + layout tokens (direction A · Bleu zellige) + save-the-date.
Stack : FastAPI + Jinja2 + Tailwind CDN + HTMX (patterns repris d'OWP).
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import admin, gate, lang, rsvp, site

app = FastAPI(title="Mariage Kenza & Julien — Meknès", docs_url=None, redoc_url=None, openapi_url=None)

app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
app.include_router(gate.router)
app.include_router(lang.router)
app.include_router(rsvp.router)
app.include_router(site.router)
app.include_router(admin.router)

if settings.env == "dev":
    # En dev local (sqlite) : schéma direct. En prod Render : alembic upgrade head au démarrage.
    from app.database import Base, engine
    Base.metadata.create_all(engine)


@app.get("/healthz")
def healthz():
    return {"ok": True}
