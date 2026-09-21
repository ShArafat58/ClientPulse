"""check_invoices MCP tool — unpaid/overdue invoice summary."""

from src.integrations.ghl import get_ghl_provider
from src.integrations.invoices.demo import get_invoice_provider


def check_invoices() -> dict:
    """Return all overdue invoices with client names and amounts."""
    ghl = get_ghl_provider()
    invoices = get_invoice_provider()

    overdue = invoices.get_overdue_invoices()
    client_lookup = {c.client_id: c.name for c in ghl.get_clients()}

    items = [
        {
            "invoice_id": inv.invoice_id,
            "client_name": client_lookup.get(inv.client_id, inv.client_id),
            "amount": inv.amount,
            "currency": inv.currency,
            "due_date": inv.due_date,
        }
        for inv in overdue
    ]

    return {
        "overdue_count": len(items),
        "total_amount": sum(item["amount"] for item in items),
        "invoices": items,
    }