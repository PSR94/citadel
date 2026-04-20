"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-19
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=False),
        sa.Column("source_path", sa.String(length=1024), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("owner_team", sa.String(length=256), nullable=True),
        sa.Column("domain", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("access_scope", sa.String(length=64), nullable=False, server_default="internal"),
        sa.Column("content_hash", sa.String(length=128), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_documents_domain", "documents", ["domain"])
    op.create_index("ix_documents_owner_team", "documents", ["owner_team"])

    op.create_table(
        "chunks",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("document_id", sa.String(length=64), sa.ForeignKey("documents.id"), nullable=False),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=False),
        sa.Column("embedding_status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_chunks_document_id", "chunks", ["document_id"])

    op.create_table(
        "ingestion_runs",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("trigger", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("processed_documents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("processed_chunks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("summary_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "retrieval_runs",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("query", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("request_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("response_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("timings_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("provider_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "eval_runs",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("profile", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("metrics_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("details_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "provider_states",
        sa.Column("name", sa.String(length=64), primary_key=True),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("latency_ms", sa.Float(), nullable=True),
        sa.Column("details_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("checked_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("actor", sa.String(length=256), nullable=False),
        sa.Column("resource", sa.String(length=256), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("provider_states")
    op.drop_table("eval_runs")
    op.drop_table("retrieval_runs")
    op.drop_table("ingestion_runs")
    op.drop_index("ix_chunks_document_id", table_name="chunks")
    op.drop_table("chunks")
    op.drop_index("ix_documents_owner_team", table_name="documents")
    op.drop_index("ix_documents_domain", table_name="documents")
    op.drop_table("documents")

