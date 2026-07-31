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
from app.gate import gate_redirect, known_household, set_household_cookie
from app.i18n.context import lang_context
from app.models import Household, HouseholdMember, Rsvp
from app.phone import is_plausible_phone, normalize_phone, phone_candidates
from app.templates_engine import templates

router = APIRouter()


def _form_step_response(request: Request, ctx: dict, household: Household, member: HouseholdMember):
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
    set_household_cookie(resp, household.id, member.id)
    return resp


@router.get("/rsvp")
def rsvp_page(request: Request, db: Session = Depends(get_db)):
    if (r := gate_redirect(request)) is not None:
        return r
    ctx = lang_context(request)

    hh_id, mem_id = known_household(request)
    if hh_id is not None:
        household = db.get(Household, hh_id)
        if household is not None and household.members:
            # Le cookie retient la personne qui s'est identifiée (par son téléphone,
            # à la porte ou au lookup) : c'est elle qu'on salue. Repli sur le premier
            # membre du foyer seulement si le cookie est antérieur au 2026-07-31, ou
            # si ce membre a disparu de la base depuis (réimport de la liste).
            member = next((m for m in household.members if m.id == mem_id), None) or household.members[0]
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
            # Recharge le cookie au format complet : un invité entré avant le correctif
            # est raccroché à la bonne personne dès sa prochaine identification.
            set_household_cookie(resp, household.id, member.id)
            return resp

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
        # Numéro absent de la liste importée : s'il ressemble à un vrai numéro
        # FR/MA/US, on propose de créer le foyer plutôt que de bloquer avec une
        # erreur (Patron 2026-07-28) — sinon, erreur inchangée.
        if is_plausible_phone(phone):
            return templates.TemplateResponse(
                request,
                "rsvp.html",
                {"step": "new", "error": False, "phone": normalize_phone(phone), "lang_switch_path": "/rsvp", **ctx},
            )
        return templates.TemplateResponse(
            request, "rsvp.html", {"step": "phone", "error": True, "lang_switch_path": "/rsvp", **ctx}
        )

    return _form_step_response(request, ctx, member.household, member)


@router.post("/rsvp/join")
def rsvp_join(request: Request, phone: str = Form(""), nom_prenom: str = Form(""), db: Session = Depends(get_db)):
    """Création d'un foyer par un invité au numéro non répertorié mais plausible
    (Patron 2026-07-28) — étape intermédiaire après /rsvp/lookup, cf. step "new"."""
    if (r := gate_redirect(request)) is not None:
        return r
    ctx = lang_context(request)
    nom_prenom = nom_prenom.strip()

    if not is_plausible_phone(phone) or not nom_prenom:
        return templates.TemplateResponse(
            request, "rsvp.html", {"step": "phone", "error": True, "lang_switch_path": "/rsvp", **ctx}
        )

    # Recheck avec phone_candidates (pas juste le nettoyage brut) : couvre le cas
    # d'un double envoi du formulaire, ou d'un numéro entré sans indicatif qu'un
    # import ultérieur aurait entre-temps rattaché à un foyer existant.
    existing = db.execute(
        select(HouseholdMember).where(HouseholdMember.phone.in_(phone_candidates(phone)))
    ).scalar_one_or_none()
    if existing is not None:
        return _form_step_response(request, ctx, existing.household, existing)

    household = Household()
    member = HouseholdMember(
        household=household,
        nom_prenom=nom_prenom,
        phone=normalize_phone(phone),
        langue=ctx["lang"],
        statut="ajoute_rsvp",
    )
    db.add(household)
    db.add(member)
    db.commit()

    return _form_step_response(request, ctx, household, member)


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
    # Le formulaire ne transporte que household_id : on préserve le membre déjà reconnu
    # dans le cookie plutôt que de l'effacer à la soumission (sinon la personne perdrait
    # son identité juste après avoir répondu).
    set_household_cookie(resp, household.id, known_household(request)[1])
    return resp
