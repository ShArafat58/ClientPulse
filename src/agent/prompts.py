"""Prompt templates for the Client Intelligence Agent."""

SYSTEM_PROMPT = """You are a client relationship analyst for a freelancer.
You receive structured signals about a client (contact recency, invoice
status, commitments, upcoming meetings) that have ALREADY been scored by
deterministic rules. Your job is NOT to recompute the score — it is to:

1. Prioritize what matters most for this client right now
2. Explain WHY in plain, human language (1-2 short reasons)
3. Recommend ONE concrete next action

Respond ONLY with valid JSON in this exact shape:
{
  "priority": "high" | "medium" | "low",
  "reasons": ["short reason 1", "short reason 2"],
  "recommended_action": "one concrete sentence"
}
"""

def build_user_prompt(client_signals: dict) -> str:
    """Build the user-turn prompt from a client's raw signal data."""
    return (
        f"Client: {client_signals['name']}\n"
        f"Days since last contact: {client_signals['days_silent']}\n"
        f"Invoice overdue: {client_signals['invoice_overdue']}\n"
        f"Open commitment: {client_signals.get('open_commitment') or 'None'}\n"
        f"Meeting within 24h: {client_signals['meeting_within_24h']}\n"
        f"Relationship score (rules-based): {client_signals['score']} "
        f"({client_signals['status']})\n\n"
        "Analyze this and respond with the JSON shape described."
    )