"""alter links table (is_public -> status)

Revision ID: 3704e3875d3b
Revises: ae8c5048630a
Create Date: 2021-11-07 12:24:44.114481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3704e3875d3b'
down_revision = 'ae8c5048630a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('link', sa.Column('status', sa.String(length=10), nullable=False))
    op.drop_column('link', 'is_public')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('link', sa.Column('is_public', sa.VARCHAR(length=1), nullable=False))
    op.drop_column('link', 'status')
    # ### end Alembic commands ###