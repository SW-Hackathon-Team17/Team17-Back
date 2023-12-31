"""empty message

Revision ID: ddd5b6cccf33
Revises: 74421cc8bd78
Create Date: 2023-06-29 11:37:16.256256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddd5b6cccf33'
down_revision = '74421cc8bd78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scriptonly',
    sa.Column('scriptOnlyIdx', sa.Integer(), nullable=False),
    sa.Column('formIdx', sa.Integer(), nullable=True),
    sa.Column('script', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['formIdx'], ['form.formIdx'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('scriptOnlyIdx')
    )
    op.drop_table('script_only')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('script_only',
    sa.Column('scriptOnlyIdx', sa.INTEGER(), nullable=False),
    sa.Column('formIdx', sa.INTEGER(), nullable=True),
    sa.Column('script', sa.TEXT(), nullable=False),
    sa.ForeignKeyConstraint(['formIdx'], ['form.formIdx'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('scriptOnlyIdx')
    )
    op.drop_table('scriptonly')
    # ### end Alembic commands ###
