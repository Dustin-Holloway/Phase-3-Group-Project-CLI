"""Added model

Revision ID: a5fcf7684d19
Revises: cbc9c4ec2a7d
Create Date: 2023-05-15 11:42:51.459433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5fcf7684d19'
down_revision = 'cbc9c4ec2a7d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('information',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('information')
    # ### end Alembic commands ###