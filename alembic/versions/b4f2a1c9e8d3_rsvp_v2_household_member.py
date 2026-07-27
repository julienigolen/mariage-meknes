"""rsvp v2 : household/household_member/rsvp (mono-evenement, identification telephone)

Revision ID: b4f2a1c9e8d3
Revises: d6b38e86c282
Create Date: 2026-07-28 00:00:00.000000

Remplace le modele S0 (household name/email/phone + guest + event + rsvp multi-evenement)
par le modele v2 issu de docs/projet_mariage-meknes/proposition_produit.md §3 :
une ligne par personne importee (household_member, telephone = identifiant), regroupees
en foyer (household) via la colonne `famille` de l'Excel, une reponse RSVP par foyer.
Tables prod vides (RSVP jamais construit avant cette migration) — drop/recreate sans
migration de donnees.
"""
from alembic import op
import sqlalchemy as sa


revision = 'b4f2a1c9e8d3'
down_revision = 'd6b38e86c282'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('rsvp')
    op.drop_table('guest')
    op.drop_table('event')
    op.drop_table('household')

    op.create_table('household',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('import_famille_label', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table('household_member',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('household_id', sa.Integer(), nullable=False),
        sa.Column('nom_prenom', sa.String(length=200), nullable=False),
        sa.Column('phone', sa.String(length=40), nullable=False),
        sa.Column('origine', sa.String(length=2), nullable=False),
        sa.Column('langue', sa.String(length=2), nullable=False),
        sa.Column('import_source', sa.String(length=200), nullable=True),
        sa.ForeignKeyConstraint(['household_id'], ['household.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('phone'),
    )
    op.create_index('ix_household_member_phone', 'household_member', ['phone'])
    op.create_table('rsvp',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('household_id', sa.Integer(), nullable=False),
        sa.Column('presence', sa.Boolean(), nullable=False),
        sa.Column('nb_adultes', sa.Integer(), nullable=False),
        sa.Column('nb_enfants', sa.Integer(), nullable=False),
        sa.Column('allergies_bool', sa.Boolean(), nullable=False),
        sa.Column('allergies_texte', sa.Text(), nullable=True),
        sa.Column('besoin_hotel', sa.Boolean(), nullable=False),
        sa.Column('horodatage', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['household_id'], ['household.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('household_id'),
    )


def downgrade() -> None:
    op.drop_table('rsvp')
    op.drop_index('ix_household_member_phone', table_name='household_member')
    op.drop_table('household_member')
    op.drop_table('household')

    op.create_table('household',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=True),
        sa.Column('phone', sa.String(length=40), nullable=True),
        sa.Column('origin', sa.String(length=2), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table('event',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('starts_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('location', sa.String(length=200), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_table('guest',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('household_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('is_child', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['household_id'], ['household.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table('rsvp',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('household_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=10), nullable=False),
        sa.Column('attendees_count', sa.Integer(), nullable=False),
        sa.Column('dietary', sa.Text(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['event.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['household_id'], ['household.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('household_id', 'event_id'),
    )
