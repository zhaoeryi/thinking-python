"""create account table

Revision ID: b4032e2ad23
Revises: None
Create Date: 2014-02-25 11:41:21.951809

"""

# revision identifiers, used by Alembic.
revision = 'b4032e2ad23'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('account')
