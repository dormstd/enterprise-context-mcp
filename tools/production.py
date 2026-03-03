"""Production tools — PRO readiness checklist, monitoring, deployment, incident response."""

from __future__ import annotations

from fastmcp import Context, FastMCP

from db import query_entries
from models import KnowledgeEntry, KnowledgeList

production_server = FastMCP("Production")

_CATEGORY = "production_readiness"


@production_server.tool(annotations={"readOnlyHint": True})
async def get_production_checklist(ctx: Context) -> KnowledgeList:
    """Return the full production readiness checklist.

    A comprehensive list of requirements a project must satisfy before it can
    be deployed to the production (PRO) environment. Covers observability,
    security, performance, runbook, support, and compliance criteria.
    """
    db = ctx.lifespan_context["db"]
    lock = ctx.lifespan_context["db_lock"]
    entries = await query_entries(db, lock, category=_CATEGORY, tags=["checklist"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@production_server.tool(annotations={"readOnlyHint": True})
async def get_monitoring_standards(ctx: Context) -> KnowledgeList:
    """Return the observability and monitoring standards for production systems.

    Covers required metrics, log formats, distributed tracing expectations,
    alerting thresholds, SLA/SLO definitions, and approved tooling.
    """
    db = ctx.lifespan_context["db"]
    lock = ctx.lifespan_context["db_lock"]
    entries = await query_entries(db, lock, category=_CATEGORY, tags=["monitoring"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@production_server.tool(annotations={"readOnlyHint": True})
async def get_deployment_process(ctx: Context) -> KnowledgeList:
    """Return the approved deployment process for production releases.

    Covers deployment strategies (canary, blue-green), required approval gates,
    rollback procedures, maintenance windows, and communication protocols
    during and after deployments.
    """
    db = ctx.lifespan_context["db"]
    lock = ctx.lifespan_context["db_lock"]
    entries = await query_entries(db, lock, category=_CATEGORY, tags=["deployment"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))


@production_server.tool(annotations={"readOnlyHint": True})
async def get_incident_response_process(ctx: Context) -> KnowledgeList:
    """Return the incident response and escalation process.

    Covers on-call responsibilities, severity classification, escalation paths,
    communication templates, war-room protocols, post-mortem requirements,
    and SLA obligations for incident resolution times.
    """
    db = ctx.lifespan_context["db"]
    lock = ctx.lifespan_context["db_lock"]
    entries = await query_entries(db, lock, category=_CATEGORY, tags=["incidents"])
    items = [KnowledgeEntry(**e) for e in entries]
    return KnowledgeList(entries=items, total=len(items))
