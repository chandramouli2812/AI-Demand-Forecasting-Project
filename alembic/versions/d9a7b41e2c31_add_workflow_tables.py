"""add workflow tables

Revision ID: d9a7b41e2c31
Revises: c7616dbbb55b
Create Date: 2026-06-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd9a7b41e2c31'
down_revision: Union[str, Sequence[str], None] = 'c7616dbbb55b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'data_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('type', sa.String(length=100), nullable=False),
        sa.Column('connection_string', sa.String(length=1024), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default=sa.text("'inactive'")),
        sa.Column('health', sa.String(length=50), nullable=False, server_default=sa.text("'unknown'")),
        sa.Column('last_sync', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_data_sources_id'), 'data_sources', ['id'], unique=False)

    op.create_table(
        'uploads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=1024), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default=sa.text("'pending'")),
        sa.Column('uploaded_by', sa.String(length=255), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_uploads_id'), 'uploads', ['id'], unique=False)

    op.create_table(
        'validation_errors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source', sa.String(length=255), nullable=False),
        sa.Column('error_type', sa.String(length=255), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False, server_default=sa.text("'medium'")),
        sa.Column('rows_affected', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('status', sa.String(length=50), nullable=False, server_default=sa.text("'open'")),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_validation_errors_id'), 'validation_errors', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_validation_errors_id'), table_name='validation_errors')
    op.drop_table('validation_errors')
    op.drop_index(op.f('ix_uploads_id'), table_name='uploads')
    op.drop_table('uploads')
    op.drop_index(op.f('ix_data_sources_id'), table_name='data_sources')
    op.drop_table('data_sources')
