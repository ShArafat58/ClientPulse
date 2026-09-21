"""Tests for rules-based relationship scoring."""

from src.scoring.relationship import calculate_relationship_score


def test_healthy_client_scores_low():
    result = calculate_relationship_score(
        days_silent=2, invoice_overdue=False, has_open_commitment=False, meeting_within_24h=False
    )
    assert result.status == "healthy"


def test_needs_attention_when_quiet_and_overdue():
    result = calculate_relationship_score(
        days_silent=14, invoice_overdue=True, has_open_commitment=True, meeting_within_24h=True
    )
    assert result.status == "needs_attention"
    assert result.score == 8


def test_watch_status_mid_range():
    result = calculate_relationship_score(
        days_silent=9, invoice_overdue=False, has_open_commitment=False, meeting_within_24h=False
    )
    assert result.status == "watch"