"""empty message

Revision ID: 9cb70ab6c07b
Revises: 
Create Date: 2023-06-29 11:32:16.428175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cb70ab6c07b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('form',
    sa.Column('formIdx', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('formIdx')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('form')
    # ### end Alembic commands ###
