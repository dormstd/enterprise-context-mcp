"""CI/CD tools — pipeline standards, security scanning, quality gates, artifact management."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from db import fetch_knowledge
from models import KnowledgeList

cicd_server = FastMCP("CICD")

_CATEGORY = "cicd"


@cicd_server.tool(annotations={"readOnlyHint": True})
async def get_cicd_pipeline_standards(ctx: Context) -> KnowledgeList:
    """Return the company's CI/CD pipeline standards.

    Covers required pipeline stages, approval gates, environment promotion flow,
    and mandatory checks that every pipeline must include before deploying to production.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["pipeline"])


@cicd_server.tool(annotations={"readOnlyHint": True})
async def get_security_scanning_rules(ctx: Context) -> KnowledgeList:
    """Return the security scanning requirements for CI/CD pipelines.

    Covers Veracode SAST/DAST configuration and thresholds, SonarQube quality profiles,
    when scans must run, blocking vs. non-blocking findings, and the exemption process.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["security-scanning"])


@cicd_server.tool(annotations={"readOnlyHint": True})
async def get_quality_gate_requirements(ctx: Context) -> KnowledgeList:
    """Return the quality gate requirements that must pass before a release.

    Covers minimum code coverage thresholds, acceptable code smell counts,
    duplication limits, and SonarQube/coverage tool pass/fail criteria.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["quality-gates"])


@cicd_server.tool(annotations={"readOnlyHint": True})
async def get_artifact_management_rules(ctx: Context) -> KnowledgeList:
    """Return the rules for artifact publication and management.

    Covers artifact versioning strategy, approved registries, retention policies,
    signing requirements, and promotion rules between environments.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["artifacts"])
