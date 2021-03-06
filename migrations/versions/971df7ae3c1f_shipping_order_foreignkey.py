"""shipping-order foreignkey

Revision ID: 971df7ae3c1f
Revises: 14f80544a26b
Create Date: 2021-10-27 20:38:38.144385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '971df7ae3c1f'
down_revision = '14f80544a26b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shipping', sa.Column('order_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'shipping', 'order', ['order_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shipping', type_='foreignkey')
    op.drop_column('shipping', 'order_id')
    # ### end Alembic commands ###
