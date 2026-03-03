"""CI/CD tools — pipeline standards, security scanning, quality gates, artifact management."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from db import query_entries
from models import KnowledgeEntry, KnowledgeList

cicd_server = FastMCP("CICD")

_CATEGORY = "cicd"


@cicd_server.tool(annotations={"readOnlyHint": True})
async def get_cicd_pipeline_standards(ctx: Context) -> KnowledgeList:
    """Return the company's CI/CD pipeline standards.

    Covers required pipeline stages, approval gates, environment promotion flow,
    and mandatory checks that every pipeline must include before deploying to production.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["pipeline"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@cicd_server.tool(annotations={"readOnlyHint": True})
async def get_security_scanning_rules(ctx: Context) -> KnowledgeList:
    """Return the security scanning requirements for CI/CD pipelines.

    Covers Veracode SAST/DAST configuration and thresholds, SonarQube quality profiles,
    when scans must run, blocking vs. non-blocking findings, and the exemption process.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["security-scanning"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@cicd_server.tool(annotations={"readOnlyHint": True})
async def get_quality_gate_requirements(ctx: Context) -> KnowledgeList:
    """Return the quality gate requirements that must pass before a release.

    Covers minimum code coverage thresholds, acceptable code smell counts,
    duplication limits, and SonarQube/coverage tool pass/fail criteria.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["quality-gates"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@cicd_server.tool(annotations={"readOnlyHint": True})
async def get_artifact_management_rules(ctx: Context) -> KnowledgeList:
    """Return the rules for artifact publication and management.

    Covers artifact versioning strategy, approved registries, retention policies,
    signing requirements, and promotion rules between environments.
    """
    db = ctx.lifespan_context["db"]
    entries = await query_entries(db, category=_CATEGORY, tags=["artifacts"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))
