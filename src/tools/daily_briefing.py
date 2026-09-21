"""get_daily_briefing MCP tool — today's client overview."""

from datetime import datetime, timezone

from src.integrations.ghl import get_ghl_provider
from src.integrations.invoices.demo import get_invoice_provider
from src.scoring.relationship import calculate_relationship_score


def get_daily_briefing() -> dict:
    """
    Return today's client briefing: number of clients needing attention,
    overdue invoices, and upcoming calls.
    """
    ghl = get_ghl_provider()
    invoices = get_invoice_provider()
    now = datetime.now(timezone.utc)

    clients = ghl.get_clients()
    overdue_invoices = invoices.get_overdue_invoices()
    overdue_client_ids = {inv.client_id for inv in overdue_invoices}

    needs_attention = 0
    upcoming_calls = 0
    top_client = None
    top_score = -1

    for client in clients:
        days_silent = (now - client.last_contact_date).days
        invoice_overdue = client.client_id in overdue_client_ids
        has_commitment = client.open_commitment is not None
        meeting_soon = (
            client.next_meeting is not None
            and (client.next_meeting - now).total_seconds() <= 86400
        )

        if client.next_meeting is not None:
            upcoming_calls += 1

        result = calculate_relationship_score(
            days_silent=days_silent,
            invoice_overdue=invoice_overdue,
            has_open_commitment=has_commitment,
            meeting_within_24h=meeting_soon,
        )

        if result.status == "needs_attention":
            needs_attention += 1

        if result.score > top_score:
            top_score = result.score
            top_client = client.name

    return {
        "needs_attention": needs_attention,
        "overdue_invoices": len(overdue_invoices),
        "upcoming_calls": upcoming_calls,
        "top_client": top_client,
    }