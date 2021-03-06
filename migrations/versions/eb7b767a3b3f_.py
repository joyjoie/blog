"""empty message

Revision ID: eb7b767a3b3f
Revises: 3aca3545b256
Create Date: 2019-02-19 11:56:15.684528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb7b767a3b3f'
down_revision = '3aca3545b256'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'profile_pic_path',
               existing_type=sa.VARCHAR(),
               nullable='False')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'profile_pic_path',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
