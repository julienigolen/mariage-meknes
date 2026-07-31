from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.gate import code_matches, has_gate, make_gate_cookie, set_household_cookie
from app.i18n.context import lang_context
from app.models import HouseholdMember
from app.phone import phone_candidates
from app.templates_engine import templates

router = APIRouter()


@router.get("/entree")
def gate_page(request: Request):
    if has_gate(request):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request, "gate.html", {"error": False, **lang_context(request)})


@router.post("/entree")
def gate_submit(request: Request, code: str = Form(""), db: Session = Depends(get_db)):
    household_id = None
    member_id = None

    if not code_matches(code):
        # Repli : le champ accepte aussi un numéro de téléphone connu (feedback
        # Patron 2026-07-29) — un invité peut entrer avec son propre numéro,
        # sans avoir besoin de retenir le code commun.
        member = db.execute(
            select(HouseholdMember).where(HouseholdMember.phone.in_(phone_candidates(code)))
        ).scalar_one_or_none()
        if member is None:
            return templates.TemplateResponse(
                request, "gate.html", {"error": True, **lang_context(request)}, status_code=401
            )
        household_id = member.household_id
        # On retient AUSSI quelle personne du foyer s'est identifiée : c'est elle que
        # /rsvp doit saluer, pas le premier membre importé (bug Patron 2026-07-31).
        member_id = member.id

    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie(
        settings.gate_cookie_name,
        make_gate_cookie(),
        max_age=settings.gate_max_age,
        httponly=True,
        samesite="lax",
        secure=settings.env == "prod",
    )
    if household_id is not None:
        set_household_cookie(resp, household_id, member_id)
    return resp
