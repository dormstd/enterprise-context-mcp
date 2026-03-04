"""Architecture tools — guidelines, patterns, and technology radar."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from db import fetch_knowledge
from models import KnowledgeList

arch_server = FastMCP("Architecture")

_CATEGORY = "architecture"


@arch_server.tool(annotations={"readOnlyHint": True})
async def get_architecture_guidelines(ctx: Context) -> KnowledgeList:
    """Return the company's architecture guidelines and decision-making process.

    Covers approved patterns, when an Architecture Decision Record (ADR) is required,
    the architecture review process, and principles guiding system design choices.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["guidelines"])


@arch_server.tool(annotations={"readOnlyHint": True})
async def get_tech_radar(ctx: Context) -> KnowledgeList:
    """Return the current state of the company technology radar.

    Lists technologies classified by adoption status:
    - Adopt: proven, recommended for production use
    - Trial: worth pursuing, with careful evaluation
    - Assess: worth exploring, not yet mature enough for production
    - Hold: avoid for new projects; may still exist in legacy systems
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["tech-radar"])
