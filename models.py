"""Pydantic response models for the Enterprise Context MCP server."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class KnowledgeEntry(BaseModel):
    id: int
    title: str
    content: str
    category: str
    category_description: str | None = None
    tags: list[str] = []
    target_roles: list[str] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Category(BaseModel):
    id: int
    name: str
    description: str | None = None


class KnowledgeList(BaseModel):
    entries: list[KnowledgeEntry]
    total: int
