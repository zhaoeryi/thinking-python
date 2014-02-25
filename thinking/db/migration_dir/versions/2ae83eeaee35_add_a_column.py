"""Add a column

Revision ID: 2ae83eeaee35
Revises: b4032e2ad23
Create Date: 2014-02-25 13:14:16.893761

"""

# revision identifiers, used by Alembic.
revision = '2ae83eeaee35'
down_revision = 'b4032e2ad23'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    op.drop_column('account', 'last_transaction_date')
