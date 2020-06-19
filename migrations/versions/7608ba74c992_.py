"""empty message

Revision ID: 7608ba74c992
Revises: 4077186f4887
Create Date: 2020-05-03 20:27:06.854138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7608ba74c992'
down_revision = '4077186f4887'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product_categories', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('subscribers', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('subscribers', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('subscribers', 'status',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subscribers', 'status',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('subscribers', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('subscribers', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('product_categories', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
