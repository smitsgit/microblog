"""Add followers association support

Revision ID: 03bcc08f4144
Revises: be9e43144b90
Create Date: 2023-07-14 09:56:23.081210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03bcc08f4144'
down_revision = 'be9e43144b90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###