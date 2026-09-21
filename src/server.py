"""
ClientPulse MCP Server
Entry point for the FastMCP server exposing ClientPulse tools to Alexa+.

MCP spec: 2025-11-25+
Transport: Streamable HTTP
"""

from fastmcp import FastMCP

mcp = FastMCP(
    name="ClientPulse",
    instructions=(
        "ClientPulse helps freelancers and agencies stay on top of "
        "their clients: daily briefings, call prep, invoice tracking, "
        "and stale-relationship detection."
    ),
)


@mcp.tool()
def get_daily_briefing() -> dict:
    """
    Return today's client briefing: number of clients needing attention,
    overdue invoices, and upcoming calls.

    This is a placeholder for Week 1 MCP proof. Real logic (DynamoDB read)
    comes in Week 2.
    """
    return {
        "needs_attention": 2,
        "overdue_invoices": 1,
        "upcoming_calls": 2,
        "top_client": "Acme Design",
    }


if __name__ == "__main__":
    # Streamable HTTP transport, required by Alexa+ MCP Toolkit
    mcp.run(transport="http", host="0.0.0.0", port=8000)