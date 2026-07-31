"""Back-office (charte §5.9) — Kenza & Julien uniquement. Auth light (app/admin_auth.py,
décision Patron 2026-07-28 : pas la mécanique d'OWP, cookie signé sans table de sessions).

Écrans : connexion, tableau invités/RSVP éditable en ligne (§5.9), import Excel depuis le
site (en plus du script CLI existant scripts/import_guests.py, qui réutilise la même
logique — app/services/import_guests.py).
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from io import BytesIO

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse, StreamingResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.admin_auth import (
    admin_redirect,
    authenticate,
    clear_admin_cookie,
    current_admin,
    set_admin_cookie,
)
from app.database import get_db
from app.models import Household, HouseholdMember, Rsvp
from app.phone import normalize_phone
from app.services.import_guests import existing_phones, export_workbook, parse_workbook, write_import
from app.templates_engine import templates

router = APIRouter(prefix="/admin")

# Allowlist des champs éditables en ligne (§5.9) — jamais de setattr sur un nom de champ
# venu tel quel de l'URL sans passer par une de ces trois listes.
_MEMBER_TEXT_FIELDS = {"nom_prenom", "phone"}
_MEMBER_INT_FIELDS = {"effectif_theorique"}
_HOUSEHOLD_TEXT_FIELDS = {"import_famille_label"}
_RSVP_TEXT_FIELDS = {"allergies_texte"}
_RSVP_INT_FIELDS = {"nb_adultes", "nb_enfants"}
_RSVP_BOOL_FIELDS = {"presence", "allergies_bool", "besoin_hotel"}


@router.get("/")
def admin_root(request: Request):
    if (r := admin_redirect(request)) is not None:
        return r
    return RedirectResponse("/admin/invites", status_code=303)


@router.get("/login")
def admin_login_page(request: Request):
    if admin_redirect(request) is None:
        return RedirectResponse("/admin/invites", status_code=303)
    return templates.TemplateResponse(request, "admin_login.html", {"error": None, "email": None})


@router.post("/login")
def admin_login_submit(
    request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user = authenticate(db, email, password)
    if user is None:
        return templates.TemplateResponse(
            request,
            "admin_login.html",
            {"error": "Email ou mot de passe incorrect (ou trop de tentatives — réessayez plus tard).", "email": email},
        )
    resp = RedirectResponse("/admin/invites", status_code=303)
    set_admin_cookie(resp, user.id)
    return resp


@router.post("/logout")
def admin_logout():
    resp = RedirectResponse("/admin/login", status_code=303)
    clear_admin_cookie(resp)
    return resp


def _all_households(db: Session) -> list[Household]:
    """Table admin simplifiée (Patron 2026-07-29) : une ligne par foyer, pas par
    personne. Invité principal = members[0], invité secondaire = members[1] s'il
    existe — on ne gère que 2 personnes nommées par foyer (décision explicite ;
    les enfants/accompagnants au-delà restent comptés via nb_adultes/nb_enfants du
    RSVP, jamais nommés individuellement)."""
    return list(
        db.execute(
            select(Household).options(selectinload(Household.members), selectinload(Household.rsvp)).order_by(Household.id)
        ).scalars()
    )


def _get_or_create_rsvp(db: Session, household: Household) -> Rsvp:
    if household.rsvp is None:
        household.rsvp = Rsvp(household_id=household.id, presence=False)
        db.add(household.rsvp)
        db.flush()
    return household.rsvp


@dataclass
class Kpis:
    """4 indicateurs (Patron 2026-07-29, plusieurs allers-retours de définition —
    voir docs/projet_mariage-meknes/proposition_produit.md pour l'historique).

    Statut d'un foyer — Invité / Accepté / Refusé — purement dérivé de la réponse RSVP
    (pas de l'origine liste_origine/ajoute_rsvp, qui reste un simple repère visuel dans
    la table, cf. admin_invites_tbody.html) :
    - Invité (pas de RSVP soumis) -> compte sur l'effectif THÉORIQUE du foyer, porté par
      l'invité principal (`members[0].effectif_theorique`, défaut 1 — table à une ligne
      par foyer depuis le 2026-07-29, l'effectif secondaire n'est pas sommé séparément),
      dans « invites » et « attendues ».
    - Accepté (RSVP « oui ») -> compte sur l'effectif RÉEL du RSVP (adultes+enfants, qui
      peut différer du théorique), dans « invites » et « positives ». Bascule aussi une
      chambre si besoin_hotel est coché.
    - Refusé (RSVP « non ») -> **exclu de « invites »** (Patron 2026-07-29 : « on ne
      comptera pas les personnes qui ont refusé »). Pas de carte dédiée pour ce cas.
    """

    invites: int = 0
    positives_pers: int = 0
    positives_foyers: int = 0
    attendues_pers: int = 0
    attendues_foyers: int = 0
    chambres_1_2: int = 0
    chambres_3_4: int = 0


def _compute_kpis(db: Session) -> Kpis:
    households = list(
        db.execute(select(Household).options(selectinload(Household.members), selectinload(Household.rsvp))).scalars()
    )
    k = Kpis()
    for hh in households:
        theorique = hh.members[0].effectif_theorique if hh.members else 0
        r = hh.rsvp
        if r is None:
            k.invites += theorique
            k.attendues_pers += theorique
            k.attendues_foyers += 1
        elif r.presence:
            headcount = r.nb_adultes + r.nb_enfants
            k.invites += headcount
            k.positives_pers += headcount
            k.positives_foyers += 1
            if r.besoin_hotel:
                if headcount <= 2:
                    k.chambres_1_2 += 1
                else:
                    k.chambres_3_4 += 1
        # else : Refusé -> exclu de "invites", rien à ajouter.
    return k


def _tbody_response(request: Request, db: Session):
    return templates.TemplateResponse(
        request, "partials/admin_edit_response.html", {"households": _all_households(db), "kpis": _compute_kpis(db)}
    )


@router.post("/import")
def admin_import(request: Request, fichier: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload direct depuis le site (Patron 2026-07-28), en plus du script CLI existant —
    même logique de parsing/écriture (app/services/import_guests.py). Import immédiat,
    pas d'étape de prévisualisation séparée : le contrôle visuel du fichier reste manuel
    et en amont (décision Patron du 2026-07-28, §5 point 21 de la proposition produit)."""
    if (r := admin_redirect(request)) is not None:
        return r
    content = fichier.file.read()
    result = parse_workbook(BytesIO(content), existing_phones(db))
    if result.header_error is None:
        write_import(db, result)
    return templates.TemplateResponse(
        request, "admin_import_result.html", {"result": result, "admin": current_admin(request, db)}
    )


@router.get("/export")
def admin_export(request: Request, db: Session = Depends(get_db)):
    if (r := admin_redirect(request)) is not None:
        return r
    buf = export_workbook(_all_households(db))
    filename = f"invites_{datetime.now(timezone.utc):%Y-%m-%d}.xlsx"
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/invites")
def admin_invites(request: Request, db: Session = Depends(get_db)):
    if (r := admin_redirect(request)) is not None:
        return r
    return templates.TemplateResponse(
        request,
        "admin_invites.html",
        {"households": _all_households(db), "kpis": _compute_kpis(db), "admin": current_admin(request, db)},
    )


@router.post("/invites/member/{member_id}/field/{field}")
def admin_edit_member(
    member_id: int, field: str, request: Request, value: str = Form(""), db: Session = Depends(get_db)
):
    """Édition en ligne (§5.9), sauvegarde en sortie de zone (blur) — un champ à la fois,
    field restreint aux allowlists _MEMBER_TEXT_FIELDS/_MEMBER_INT_FIELDS, jamais un
    setattr libre."""
    if (r := admin_redirect(request)) is not None:
        return r
    if field in _MEMBER_TEXT_FIELDS:
        member = db.get(HouseholdMember, member_id)
        value = value.strip()
        if member is not None and value:  # jamais un identifiant vidé silencieusement
            if field == "phone":
                value = normalize_phone(value)
            setattr(member, field, value)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()  # ex. téléphone dupliqué — édition ignorée, la ligne revient à l'état réel
    elif field in _MEMBER_INT_FIELDS:
        member = db.get(HouseholdMember, member_id)
        if member is not None:
            try:
                setattr(member, field, max(1, int(value)))
                db.commit()
            except ValueError:
                pass
    return _tbody_response(request, db)


@router.post("/invites/household/{household_id}/secondary")
def admin_add_secondary(
    household_id: int,
    request: Request,
    nom_prenom: str = Form(""),
    phone: str = Form(""),
    db: Session = Depends(get_db),
):
    """Crée l'invité secondaire d'un foyer qui n'en a pas encore (table à une ligne par
    foyer, deux personnes nommées maximum — Patron 2026-07-29). Les deux champs (nom ET
    téléphone) arrivent ensemble via hx-include (cf. admin_invites_tbody.html), quel que
    soit celui qui a déclenché la sauvegarde : on ne crée jamais un invité à moitié
    renseigné. No-op si le foyer a déjà 2 membres ou si l'un des deux champs est vide."""
    if (r := admin_redirect(request)) is not None:
        return r
    household = db.get(Household, household_id)
    nom_prenom = nom_prenom.strip()
    phone = phone.strip()
    if household is not None and len(household.members) < 2 and nom_prenom and phone:
        db.add(HouseholdMember(household_id=household.id, nom_prenom=nom_prenom, phone=normalize_phone(phone)))
        try:
            db.commit()
        except IntegrityError:
            db.rollback()  # téléphone déjà connu ailleurs — création ignorée
    return _tbody_response(request, db)


@router.post("/invites/household/{household_id}/field/{field}")
def admin_edit_household(
    household_id: int, field: str, request: Request, value: str = Form(""), db: Session = Depends(get_db)
):
    if (r := admin_redirect(request)) is not None:
        return r
    if field in _HOUSEHOLD_TEXT_FIELDS:
        household = db.get(Household, household_id)
        if household is not None:
            setattr(household, field, value.strip() or None)
            db.commit()
    return _tbody_response(request, db)


@router.post("/invites/rsvp/{household_id}/field/{field}")
def admin_edit_rsvp(
    household_id: int, field: str, request: Request, value: str = Form(""), db: Session = Depends(get_db)
):
    if (r := admin_redirect(request)) is not None:
        return r
    household = db.get(Household, household_id)
    if household is not None:
        rsvp = _get_or_create_rsvp(db, household)
        if field in _RSVP_BOOL_FIELDS:
            setattr(rsvp, field, value == "oui")
            db.commit()
        elif field in _RSVP_INT_FIELDS:
            try:
                setattr(rsvp, field, max(0, int(value)))
                db.commit()
            except ValueError:
                pass
        elif field in _RSVP_TEXT_FIELDS:
            setattr(rsvp, field, value.strip() or None)
            db.commit()
    return _tbody_response(request, db)


@router.delete("/invites/household/{household_id}")
def admin_delete_household(household_id: int, request: Request, db: Session = Depends(get_db)):
    """Suppression du foyer entier (Patron 2026-08-01), confirmée côté client par
    hx-confirm (cf. admin_invites_tbody.html) — cascade ORM sur ses membres et son
    RSVP (Household.members/.rsvp, app/models.py)."""
    if (r := admin_redirect(request)) is not None:
        return r
    household = db.get(Household, household_id)
    if household is not None:
        db.delete(household)
        db.commit()
    return _tbody_response(request, db)
