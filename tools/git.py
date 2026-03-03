"""Git process tools — PR conventions, branching strategy, code review standards."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from db import query_entries
from models import KnowledgeEntry, KnowledgeList

git_server = FastMCP("Git")

_CATEGORY = "git_pr"


@git_server.tool(annotations={"readOnlyHint": True})
async def get_pr_conventions(ctx: Context) -> KnowledgeList:
    """Return the company's pull request conventions.

    Covers required PR title format, description template, linked ticket requirements,
    review assignment rules, minimum approvals, and merge strategy (squash, rebase, merge).
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["pull-requests"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@git_server.tool(annotations={"readOnlyHint": True})
async def get_branching_strategy(ctx: Context) -> KnowledgeList:
    """Return the company's branching strategy and naming conventions.

    Covers the adopted flow model (trunk-based, gitflow, etc.), branch naming
    patterns, protected branch rules, release branch lifecycle, and hotfix process.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["branching"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@git_server.tool(annotations={"readOnlyHint": True})
async def get_code_review_standards(ctx: Context) -> KnowledgeList:
    """Return the code review standards and expectations.

    Covers what reviewers must check, turnaround time expectations, constructive
    feedback guidelines, blocking vs. non-blocking comments, and approval requirements
    before merging.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["code-review"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))
