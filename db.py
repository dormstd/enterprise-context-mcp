"""DuckDB lifespan and shared query helpers.

This server is read-only. Schema creation, seeding, and CRUD operations
are handled by the companion `enterprise-context-admin` project.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Any

import duckdb
from fastmcp import Context

from models import KnowledgeEntry, KnowledgeList

_DB_PATH_DEFAULT = "./enterprise.duckdb"


@asynccontextmanager
async def db_lifespan(app: Any):
    """Open a READ_ONLY DuckDB connection for the lifetime of the server."""
    db_path = os.environ.get("ENTERPRISE_DB_PATH", _DB_PATH_DEFAULT)
    con = duckdb.connect(db_path, read_only=True)
    try:
        yield {"db": con}
    finally:
        con.close()


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------


async def query_entries(
    db: duckdb.DuckDBPyConnection,
    *,
    category: str | None = None,
    role: str | None = None,
    tags: list[str] | None = None,
    search: str | None = None,
) -> list[dict[str, Any]]:
    """Return knowledge entries matching the given filters.

    All parameters are optional and can be combined:
    - category: filter by category name (e.g. 'cicd', 'security')
    - role: filter by target role (e.g. 'developer', 'devops')
    - tags: filter entries that have ALL of the provided tags
    - search: full-text search on title and content (case-insensitive)
    """
    conditions: list[str] = []
    params: list[Any] = []

    if category:
        conditions.append("c.name = ?")
        params.append(category)

    if role:
        conditions.append("""
            ke.id IN (
                SELECT er.entry_id
                FROM entry_roles er
                JOIN roles r ON r.id = er.role_id
                WHERE r.name = ?
            )
        """)
        params.append(role)

    if tags:
        for tag in tags:
            conditions.append("""
                ke.id IN (
                    SELECT et.entry_id
                    FROM entry_tags et
                    JOIN tags t ON t.id = et.tag_id
                    WHERE t.name = ?
                )
            """)
            params.append(tag)

    if search:
        conditions.append("(LOWER(ke.title) LIKE ? OR LOWER(ke.content) LIKE ?)")
        pattern = f"%{search.lower()}%"
        params.extend([pattern, pattern])

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    sql = f"""
        SELECT
            ke.id,
            ke.title,
            ke.content,
            c.name  AS category,
            c.description AS category_description,
            ke.created_at,
            ke.updated_at
        FROM knowledge_entries ke
        JOIN categories c ON c.id = ke.category_id
        {where}
        ORDER BY ke.id
    """

    rows = db.execute(sql, params).fetchall()
    col_names = [desc[0] for desc in db.description]  # type: ignore[union-attr]

    entries: list[dict[str, Any]] = []
    for row in rows:
        entry = dict(zip(col_names, row))
        entry_id = entry["id"]

        # Fetch associated roles
        role_rows = db.execute(
            """
            SELECT r.name FROM roles r
            JOIN entry_roles er ON er.role_id = r.id
            WHERE er.entry_id = ?
            """,
            [entry_id],
        ).fetchall()
        entry["target_roles"] = [r[0] for r in role_rows]

        # Fetch associated tags
        tag_rows = db.execute(
            """
            SELECT t.name FROM tags t
            JOIN entry_tags et ON et.tag_id = t.id
            WHERE et.entry_id = ?
            """,
            [entry_id],
        ).fetchall()
        entry["tags"] = [t[0] for t in tag_rows]

        entries.append(entry)

    return entries


async def fetch_knowledge(
    ctx: Context,
    *,
    category: str | None = None,
    tags: list[str] | None = None,
    role: str | None = None,
    search: str | None = None,
) -> KnowledgeList:
    """Resolve the DB connection from context, query entries, and return a KnowledgeList."""
    db = ctx.lifespan_context["db"]
    rows = await query_entries(db, category=category, tags=tags, role=role, search=search)
    items = [KnowledgeEntry(**entry) for entry in rows]
    return KnowledgeList(entries=items, total=len(items))
