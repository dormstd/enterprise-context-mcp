"""Security tools — policies, compliance requirements, secrets management."""

from __future__ import annotations

from typing import Annotated

from fastmcp import Context, FastMCP
from pydantic import Field

from db import fetch_knowledge
from models import KnowledgeList

security_server = FastMCP("Security")

_CATEGORY = "security"

_VALID_AREAS = ("auth", "data", "api", "secrets", "networking")


@security_server.tool(annotations={"readOnlyHint": True})
async def get_security_policies(
    ctx: Context,
    area: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional area to filter policies. "
                f"Valid values: {', '.join(_VALID_AREAS)}. "
                "Omit to retrieve all security policies."
            ),
        ),
    ] = None,
) -> KnowledgeList:
    """Return the company's security policies.

    Retrieves all security policies, or policies scoped to a specific area:
    auth (authentication & authorisation), data (data classification & handling),
    api (API security standards), secrets (credential management),
    networking (network segmentation & exposure rules).
    """
    tags = ["security"]
    if area:
        tags.append(area)
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=tags)


@security_server.tool(annotations={"readOnlyHint": True})
async def get_compliance_requirements(ctx: Context) -> KnowledgeList:
    """Return the regulatory and compliance obligations that projects must satisfy.

    Covers applicable regulations, audit requirements, data residency rules,
    privacy obligations, and certification maintenance responsibilities.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["compliance"])


@security_server.tool(annotations={"readOnlyHint": True})
async def get_secrets_management_policy(ctx: Context) -> KnowledgeList:
    """Return the company policy for managing secrets.

    Covers approved secret storage solutions (vaults), injection methods,
    rotation schedules, prohibited patterns (e.g. secrets in source code or logs),
    and incident response for exposed credentials.
    """
    return await fetch_knowledge(ctx, category=_CATEGORY, tags=["secrets"])
