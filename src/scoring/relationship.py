"""
Rules-based relationship health scoring.

Deterministic scoring — no AI/LLM involved here. Bedrock is used later
only to explain and prioritize these scores, not to compute them.
"""

from dataclasses import dataclass


@dataclass
class RelationshipScore:
    score: int
    status: str  # "healthy" | "watch" | "needs_attention"


def calculate_relationship_score(
    days_silent: int,
    invoice_overdue: bool,
    has_open_commitment: bool,
    meeting_within_24h: bool,
) -> RelationshipScore:
    """Calculate a client's relationship health score from raw signals."""
    score = 0

    if days_silent >= 30:
        score += 5
    elif days_silent >= 14:
        score += 3
    elif days_silent >= 7:
        score += 1

    if invoice_overdue:
        score += 2

    if has_open_commitment:
        score += 2

    if meeting_within_24h:
        score += 1

    if score == 0:
        status = "healthy"
    elif score <= 3:
        status = "watch"
    else:
        status = "needs_attention"

    return RelationshipScore(score=score, status=status)