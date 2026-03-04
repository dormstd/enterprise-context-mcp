"""Git process tools — PR conventions, branching strategy, code review standards."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from db import fetch_knowledge
from models import KnowledgeList

git_server = FastMCP("Git")

_CATEGORY = "git_pr"


@git_server.tool(annotations={"readOnlyHint": True})
async def get_pr_conventions(ctx: Context) -> KnowledgeList:
    """Return the company's pull request conventions.

    Covers required PR title format, description template, linked ticket requirements,
    review assignment rules, minimum approvals, and merge strategy (squash, rebase, merge).
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["pull-requests"])


@git_server.tool(annotations={"readOnlyHint": True})
async def get_branching_strategy(ctx: Context) -> KnowledgeList:
    """Return the company's branching strategy and naming conventions.

    Covers the adopted flow model (trunk-based, gitflow, etc.), branch naming
    patterns, protected branch rules, release branch lifecycle, and hotfix process.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["branching"])


@git_server.tool(annotations={"readOnlyHint": True})
async def get_code_review_standards(ctx: Context) -> KnowledgeList:
    """Return the code review standards and expectations.

    Covers what reviewers must check, turnaround time expectations, constructive
    feedback guidelines, blocking vs. non-blocking comments, and approval requirements
    before merging.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["code-review"])
