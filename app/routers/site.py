from datetime import date

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.gate import gate_redirect, known_household_id
from app.i18n.context import lang_context
from app.models import Household
from app.templates_engine import templates

router = APIRouter()

WEDDING_DATE = date(2026, 10, 23)


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    if (r := gate_redirect(request)) is not None:
        return r
    days_left = (WEDDING_DATE - date.today()).days

    # Foyer déjà répondu (feedback Patron 2026-07-29) : si le cookie household
    # identifie un foyer et qu'il a déjà une réponse, on l'affiche sur la home
    # au lieu du CTA générique "Confirmer ma présence" (charte §2.2 : jamais un
    # aplat vert plein pour un état déjà acquis — géré côté template).
    my_rsvp = None
    hh_id = known_household_id(request)
    if hh_id is not None:
        household = db.get(Household, hh_id)
        if household is not None:
            my_rsvp = household.rsvp

    return templates.TemplateResponse(
        request, "home.html", {"days_left": days_left, "my_rsvp": my_rsvp, **lang_context(request)}
    )
