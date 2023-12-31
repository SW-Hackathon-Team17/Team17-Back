"""empty message

Revision ID: eeb8248dea10
Revises: 135e011ac27c
Create Date: 2023-06-29 16:58:06.498279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeb8248dea10'
down_revision = '135e011ac27c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('form', schema=None) as batch_op:
        batch_op.drop_column('check')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('form', schema=None) as batch_op:
        batch_op.add_column(sa.Column('check', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
