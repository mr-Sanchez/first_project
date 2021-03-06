"""empty message

Revision ID: 5e3cd395f772
Revises: fe64ee94f4ef
Create Date: 2021-04-08 11:51:13.962969

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5e3cd395f772'
down_revision = 'fe64ee94f4ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('purchase', 'purchase_discount')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchase', sa.Column('purchase_discount', mysql.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
