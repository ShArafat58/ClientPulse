"""Tests for the DynamoDB storage layer (runs against DynamoDB Local)."""

import pytest

from src.storage import dynamodb


def test_save_and_get_client_health():
    dynamodb.save_client_health(
        "acme",
        {
            "days_silent": 14,
            "invoice_overdue": True,
            "relationship_score": 7,
            "status": "needs_attention",
        },
    )
    health = dynamodb.get_client_health("acme")
    assert health is not None
    assert health["status"] == "needs_attention"
    assert health["days_silent"] == 14


def test_save_and_get_client_note():
    timestamp = dynamodb.save_client_note("acme", "Send revised proposal Friday")
    note = dynamodb.get_client_note("acme", timestamp)
    assert note is not None
    assert note["note"] == "Send revised proposal Friday"


def test_get_client_notes_returns_list():
    dynamodb.save_client_note("acme", "Follow up next week")
    notes = dynamodb.get_client_notes("acme")
    assert isinstance(notes, list)
    assert len(notes) >= 1


def test_save_and_get_insight():
    dynamodb.save_insight(
        "acme",
        {
            "priority": "high",
            "reasons": ["No contact for 14 days", "Invoice overdue"],
            "recommended_action": "Confirm invoice during next call",
        },
    )
    insight = dynamodb.get_latest_insight("acme")
    assert insight is not None
    assert insight["priority"] == "high"