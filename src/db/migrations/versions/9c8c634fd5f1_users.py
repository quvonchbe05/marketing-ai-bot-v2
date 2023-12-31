"""users

Revision ID: 9c8c634fd5f1
Revises: 9528f4dd24f5
Create Date: 2023-12-01 09:39:42.966802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c8c634fd5f1'
down_revision: Union[str, None] = '9528f4dd24f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('history', sa.Column('user_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'history', 'user', ['user_id'], ['id'])
    op.drop_column('history', 'user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('history', sa.Column('user', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'history', type_='foreignkey')
    op.drop_column('history', 'user_id')
    op.drop_table('user')
    # ### end Alembic commands ###
