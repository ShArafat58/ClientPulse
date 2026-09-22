"""prep_call MCP tool — call preparation context for a specific client."""

from datetime import datetime, timezone

from src.integrations.ghl import get_ghl_provider
from src.integrations.invoices.demo import get_invoice_provider
from src.scoring.relationship import calculate_relationship_score
from src.storage.store import get_client_notes, get_latest_insight, save_insight
from src.agent.client_intelligence import generate_client_insight


def prep_call(client_id: str) -> dict:
    """
    Return call-prep context for a client: last interaction, invoice
    status, open commitments, relationship health, recorded notes, and
    an AI-generated priority insight with a recommended next action.
    """
    ghl = get_ghl_provider()
    invoices = get_invoice_provider()
    now = datetime.now(timezone.utc)

    client = ghl.get_client(client_id)
    if client is None:
        return {"error": f"Client '{client_id}' not found."}

    client_invoices = invoices.get_invoices_for_client(client_id)
    invoice_overdue = any(inv.status == "overdue" for inv in client_invoices)
    days_silent = (now - client.last_contact_date).days
    meeting_soon = (
        client.next_meeting is not None
        and (client.next_meeting - now).total_seconds() <= 86400
    )

    score = calculate_relationship_score(
        days_silent=days_silent,
        invoice_overdue=invoice_overdue,
        has_open_commitment=client.open_commitment is not None,
        meeting_within_24h=meeting_soon,
    )

    notes = get_client_notes(client_id)
    recent_notes = [n["note"] for n in notes[-3:]] if notes else []

    # Generate (or reuse cached) AI insight — explanation and next-action only,
    # never the priority score itself, which is computed deterministically above.
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
    save_insight(client_id, insight)

    return {
        "client_name": client.name,
        "days_since_last_contact": days_silent,
        "open_commitment": client.open_commitment,
        "invoice_status": "overdue" if invoice_overdue else "current",
        "invoice_amounts": [
            {"id": inv.invoice_id, "amount": inv.amount, "status": inv.status}
            for inv in client_invoices
        ],
        "relationship_status": score.status,
        "next_meeting": client.next_meeting.isoformat() if client.next_meeting else None,
        "recent_notes": recent_notes,
        "ai_insight": {
            "priority": insight["priority"],
            "reasons": insight["reasons"],
            "recommended_action": insight["recommended_action"],
        },
    }