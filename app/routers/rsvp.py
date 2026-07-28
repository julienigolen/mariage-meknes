"""RSVP — identification par téléphone, formulaire par foyer (proposition_produit.md §2 point 4).

MVP (2026-07-28) : pas de goodies (message personnalisé, notice « famille a déjà
répondu »), pas d'email de confirmation. Le formulaire reste toujours modifiable
(§5.11) : re-soumettre un numéro déjà répondu pré-remplit la réponse existante,
sans bandeau dédié pour l'instant.

Reconnaissance du foyer (2026-07-29, feedback Patron) : le cookie household posé
ici (lookup + submit) et à la porte (gate.py, entrée par téléphone) permet à un
invité déjà identifié de sauter directement à son formulaire pré-rempli sans
retaper son numéro — et à la home de savoir qu'il a déjà répondu.
"""
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.gate import gate_redirect, known_household_id, set_household_cookie
from app.i18n.context import lang_context
from app.models import Household, HouseholdMember, Rsvp
from app.phone import phone_candidates
from app.templates_engine import templates

router = APIRouter()


@router.get("/rsvp")
def rsvp_page(request: Request, db: Session = Depends(get_db)):
    if (r := gate_redirect(request)) is not None:
        return r
    ctx = lang_context(request)

    hh_id = known_household_id(request)
    if hh_id is not None:
        household = db.get(Household, hh_id)
        if household is not None and household.members:
            # Le cookie ne retient que le foyer, pas quel membre précis s'est
            # identifié la dernière fois — on salue le premier membre importé,
            # imprécision acceptée pour ce MVP sur un foyer à plusieurs personnes.
            member = household.members[0]
            return templates.TemplateResponse(
                request,
                "rsvp.html",
                {
                    "step": "form",
                    "error": False,
                    "household_id": household.id,
                    "nom_prenom": member.nom_prenom,
                    "rsvp": household.rsvp,
                    "lang_switch_path": "/rsvp",
                    **ctx,
                },
            )

    return templates.TemplateResponse(request, "rsvp.html", {"step": "phone", "error": False, **ctx})


@router.post("/rsvp/lookup")
def rsvp_lookup(request: Request, phone: str = Form(""), db: Session = Depends(get_db)):
    if (r := gate_redirect(request)) is not None:
        return r
    ctx = lang_context(request)
    member = db.execute(
        select(HouseholdMember).where(HouseholdMember.phone.in_(phone_candidates(phone)))
    ).scalar_one_or_none()

    if member is None:
        return templates.TemplateResponse(
            request, "rsvp.html", {"step": "phone", "error": True, "lang_switch_path": "/rsvp", **ctx}
        )

    household = member.household
    resp = templates.TemplateResponse(
        request,
        "rsvp.html",
        {
            "step": "form",
            "error": False,
            "household_id": household.id,
            "nom_prenom": member.nom_prenom,
            "rsvp": household.rsvp,
            "lang_switch_path": "/rsvp",
            **ctx,
        },
    )
    set_household_cookie(resp, household.id)
    return resp


@router.post("/rsvp/submit")
def rsvp_submit(
    request: Request,
    household_id: int = Form(...),
    presence: str = Form("non"),
    nb_adultes: int = Form(0),
    nb_enfants: int = Form(0),
    allergies_bool: str = Form("non"),
    allergies_texte: str = Form(""),
    besoin_hotel: str = Form("non"),
    db: Session = Depends(get_db),
):
    if (r := gate_redirect(request)) is not None:
        return r

    household = db.get(Household, household_id)
    if household is None:
        return RedirectResponse("/rsvp", status_code=303)

    presence_b = presence == "oui"
    allergies_b = allergies_bool == "oui"
    hotel_b = besoin_hotel == "oui"
    nb_adultes = nb_adultes if presence_b else 0
    nb_enfants = nb_enfants if presence_b else 0
    allergies_texte = allergies_texte if allergies_b else None

    if household.rsvp is None:
        household.rsvp = Rsvp(
            household_id=household.id,
            presence=presence_b,
            nb_adultes=nb_adultes,
            nb_enfants=nb_enfants,
            allergies_bool=allergies_b,
            allergies_texte=allergies_texte,
            besoin_hotel=hotel_b,
        )
    else:
        r = household.rsvp
        r.presence = presence_b
        r.nb_adultes = nb_adultes
        r.nb_enfants = nb_enfants
        r.allergies_bool = allergies_b
        r.allergies_texte = allergies_texte
        r.besoin_hotel = hotel_b
    db.commit()

    resp = templates.TemplateResponse(
        request,
        "rsvp.html",
        {"step": "success", "error": False, "lang_switch_path": "/rsvp", **lang_context(request)},
    )
    set_household_cookie(resp, household.id)
    return resp
