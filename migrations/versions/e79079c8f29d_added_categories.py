"""added categories

Revision ID: e79079c8f29d
Revises: 401b73b5d218
Create Date: 2024-08-16 10:47:31.439881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e79079c8f29d'
down_revision = '401b73b5d218'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###