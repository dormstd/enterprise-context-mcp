"""Development process tools — coding standards, project checklists, dependency policies."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from db import query_entries
from models import KnowledgeEntry, KnowledgeList

dev_server = FastMCP("Development")

_CATEGORY = "development_process"


@dev_server.tool(annotations={"readOnlyHint": True})
async def get_development_standards(ctx: Context) -> KnowledgeList:
    """Return the company's general development standards.

    Covers coding standards, naming conventions, code documentation requirements,
    and quality expectations that apply to all projects regardless of technology.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["standards"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@dev_server.tool(annotations={"readOnlyHint": True})
async def get_new_project_checklist(ctx: Context) -> KnowledgeList:
    """Return the high-level checklist for bootstrapping a new project.

    Aggregates everything a developer needs to consider when starting a new project:
    repository setup, CI/CD integration, security scanning, observability, documentation,
    and production readiness requirements.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["new-project"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@dev_server.tool(annotations={"readOnlyHint": True})
async def get_dependency_management_policy(ctx: Context) -> KnowledgeList:
    """Return the company policy for managing third-party dependencies.

    Covers dependency approval process, version pinning requirements,
    vulnerability handling procedures, and approved package registries.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["dependencies"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))
