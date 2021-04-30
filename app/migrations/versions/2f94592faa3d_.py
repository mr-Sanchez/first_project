"""empty message

Revision ID: 2f94592faa3d
Revises: 
Create Date: 2021-04-08 11:42:37.623864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f94592faa3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clothes_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_path', sa.String(length=255), nullable=True),
    sa.Column('category_name', sa.String(length=255), nullable=True),
    sa.Column('clothes_for', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_method',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payment_method_name', sa.String(length=100), nullable=True),
    sa.Column('payment_method_caption', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=255), nullable=True),
    sa.Column('user_email', sa.String(length=255), nullable=True),
    sa.Column('user_password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_email')
    )
    op.create_table('Сoupon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coupon_code', sa.String(length=20), nullable=True),
    sa.Column('coupon_discount', sa.Integer(), nullable=True),
    sa.Column('coupon_is_added', sa.Boolean(), nullable=True),
    sa.Column('coupon_is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clothes_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('clothes_name', sa.String(length=255), nullable=True),
    sa.Column('clothes_price', sa.Integer(), nullable=True),
    sa.Column('clothes_discount', sa.Integer(), nullable=True),
    sa.Column('clothes_description', sa.Text(), nullable=True),
    sa.Column('clothes_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['clothes_category_id'], ['clothes_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('purchase_date', sa.DateTime(), nullable=True),
    sa.Column('purchase_cost', sa.Integer(), nullable=True),
    sa.Column('purchase_discount', sa.Integer(), nullable=True),
    sa.Column('purchase_address', sa.String(length=255), nullable=True),
    sa.Column('purchase_payment_method_id', sa.Integer(), nullable=True),
    sa.Column('purchase_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['purchase_payment_method_id'], ['payment_method.id'], ),
    sa.ForeignKeyConstraint(['purchase_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clothes_item_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('clothes_image_path', sa.String(length=255), nullable=True),
    sa.Column('clothes_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['clothes_id'], ['clothes_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clothes_sizes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('size', sa.String(length=100), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('clothes_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['clothes_id'], ['clothes_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sold_clothes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sold_clothes_quantity', sa.Integer(), nullable=True),
    sa.Column('sold_clothes_size_id', sa.Integer(), nullable=True),
    sa.Column('sold_clothes_purchase_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sold_clothes_purchase_id'], ['purchase.id'], ),
    sa.ForeignKeyConstraint(['sold_clothes_size_id'], ['clothes_sizes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sold_clothes')
    op.drop_table('clothes_sizes')
    op.drop_table('clothes_item_image')
    op.drop_table('purchase')
    op.drop_table('clothes_item')
    op.drop_table('Сoupon')
    op.drop_table('user')
    op.drop_table('payment_method')
    op.drop_table('clothes_category')
    # ### end Alembic commands ###