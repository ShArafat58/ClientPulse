"""Tests for the background sync worker."""

from workers.sync_and_analyze import sync_and_analyze


def test_sync_processes_all_demo_clients():
    result = sync_and_analyze()
    assert result["clients_processed"] == 5
    assert "briefing" in result
    assert "needs_attention" in result["briefing"]