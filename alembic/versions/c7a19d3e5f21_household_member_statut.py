"""household_member.statut — distingue liste d'origine et ajouts au RSVP

Ajout Patron du 2026-07-28 : un invité au numéro non répertorié mais au format
plausible (FR/MA/US) peut désormais s'ajouter lui-même à l'identification RSVP
(cf. app/routers/rsvp.py). `statut` distingue liste_origine (import Excel) de
ajoute_rsvp (auto-ajout), sans quoi les deux seraient indiscernables en base.

Revision ID: c7a19d3e5f21
Revises: b4f2a1c9e8d3
Create Date: 2026-07-28
"""
from alembic import op
import sqlalchemy as sa

revision = 'c7a19d3e5f21'
down_revision = 'b4f2a1c9e8d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "household_member",
        sa.Column("statut", sa.String(length=20), nullable=False, server_default="liste_origine"),
    )


def downgrade() -> None:
    op.drop_column("household_member", "statut")
