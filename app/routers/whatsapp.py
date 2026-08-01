"""Invitations WhatsApp (Patron 2026-08-01) -- deux écrans :

- Liste (une ligne par personne, principal OU secondaire -- cf. app/models.py::HouseholdMember,
  pas une ligne par foyer comme /admin/invites) : groupe rattaché (get-or-create par libellé,
  même logique que household.import_famille_label), lien d'invitation du groupe, date
  d'envoi (pas un booléen -- on veut savoir QUAND, cf. migration 649e01107e3e).
- Message personnalisé par groupe, avec navigation prev/next (5-10 groupes attendus,
  pas besoin d'une liste/recherche).

Même auth que /admin/invites (app/admin_auth.py).
"""
import re
from datetime import date as date_type

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.admin_auth import admin_redirect, current_admin
from app.database import get_db
from app.models import HouseholdMember, WhatsappGroup
from app.templates_engine import templates

router = APIRouter(prefix="/admin/whatsapp")

# Pré-rempli à la création d'un groupe (Patron 2026-08-01) -- point de départ à ajuster
# par groupe, jamais régénéré ni traduit ensuite (même principe que le message RSVP,
# proposition_produit.md §5.17). Deux placeholders littéraux, substitués uniquement au
# moment de générer le lien wa.me (cf. partials/whatsapp_table.html), jamais écrits en
# base : "[lien du groupe]" (le lien n'est en général pas encore connu au moment où le
# groupe est créé -- juste un libellé tapé sur l'écran liste) et "[Prénom]" (premier mot
# du champ Invité de CETTE personne, donc différent par contact même si le message est
# partagé par tout le groupe).
_DEFAULT_MESSAGE = """Bonjour [Prénom],

Avec Kenza, on se marie le vendredi 23 octobre 2026 à Meknès (Palais Laraki) — et on est ravis de vous compter parmi nos invités !

Pour suivre les infos et échanger avec les autres invités, rejoignez le groupe WhatsApp : [lien du groupe]

Toutes les infos pratiques (programme, comment venir, RSVP...) sont sur notre site : https://mariage-maroc.igolen.com — à la porte d'entrée, entrez simplement votre numéro de téléphone, il vous reconnaîtra directement.

À très vite,
Kenza & Julien"""


def _all_members(db: Session) -> list[HouseholdMember]:
    return list(
        db.execute(
            select(HouseholdMember)
            .options(selectinload(HouseholdMember.whatsapp_group))
            .order_by(HouseholdMember.household_id, HouseholdMember.id)
        ).scalars()
    )


def _all_groups(db: Session) -> list[WhatsappGroup]:
    return list(db.execute(select(WhatsappGroup).order_by(WhatsappGroup.label)).scalars())


def _get_or_create_group(db: Session, label: str) -> WhatsappGroup | None:
    """Retrouve un groupe par libellé exact, ou le crée -- même logique que
    household.import_famille_label, pas d'écran de création séparé."""
    label = label.strip()
    if not label:
        return None
    group = db.execute(select(WhatsappGroup).where(WhatsappGroup.label == label)).scalar_one_or_none()
    if group is None:
        group = WhatsappGroup(label=label, message=_DEFAULT_MESSAGE)
        db.add(group)
        db.flush()
    return group


def _list_response(request: Request, db: Session):
    return templates.TemplateResponse(request, "partials/whatsapp_table.html", {"members": _all_members(db)})


@router.get("")
def whatsapp_list(request: Request, db: Session = Depends(get_db)):
    if (r := admin_redirect(request)) is not None:
        return r
    return templates.TemplateResponse(
        request,
        "admin_whatsapp.html",
        {"members": _all_members(db), "groups": _all_groups(db), "admin": current_admin(request, db)},
    )


@router.post("/member/{member_id}/group-label")
def whatsapp_set_group_label(
    member_id: int, request: Request, value: str = Form(""), db: Session = Depends(get_db)
):
    """Rattache (ou détache si vide) la personne à un groupe -- le libellé fait foi, pas
    un id : deux personnes qui tapent le même texte finissent dans le même groupe."""
    if (r := admin_redirect(request)) is not None:
        return r
    member = db.get(HouseholdMember, member_id)
    if member is not None:
        group = _get_or_create_group(db, value)
        member.whatsapp_group_id = group.id if group else None
        db.commit()
    return _list_response(request, db)


@router.post("/member/{member_id}/group-link")
def whatsapp_set_group_link(
    member_id: int, request: Request, value: str = Form(""), db: Session = Depends(get_db)
):
    """Édite le lien du GROUPE (partagé), pas un champ propre à la personne -- no-op si
    la personne n'a pas encore de groupe (rien à éditer)."""
    if (r := admin_redirect(request)) is not None:
        return r
    member = db.get(HouseholdMember, member_id)
    if member is not None and member.whatsapp_group is not None:
        member.whatsapp_group.invite_link = value.strip() or None
        db.commit()
    return _list_response(request, db)


@router.post("/member/{member_id}/sent-date")
def whatsapp_set_sent_date(
    member_id: int, request: Request, value: str = Form(""), db: Session = Depends(get_db)
):
    if (r := admin_redirect(request)) is not None:
        return r
    member = db.get(HouseholdMember, member_id)
    if member is not None:
        value = value.strip()
        if value:
            try:
                member.whatsapp_invite_envoyee_le = date_type.fromisoformat(value)
            except ValueError:
                pass
        else:
            member.whatsapp_invite_envoyee_le = None
        db.commit()
    return _list_response(request, db)


def _vcard_escape(value: str) -> str:
    """Échappe , ; \\ et retours à la ligne -- seuls caractères spéciaux du format
    vCard (RFC 6350 §3.4) susceptibles d'apparaître dans un nom."""
    return value.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


@router.get("/member/{member_id}/vcard")
def whatsapp_member_vcard(member_id: int, request: Request, db: Session = Depends(get_db)):
    """Fiche contact téléchargeable (Patron 2026-08-01) -- pour importer un invité dans le
    répertoire du téléphone avant de lui écrire, sans repasser par WhatsApp. Prénom = premier
    mot du champ Invité, même découpage que le placeholder [Prénom] (partials/whatsapp_table.html)."""
    if (r := admin_redirect(request)) is not None:
        return r
    member = db.get(HouseholdMember, member_id)
    if member is None:
        return Response(status_code=404)
    parts = member.nom_prenom.split(maxsplit=1)
    prenom, nom = (parts[0], parts[1]) if len(parts) > 1 else (parts[0], "")
    vcard = (
        "BEGIN:VCARD\r\n"
        "VERSION:3.0\r\n"
        f"N:{_vcard_escape(nom)};{_vcard_escape(prenom)};;;\r\n"
        f"FN:{_vcard_escape(member.nom_prenom)}\r\n"
        f"TEL;TYPE=CELL:{member.phone}\r\n"
        "END:VCARD\r\n"
    )
    filename = re.sub(r'[\\/:*?"<>|]', "", member.nom_prenom).strip() or "contact"
    return Response(
        content=vcard,
        media_type="text/vcard",
        headers={"Content-Disposition": f'attachment; filename="{filename}.vcf"'},
    )


@router.get("/groups")
def whatsapp_groups_root(request: Request, db: Session = Depends(get_db)):
    """Point d'entrée générique (lien depuis l'écran liste) -- redirige vers le premier
    groupe, ou affiche l'état vide si aucun groupe n'existe encore."""
    if (r := admin_redirect(request)) is not None:
        return r
    groups = _all_groups(db)
    if not groups:
        return templates.TemplateResponse(
            request,
            "admin_whatsapp_group.html",
            {"group": None, "groups": [], "admin": current_admin(request, db)},
        )
    return RedirectResponse(f"/admin/whatsapp/groups/{groups[0].id}", status_code=303)


@router.get("/groups/{group_id}")
def whatsapp_group_detail(group_id: int, request: Request, db: Session = Depends(get_db)):
    if (r := admin_redirect(request)) is not None:
        return r
    groups = _all_groups(db)
    group = next((g for g in groups if g.id == group_id), None)
    if group is None:
        return RedirectResponse("/admin/whatsapp/groups", status_code=303)
    return templates.TemplateResponse(
        request,
        "admin_whatsapp_group.html",
        {"group": group, "groups": groups, "admin": current_admin(request, db)},
    )


@router.post("/groups/{group_id}/message")
def whatsapp_group_save_message(
    group_id: int, request: Request, message: str = Form(""), db: Session = Depends(get_db)
):
    if (r := admin_redirect(request)) is not None:
        return r
    group = db.get(WhatsappGroup, group_id)
    if group is not None:
        group.message = message.strip() or None
        db.commit()
    return RedirectResponse(f"/admin/whatsapp/groups/{group_id}", status_code=303)
