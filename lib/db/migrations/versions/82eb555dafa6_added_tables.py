"""Added Tables

Revision ID: 82eb555dafa6
Revises: 1c22ae5fc9bf
Create Date: 2023-05-16 14:39:29.436473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82eb555dafa6'
down_revision = '1c22ae5fc9bf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bikes')
    op.drop_table('lockers')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lockers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('locker_location', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bikes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
