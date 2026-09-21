"""record_client_note MCP tool — persist a commitment or note for a client."""

from src.integrations.ghl import get_ghl_provider
from src.storage.dynamodb import save_client_note


def record_client_note(client_id: str, note: str) -> dict:
    """
    Save a note or commitment for a client. Future prep_call calls
    will include this note in their context.
    """
    ghl = get_ghl_provider()
    client = ghl.get_client(client_id)
    if client is None:
        return {"error": f"Client '{client_id}' not found."}

    timestamp = save_client_note(client_id, note)

    return {
        "status": "saved",
        "client_name": client.name,
        "note": note,
        "timestamp": timestamp,
    }