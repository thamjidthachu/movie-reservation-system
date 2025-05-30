"""empty message

Revision ID: 92e6d5e91583
Revises: 3d186f090959
Create Date: 2025-05-26 11:43:55.928000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92e6d5e91583'
down_revision = '3d186f090959'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('unique_booking_per_user_per_showtime'), type_='unique')
        batch_op.create_unique_constraint('unique_booking_per_user_per_showtime', ['showtime_id', 'user_id', 'created_at'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_constraint('unique_booking_per_user_per_showtime', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('unique_booking_per_user_per_showtime'), ['showtime_id', 'user_id'])

    # ### end Alembic commands ###
