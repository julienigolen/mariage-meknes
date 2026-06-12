"""Modèle de données — cf. docs/PROPOSITION_site_mariage_meknes.md §4.

household : le foyer (unité de réponse RSVP)
guest     : personne rattachée à un foyer
event     : moment du programme (le mariage = Palais Laraki, N moments à définir)
rsvp      : réponse d'un foyer pour un événement
admin_user: les mariés (accès admin)
"""
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Household(Base):
    __tablename__ = "household"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))           # « Famille Bennani », « Sophie & Marc »
    email: Mapped[str | None] = mapped_column(String(320))
    phone: Mapped[str | None] = mapped_column(String(40))
    origin: Mapped[str] = mapped_column(String(2), default="fr")  # fr | ma
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    guests: Mapped[list["Guest"]] = relationship(back_populates="household", cascade="all, delete-orphan")
    rsvps: Mapped[list["Rsvp"]] = relationship(back_populates="household", cascade="all, delete-orphan")


class Guest(Base):
    __tablename__ = "guest"

    id: Mapped[int] = mapped_column(primary_key=True)
    household_id: Mapped[int] = mapped_column(ForeignKey("household.id", ondelete="CASCADE"))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    is_child: Mapped[int] = mapped_column(Integer, default=0)  # 0/1 (portable sqlite/pg)

    household: Mapped["Household"] = relationship(back_populates="guests")


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True)
    title: Mapped[str] = mapped_column(String(200))
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    location: Mapped[str] = mapped_column(String(200), default="Palais Laraki, Meknès")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class Rsvp(Base):
    __tablename__ = "rsvp"
    __table_args__ = (UniqueConstraint("household_id", "event_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    household_id: Mapped[int] = mapped_column(ForeignKey("household.id", ondelete="CASCADE"))
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(10), default="pending")  # yes | no | pending
    attendees_count: Mapped[int] = mapped_column(Integer, default=0)
    dietary: Mapped[str | None] = mapped_column(Text)                    # allergies / régimes
    message: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    household: Mapped["Household"] = relationship(back_populates="rsvps")


class AdminUser(Base):
    __tablename__ = "admin_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
