"""
ClientPulse background sync worker.

Intended to run on a schedule (EventBridge Scheduler → this Lambda), once
per day. Pulls fresh client and invoice data, recomputes rules-based
relationship scores, generates AI insights via the Client Intelligence
Agent, and caches everything in DynamoDB so Alexa+ MCP tool calls stay
fast (no live GHL or Bedrock calls on the voice request path).
"""

from datetime import datetime, timezone

from src.integrations.ghl import get_ghl_provider
from src.integrations.invoices.demo import get_invoice_provider
from src.scoring.relationship import calculate_relationship_score
from src.agent.client_intelligence import generate_client_insight
from src.storage.store import (
    save_client_health,
    save_insight,
    save_daily_briefing_cache,
)

MAX_CLIENTS = 10  # matches MAX_CLIENTS_IN_DEMO env var, hackathon-scale guard


def sync_and_analyze(user_id: str = "demo") -> dict:
    """
    Run one full background sync cycle: score every client, generate an
    AI insight for each, and cache a daily briefing summary.

    Returns a summary dict (useful for logging / Lambda invocation result).
    """
    ghl = get_ghl_provider()
    invoices = get_invoice_provider()
    now = datetime.now(timezone.utc)

    clients = ghl.get_clients()[:MAX_CLIENTS]
    overdue_invoices = invoices.get_overdue_invoices()
    overdue_client_ids = {inv.client_id for inv in overdue_invoices}

    needs_attention = 0
    upcoming_calls = 0
    top_client = None
    top_score = -1
    processed = []

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

        score = calculate_relationship_score(
            days_silent=days_silent,
            invoice_overdue=invoice_overdue,
            has_open_commitment=has_commitment,
            meeting_within_24h=meeting_soon,
        )

        if score.status == "needs_attention":
            needs_attention += 1
        if score.score > top_score:
            top_score = score.score
            top_client = client.name

        save_client_health(
            client.client_id,
            {
                "days_silent": days_silent,
                "invoice_overdue": invoice_overdue,
                "relationship_score": score.score,
                "status": score.status,
            },
        )

        signals = {
            "name": client.name,
            "days_silent": days_silent,
            "invoice_overdue": invoice_overdue,
            "open_commitment": client.open_commitment,
            "meeting_within_24h": meeting_soon,
            "score": score.score,
            "status": score.status,
        }
        insight = generate_client_insight(signals)
        save_insight(client.client_id, insight)

        processed.append({"client_id": client.client_id, "status": score.status})

    briefing = {
        "needs_attention": needs_attention,
        "overdue_invoices": len(overdue_invoices),
        "upcoming_calls": upcoming_calls,
        "top_client": top_client,
    }
    save_daily_briefing_cache(user_id, now.date().isoformat(), briefing)

    return {"clients_processed": len(processed), "briefing": briefing}


def lambda_handler(event, context):
    """Entry point for the EventBridge-triggered worker Lambda."""
    result = sync_and_analyze()
    return {"statusCode": 200, "body": result}


if __name__ == "__main__":
    print(sync_and_analyze())