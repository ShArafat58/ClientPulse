"""list_stale_clients MCP tool — clients who have gone quiet."""

from datetime import datetime, timezone

from src.integrations.ghl import get_ghl_provider

STALE_THRESHOLD_DAYS = 7


def list_stale_clients() -> dict:
    """Return clients with no meaningful contact in 7+ days, with reasons."""
    ghl = get_ghl_provider()
    now = datetime.now(timezone.utc)

    stale = []
    for client in ghl.get_clients():
        days_silent = (now - client.last_contact_date).days
        if days_silent >= STALE_THRESHOLD_DAYS:
            stale.append(
                {
                    "client_name": client.name,
                    "days_silent": days_silent,
                    "open_commitment": client.open_commitment,
                }
            )

    stale.sort(key=lambda c: c["days_silent"], reverse=True)

    return {"stale_count": len(stale), "clients": stale}