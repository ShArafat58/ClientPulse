"""
Mock model for local development while AWS Bedrock account access is
pending. Returns deterministic, realistic responses so the rest of the
pipeline (Strands Agent orchestration, DynamoDB caching) can be built
and tested end-to-end without a live Bedrock call.

Swap MockInsightModel for the real Bedrock-backed Strands Agent by
setting USE_MOCK_BEDROCK=false once model access is confirmed.
"""

import json


class MockInsightModel:
    """Drop-in stand-in for the Strands+Bedrock call during development."""

    def generate(self, client_signals: dict) -> dict:
        days_silent = client_signals["days_silent"]
        invoice_overdue = client_signals["invoice_overdue"]
        commitment = client_signals.get("open_commitment")
        meeting_soon = client_signals["meeting_within_24h"]

        reasons = []
        if days_silent >= 14:
            reasons.append(f"No communication for {days_silent} days")
        elif days_silent >= 7:
            reasons.append(f"Contact has gone quiet for {days_silent} days")
        if invoice_overdue:
            reasons.append("Invoice is overdue")
        if commitment:
            reasons.append(f"Open commitment: {commitment}")
        if meeting_soon:
            reasons.append("Meeting scheduled within 24 hours")
        if not reasons:
            reasons.append("No urgent signals detected")

        status = client_signals["status"]
        priority = "high" if status == "needs_attention" else "medium" if status == "watch" else "low"

        if invoice_overdue and meeting_soon:
            action = "Confirm the invoice status and any open items during the upcoming call."
        elif commitment:
            action = f"Follow up on: {commitment}"
        elif days_silent >= 14:
            action = "Send a short check-in message to re-open the conversation."
        else:
            action = "No action needed right now — relationship is healthy."

        return {
            "priority": priority,
            "reasons": reasons[:2],
            "recommended_action": action,
        }