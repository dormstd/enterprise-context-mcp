# enterprise-context-mcp

A read-only [MCP](https://modelcontextprotocol.io/) server built with [FastMCP v3](https://github.com/jlowin/fastmcp) that exposes your company's process knowledge — CI/CD standards, security policies, Git conventions, architecture guidelines, and more — to LLM-powered tools.

Knowledge is stored in a [DuckDB](https://duckdb.org/) file managed by the companion writer service [`enterprise-context-mcp-admin`](https://github.com/dormstd/enterprise-context-mcp-admin). This server only ever opens the database in `READ_ONLY` mode and can run as many replicas as needed.

---

## Overview

```
┌─────────────────────────────────┐      ┌───────────────────────────┐
│  enterprise-context-mcp-admin   │      │   enterprise-context-mcp  │
│  (FastAPI  ·  READ_WRITE)       │─────▶│   (FastMCP  ·  READ_ONLY) │
│  replicas: 1                    │  DB  │   replicas: N             │
└─────────────────────────────────┘      └───────────────────────────┘
              │                                        │
              └──────────────┐ ┌─────────────────────┘
                             ▼ ▼
                      enterprise.duckdb
                      (shared PVC / file)
```

LLMs connect to this MCP server and call tools to retrieve guidelines relevant to the task at hand. All tools carry `readOnlyHint: true` — no data is ever modified through this server.

---

## Features

- **19 read-only tools** across 6 knowledge domains
- **Namespaced sub-servers** — tools are grouped and prefixed by domain (`dev_`, `cicd_`, `security_`, `prod_`, `git_`, `arch_`)
- **Flexible queries** — filter entries by category, role, tags, or free-text search
- **Read-only by design** — DuckDB opened with `read_only=True`; safe to scale horizontally
- **Zero schema ownership** — schema and seed data live in the admin service

---

## Tech Stack

| Component | Version |
|-----------|---------|
| Python    | 3.13    |
| FastMCP   | ≥ 3.0.2 |
| DuckDB    | ≥ 1.2.0 |
| UV        | package manager |

---

## Project Structure

```
enterprise-context-mcp/
├── main.py          # FastMCP app, mounts all 6 sub-servers
├── db.py            # READ_ONLY DuckDB lifespan + query_entries() helper
├── models.py        # KnowledgeEntry, KnowledgeList Pydantic models
└── tools/
    ├── development.py   # dev_server  (namespace: dev)
    ├── cicd.py          # cicd_server (namespace: cicd)
    ├── security.py      # security_server (namespace: security)
    ├── production.py    # production_server (namespace: prod)
    ├── git.py           # git_server  (namespace: git)
    └── architecture.py  # arch_server (namespace: arch)
```

---

## Getting Started

### Prerequisites

- [UV](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- A populated `enterprise.duckdb` file (created by [`enterprise-context-mcp-admin`](https://github.com/dormstd/enterprise-context-mcp-admin))

### Install dependencies

```bash
uv sync
```

### Run as an MCP server (http transport)

```bash
ENTERPRISE_DB_PATH=/path/to/enterprise.duckdb uv run fastmcp run main.py:mcp --transport http --port 8000
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENTERPRISE_DB_PATH` | `./enterprise.duckdb` | Absolute or relative path to the DuckDB file |

> In Kubernetes, set this to the mount path of the shared PVC so both the admin and MCP reader services access the same file.

---

## Tools Reference

All tools return a `KnowledgeList` containing a list of `KnowledgeEntry` objects and a total count.

### `dev` — Development Process

| Tool | Description |
|------|-------------|
| `dev_get_development_standards` | General coding standards, naming conventions, and quality expectations |
| `dev_get_new_project_checklist` | Checklist for bootstrapping a new project (repo, CI/CD, security, observability) |
| `dev_get_dependency_management_policy` | Dependency approval process, version pinning, and approved registries |

### `cicd` — CI/CD

| Tool | Description |
|------|-------------|
| `cicd_get_cicd_pipeline_standards` | Required pipeline stages, approval gates, and environment promotion flow |
| `cicd_get_security_scanning_rules` | SAST/DAST configuration, SonarQube thresholds, blocking vs. non-blocking findings |
| `cicd_get_quality_gate_requirements` | Coverage thresholds, code smell limits, and pass/fail criteria |
| `cicd_get_artifact_management_rules` | Artifact versioning, approved registries, retention policies, and signing |

### `security` — Security

| Tool | Description |
|------|-------------|
| `security_get_security_policies` | All security policies, optionally filtered by `area` (`auth`, `data`, `api`, `secrets`, `networking`) |
| `security_get_compliance_requirements` | Regulatory obligations, audit requirements, and data residency rules |
| `security_get_secrets_management_policy` | Approved vaults, rotation schedules, and prohibited patterns |

### `prod` — Production Readiness

| Tool | Description |
|------|-------------|
| `prod_get_production_checklist` | Full PRO readiness checklist (observability, security, performance, runbook) |
| `prod_get_monitoring_standards` | Required metrics, log formats, alerting thresholds, and approved tooling |
| `prod_get_deployment_process` | Deployment strategies, approval gates, rollback procedures, and maintenance windows |
| `prod_get_incident_response_process` | Severity classification, escalation paths, post-mortem requirements |

### `git` — Git & PR

| Tool | Description |
|------|-------------|
| `git_get_pr_conventions` | PR title format, description template, minimum approvals, and merge strategy |
| `git_get_branching_strategy` | Flow model, branch naming patterns, protected branches, and hotfix process |
| `git_get_code_review_standards` | Reviewer expectations, turnaround times, and comment guidelines |

### `arch` — Architecture

| Tool | Description |
|------|-------------|
| `arch_get_architecture_guidelines` | Approved patterns, ADR requirements, and the architecture review process |
| `arch_get_tech_radar` | Technologies classified as Adopt / Trial / Assess / Hold |

---

## Deployment (Kubernetes)

```yaml
spec:
  replicas: 3   # scale freely — READ_ONLY
  containers:
    - name: mcp
      env:
        - name: ENTERPRISE_DB_PATH
          value: /data/enterprise.duckdb
      volumeMounts:
        - name: db-storage
          mountPath: /data
```

Both the admin and MCP reader deployments must mount the same PVC at the path pointed to by `ENTERPRISE_DB_PATH`.

---

## Using with an LLM Client

Add the server to your MCP client configuration (e.g. Claude Desktop):
```json
"enterprise-context-mcp": {
    "type": "http",
    "url": "http://localhost:8000/mcp"
}
```

---

## Related

- [`enterprise-context-mcp-admin`](https://github.com/dormstd/enterprise-context-mcp-admin) — the FastAPI write service that manages schema, CRUD, and seeding


## ToDo

- Authentication mechanisms


## License

MIT
