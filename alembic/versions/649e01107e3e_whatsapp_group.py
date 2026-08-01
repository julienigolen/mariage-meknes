"""whatsapp_group + household_member.whatsapp_group_id/whatsapp_invite_envoyee_le

Ajout Patron du 2026-08-01 : écran dédié aux invitations WhatsApp (liste par personne,
principal ou secondaire, rattachée à un groupe créé/retrouvé par libellé) + écran de
message personnalisé par groupe (5-10 groupes attendus). `whatsapp_invite_envoyee_le`
est une DATE (pas un booléen) pour savoir quand une invitation a été envoyée, pas
seulement si.

Revision ID: 649e01107e3e
Revises: e91b4c6f2a08
Create Date: 2026-08-01
"""
from alembic import op
import sqlalchemy as sa

revision = '649e01107e3e'
down_revision = 'e91b4c6f2a08'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'whatsapp_group',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('label', sa.String(length=200), nullable=False),
        sa.Column('invite_link', sa.String(length=500), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('label'),
    )
    op.add_column(
        'household_member',
        sa.Column('whatsapp_group_id', sa.Integer(), nullable=True),
    )
    op.add_column(
        'household_member',
        sa.Column('whatsapp_invite_envoyee_le', sa.Date(), nullable=True),
    )
    op.create_foreign_key(
        'fk_household_member_whatsapp_group_id',
        'household_member', 'whatsapp_group',
        ['whatsapp_group_id'], ['id'],
        ondelete='SET NULL',
    )


def downgrade() -> None:
    op.drop_constraint('fk_household_member_whatsapp_group_id', 'household_member', type_='foreignkey')
    op.drop_column('household_member', 'whatsapp_invite_envoyee_le')
    op.drop_column('household_member', 'whatsapp_group_id')
    op.drop_table('whatsapp_group')
