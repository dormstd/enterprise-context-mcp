from fastmcp import FastMCP

from db import db_lifespan
from tools.architecture import arch_server
from tools.cicd import cicd_server
from tools.development import dev_server
from tools.git import git_server
from tools.production import production_server
from tools.security import security_server

mcp = FastMCP(
    "Enterprise Context",
    instructions=(
        "This server provides read-only access to enterprise process knowledge. "
        "Use the available tools to retrieve standards, checklists, policies, and "
        "guidelines that apply to all projects. Tools are grouped by domain: "
        "development process, CI/CD, security, production readiness, Git/PR conventions, "
        "and architecture."
    ),
    lifespan=db_lifespan,
)

mcp.mount(dev_server, namespace="dev")
mcp.mount(cicd_server, namespace="cicd")
mcp.mount(security_server, namespace="security")
mcp.mount(production_server, namespace="prod")
mcp.mount(git_server, namespace="git")
mcp.mount(arch_server, namespace="arch")

if __name__ == "__main__":
    mcp.run()