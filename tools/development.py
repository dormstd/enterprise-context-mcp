"""Development process tools — coding standards, project checklists, dependency policies."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from db import fetch_knowledge
from models import KnowledgeList

dev_server = FastMCP("Development")

_CATEGORY = "development_process"


@dev_server.tool(annotations={"readOnlyHint": True})
async def get_development_standards(ctx: Context) -> KnowledgeList:
    """Return the company's general development standards.

    Covers coding standards, naming conventions, code documentation requirements,
    and quality expectations that apply to all projects regardless of technology.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["standards"])


@dev_server.tool(annotations={"readOnlyHint": True})
async def get_new_project_checklist(ctx: Context) -> KnowledgeList:
    """Return the high-level checklist for bootstrapping a new project.

    Aggregates everything a developer needs to consider when starting a new project:
    repository setup, CI/CD integration, security scanning, observability, documentation,
    and production readiness requirements.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["new-project"])


@dev_server.tool(annotations={"readOnlyHint": True})
async def get_dependency_management_policy(ctx: Context) -> KnowledgeList:
    """Return the company policy for managing third-party dependencies.

    Covers dependency approval process, version pinning requirements,
    vulnerability handling procedures, and approved package registries.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["dependencies"])
