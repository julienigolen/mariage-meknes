"""Modèle de données v2 — cf. docs/projet_mariage-meknes/proposition_produit.md §3.

household        : le foyer (unité de réponse RSVP), regroupé à l'import via la colonne
                    `famille` de l'Excel (§2 point 4). Une ligne sans famille = son propre foyer.
household_member : une ligne par personne importée, rattachée à un foyer. Porte le téléphone
                    (identifiant de connexion) — un foyer peut avoir N membres, donc N numéros.
rsvp              : une ligne par foyer (pas par personne). Son existence déclenche le
                    pré-remplissage à la resoumission.
admin_user        : les mariés (accès admin — pas encore d'écran dans ce MVP).
whatsapp_group    : groupe WhatsApp d'invités (Patron, 2026-08-01) — lien d'invitation
                    (chat.whatsapp.com/...) + message personnalisé, partagés par tous les
                    household_member qui y sont rattachés. Créé/retrouvé par libellé
                    depuis l'écran invitations WhatsApp (pas d'écran de création dédié,
                    même logique que `import_famille_label` sur household).

Colonnes volontairement absentes de ce MVP (§5.16-21 de la proposition) : email/token_modification
sur rsvp (email de confirmation différé), message_personnalise et relance_le sur household
(goodie et suivi admin différés), settings.date_limite_rsvp (pas d'écran admin pour l'éditer —
la date cible reste un texte statique côté template pour l'instant).
"""
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Household(Base):
    __tablename__ = "household"

    id: Mapped[int] = mapped_column(primary_key=True)
    import_famille_label: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    members: Mapped[list["HouseholdMember"]] = relationship(
        back_populates="household", cascade="all, delete-orphan"
    )
    rsvp: Mapped["Rsvp | None"] = relationship(
        back_populates="household", cascade="all, delete-orphan", uselist=False
    )


class HouseholdMember(Base):
    __tablename__ = "household_member"

    id: Mapped[int] = mapped_column(primary_key=True)
    household_id: Mapped[int] = mapped_column(ForeignKey("household.id", ondelete="CASCADE"))
    nom_prenom: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    origine: Mapped[str] = mapped_column(String(2), default="fr")  # fr | ma
    langue: Mapped[str] = mapped_column(String(2), default="fr")   # fr | ar — déduite de l'indicatif, dormante (§5.13)
    import_source: Mapped[str | None] = mapped_column(String(200))  # traçabilité ligne Excel
    # liste_origine (import Excel) | ajoute_rsvp (numéro non répertorié mais au bon
    # format, saisi au RSVP — Patron 2026-07-28) : distingue la liste de mariage
    # d'origine des invités que le foyer a lui-même ajoutés à l'identification.
    # Ne pilote plus le badge "Statut" affiché (Invité/Accepté/Refusé, purement dérivé
    # de la réponse RSVP, Patron 2026-07-29) — sert uniquement au repère visuel
    # "auto-inscrit" de la table admin.
    statut: Mapped[str] = mapped_column(String(20), default="liste_origine")
    # Effectif théorique que représente CETTE ligne avant toute réponse RSVP (Patron
    # 2026-07-29) — par défaut 1 (une ligne = une personne), mais ajustable pour un
    # contact qui représente en réalité plusieurs personnes (ex. "Famille Dupont" sans
    # lister chaque enfant). Alimente le KPI "Invités" tant que le foyer n'a pas répondu ;
    # une fois répondu, c'est l'effectif réel du RSVP qui prend le relais (§ compteur
    # d'invités, app/routers/admin.py::_compute_kpis).
    effectif_theorique: Mapped[int] = mapped_column(Integer, default=1)

    # Invitation WhatsApp (Patron 2026-08-01) : groupe rattaché (0 ou 1, get-or-create par
    # libellé) + date d'envoi du lien d'invitation à CETTE personne. La date (pas un simple
    # booléen) permet de savoir QUAND, de corriger une erreur de saisie, et suit le pattern
    # déjà retenu pour `household.relance_le` (proposition_produit.md §5.16) plutôt que
    # d'introduire un second système de suivi. Nulle = pas encore envoyé.
    whatsapp_group_id: Mapped[int | None] = mapped_column(ForeignKey("whatsapp_group.id", ondelete="SET NULL"))
    whatsapp_invite_envoyee_le: Mapped[date | None] = mapped_column(Date)

    household: Mapped["Household"] = relationship(back_populates="members")
    whatsapp_group: Mapped["WhatsappGroup | None"] = relationship(back_populates="members")


class Rsvp(Base):
    __tablename__ = "rsvp"
    __table_args__ = (UniqueConstraint("household_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    household_id: Mapped[int] = mapped_column(ForeignKey("household.id", ondelete="CASCADE"))
    presence: Mapped[bool] = mapped_column(Boolean)
    nb_adultes: Mapped[int] = mapped_column(Integer, default=0)
    nb_enfants: Mapped[int] = mapped_column(Integer, default=0)
    allergies_bool: Mapped[bool] = mapped_column(Boolean, default=False)
    allergies_texte: Mapped[str | None] = mapped_column(Text)
    besoin_hotel: Mapped[bool] = mapped_column(Boolean, default=False)
    horodatage: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    household: Mapped["Household"] = relationship(back_populates="rsvp")


class WhatsappGroup(Base):
    __tablename__ = "whatsapp_group"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(200), unique=True)
    invite_link: Mapped[str | None] = mapped_column(String(500))
    # Texte libre, plusieurs lignes, saisi une fois pour tout le groupe -- jamais traduit
    # ni généré automatiquement (même principe que le message personnalisé RSVP, §5.17 :
    # le Patron connaît ses invités et écrit lui-même).
    message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    members: Mapped[list["HouseholdMember"]] = relationship(back_populates="whatsapp_group")


class AdminUser(Base):
    __tablename__ = "admin_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
