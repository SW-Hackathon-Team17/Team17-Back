"""empty message

Revision ID: fa5cfa0792a5
Revises: b68ee7b56b99
Create Date: 2023-06-29 11:43:35.603159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa5cfa0792a5'
down_revision = 'b68ee7b56b99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('topic', sa.Integer(), nullable=True))

    with op.batch_alter_table('keyword', schema=None) as batch_op:
        batch_op.add_column(sa.Column('topic', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('keyword', schema=None) as batch_op:
        batch_op.drop_column('topic')

    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_column('topic')

    # ### end Alembic commands ###