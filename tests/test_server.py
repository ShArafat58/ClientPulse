"""Basic tests for the ClientPulse MCP server."""

import pytest
from fastmcp import Client

from src.server import mcp


@pytest.mark.asyncio
async def test_server_has_daily_briefing_tool():
    """Verify get_daily_briefing tool is registered."""
    async with Client(mcp) as client:
        tools = await client.list_tools()
        tool_names = [t.name for t in tools]
        assert "get_daily_briefing" in tool_names


@pytest.mark.asyncio
async def test_get_daily_briefing_returns_expected_shape():
    """Verify the tool returns the expected dict structure."""
    async with Client(mcp) as client:
        result = await client.call_tool("get_daily_briefing", {})
        data = result.data
        assert "needs_attention" in data
        assert "overdue_invoices" in data
        assert "upcoming_calls" in data
        assert "top_client" in data