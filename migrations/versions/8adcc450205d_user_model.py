"""user model

Revision ID: 8adcc450205d
Revises: 93d566467ead
Create Date: 2021-10-27 10:22:50.981673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8adcc450205d'
down_revision = '93d566467ead'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('gov_id', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('order', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'user_id')
    op.drop_table('user')
    # ### end Alembic commands ###
