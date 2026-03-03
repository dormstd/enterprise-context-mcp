"""Architecture tools — guidelines, patterns, and technology radar."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from db import query_entries
from models import KnowledgeEntry, KnowledgeList

arch_server = FastMCP("Architecture")

_CATEGORY = "architecture"


@arch_server.tool(annotations={"readOnlyHint": True})
async def get_architecture_guidelines(ctx: Context) -> KnowledgeList:
    """Return the company's architecture guidelines and decision-making process.

    Covers approved patterns, when an Architecture Decision Record (ADR) is required,
    the architecture review process, and principles guiding system design choices.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["guidelines"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@arch_server.tool(annotations={"readOnlyHint": True})
async def get_tech_radar(ctx: Context) -> KnowledgeList:
    """Return the current state of the company technology radar.

    Lists technologies classified by adoption status:
    - Adopt: proven, recommended for production use
    - Trial: worth pursuing, with careful evaluation
    - Assess: worth exploring, not yet mature enough for production
    - Hold: avoid for new projects; may still exist in legacy systems
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["tech-radar"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))
