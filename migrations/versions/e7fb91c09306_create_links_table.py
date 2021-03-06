"""create links table

Revision ID: e7fb91c09306
Revises: 4ea32de0a2ed
Create Date: 2021-11-07 12:28:50.630410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7fb91c09306'
down_revision = '4ea32de0a2ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('url', sa.String(length=512), nullable=False),
    sa.Column('shorten_url', sa.String(length=256), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link')
    # ### end Alembic commands ###
