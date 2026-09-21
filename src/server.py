"""
ClientPulse MCP Server
Entry point for the FastMCP server exposing ClientPulse tools to Alexa+.

MCP spec: 2025-11-25+
Transport: Streamable HTTP
"""

from fastmcp import FastMCP

from src.tools.daily_briefing import get_daily_briefing as _get_daily_briefing
from src.tools.prep_call import prep_call as _prep_call
from src.tools.invoices import check_invoices as _check_invoices
from src.tools.stale_clients import list_stale_clients as _list_stale_clients
from src.tools.notes import record_client_note as _record_client_note

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
    """Return today's client briefing: attention items, overdue invoices, upcoming calls."""
    return _get_daily_briefing()


@mcp.tool()
def prep_call(client_id: str) -> dict:
    """Return call-prep context for a client: last contact, invoices, commitments, notes."""
    return _prep_call(client_id)


@mcp.tool()
def check_invoices() -> dict:
    """Return all overdue invoices with client names and amounts."""
    return _check_invoices()


@mcp.tool()
def list_stale_clients() -> dict:
    """Return clients with no meaningful contact in 7+ days."""
    return _list_stale_clients()


@mcp.tool()
def record_client_note(client_id: str, note: str) -> dict:
    """Save a note or commitment for a client, remembered for future call prep."""
    return _record_client_note(client_id, note)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)