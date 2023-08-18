"""

Revision ID: d08bfa70180b
Revises: d06be7bab138
Create Date: 2023-08-18 13:51:20.988139

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd08bfa70180b'
down_revision = 'd06be7bab138'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('achievements', 'acceptedBy',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_constraint('fk_achievements_acceptedBy_users', 'achievements', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('fk_achievements_acceptedBy_users', 'achievements', 'users', ['acceptedBy'], ['uuid'], ondelete='CASCADE')
    op.alter_column('achievements', 'acceptedBy',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###