"""Add requirements.capability_id (R1-B43 PR 2, TB-0188/PB-0190).

No requirement-to-capability association existed before this -- the
guided-design requirements-capture step traces a requirement to the
capability it realises, through unified_capabilities (ADR 0008's
canonical capability store), not a second one.

Revision ID: 20261004_req_capability
Revises: 20261007_public_visitor_events
Create Date: 2026-10-04

Re-chained 2026-10-08: this revision originally built on
20261006_agent_registration, main's single head at the time it was
written. Main has since progressed agent_registration -> 20261005_bf_
capability_fk -> 20261006_owner_element_ref -> 20261007_public_visitor_
events (the current single head) without this branch picking those up,
producing two heads ("Multiple head revisions are present") in CI's
schema-drift gate. Re-pointed to the real current head; this revision's
own upgrade/downgrade are unaffected (they only touch requirements.*).
"""
from alembic import op
from sqlalchemy import text

revision = "20261004_req_capability"
down_revision = "20261007_public_visitor_events"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    bind.execute(text(
        "ALTER TABLE requirements ADD COLUMN IF NOT EXISTS capability_id INTEGER "
        "REFERENCES unified_capabilities(id) ON DELETE SET NULL"
    ))
    bind.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_requirements_capability_id ON requirements(capability_id)"
    ))
    bind.execute(text(
        "ALTER TABLE requirements ADD COLUMN IF NOT EXISTS solution_id INTEGER "
        "REFERENCES solutions(id) ON DELETE CASCADE"
    ))
    bind.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_requirements_solution_id ON requirements(solution_id)"
    ))


def downgrade():
    bind = op.get_bind()
    bind.execute(text("DROP INDEX IF EXISTS ix_requirements_solution_id"))
    bind.execute(text("ALTER TABLE requirements DROP COLUMN IF EXISTS solution_id"))
    bind.execute(text("DROP INDEX IF EXISTS ix_requirements_capability_id"))
    bind.execute(text("ALTER TABLE requirements DROP COLUMN IF EXISTS capability_id"))
