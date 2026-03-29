"""initial migration
Revision ID: 0c65a4f76152
Revises: 
Create Date: 2026-03-28 15:59:08.558489
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
# revision identifiers, used by Alembic.
revision: str = '0c65a4f76152'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    """Upgrade schema."""
    # ensure enum type exists; do nothing if already present
    op.execute("""
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
        CREATE TYPE userrole AS ENUM ('student', 'teacher', 'admin');
    END IF;
END$$;
""")
    op.create_table('users',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column('role', postgresql.ENUM('student', 'teacher', 'admin', name='userrole', create_type=False), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('users_pkey'))
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('courses',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
        sa.Column('is_free', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column('thumbnail', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('is_published', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], name=op.f('courses_teacher_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('courses_pkey'))
    )
    op.create_index(op.f('ix_courses_title'), 'courses', ['title'], unique=False)
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    op.create_table('sections',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('order_num', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name=op.f('sections_course_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('sections_pkey'))
    )
    op.create_index(op.f('ix_sections_id'), 'sections', ['id'], unique=False)
    op.create_table('lectures',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('video_url', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('is_preview', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column('order_num', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('section_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['section_id'], ['sections.id'], name=op.f('lectures_section_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('lectures_pkey'))
    )
    op.create_index(op.f('ix_lectures_id'), 'lectures', ['id'], unique=False)
    op.create_table('notes',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('pdf_url', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('section_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['section_id'], ['sections.id'], name=op.f('notes_section_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('notes_pkey'))
    )
    op.create_index(op.f('ix_notes_id'), 'notes', ['id'], unique=False)
    op.create_table('enrollments',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('enrollment_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name=op.f('enrollments_course_id_fkey'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('enrollments_user_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('enrollments_pkey')),
        sa.UniqueConstraint('user_id', 'course_id', name=op.f('uix_user_course_enrollment'))
    )
    op.create_index(op.f('ix_enrollments_id'), 'enrollments', ['id'], unique=False)
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_enrollments_id'), table_name='enrollments')
    op.drop_table('enrollments')
    op.drop_index(op.f('ix_notes_id'), table_name='notes')
    op.drop_table('notes')
    op.drop_index(op.f('ix_lectures_id'), table_name='lectures')
    op.drop_table('lectures')
    op.drop_index(op.f('ix_sections_id'), table_name='sections')
    op.drop_table('sections')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_index(op.f('ix_courses_title'), table_name='courses')
    op.drop_table('courses')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS userrole;")
