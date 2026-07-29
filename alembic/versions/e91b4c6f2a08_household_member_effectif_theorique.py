"""household_member.effectif_theorique — effectif théorique par ligne avant réponse RSVP

Ajout Patron du 2026-07-29 : le KPI "Invités" compte désormais l'effectif théorique
(par défaut 1 par ligne, ajustable) tant qu'un foyer n'a pas répondu, puis l'effectif
réel du RSVP une fois répondu. Sans ce champ, une ligne "Famille Dupont" représentant
plusieurs personnes ne pouvait pas être comptée correctement avant réponse.

Revision ID: e91b4c6f2a08
Revises: c7a19d3e5f21
Create Date: 2026-07-29
"""
from alembic import op
import sqlalchemy as sa

revision = 'e91b4c6f2a08'
down_revision = 'c7a19d3e5f21'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "household_member",
        sa.Column("effectif_theorique", sa.Integer(), nullable=False, server_default="1"),
    )


def downgrade() -> None:
    op.drop_column("household_member", "effectif_theorique")
