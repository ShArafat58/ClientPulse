"""Tests for the Client Intelligence Agent (mock mode)."""

from src.agent.client_intelligence import generate_client_insight


def test_needs_attention_client_gets_high_priority():
    signals = {
        "name": "Acme Design",
        "days_silent": 14,
        "invoice_overdue": True,
        "open_commitment": "Send revised proposal",
        "meeting_within_24h": True,
        "score": 8,
        "status": "needs_attention",
    }
    insight = generate_client_insight(signals)
    assert insight["priority"] == "high"
    assert len(insight["reasons"]) <= 2
    assert "recommended_action" in insight


def test_healthy_client_gets_low_priority():
    signals = {
        "name": "PixelWorks",
        "days_silent": 2,
        "invoice_overdue": False,
        "open_commitment": None,
        "meeting_within_24h": False,
        "score": 0,
        "status": "healthy",
    }
    insight = generate_client_insight(signals)
    assert insight["priority"] == "low"