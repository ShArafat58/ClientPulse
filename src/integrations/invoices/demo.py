"""
Seeded demo invoice data for the hackathon build.

Production adapters can implement InvoiceProvider against Stripe,
QuickBooks, or GHL invoicing without changing calling code.
"""

from .base import InvoiceProvider, InvoiceRecord


class DemoInvoiceProvider(InvoiceProvider):
    def __init__(self) -> None:
        self._invoices = [
            InvoiceRecord(
                invoice_id="INV-001",
                client_id="acme",
                amount=1250.00,
                currency="USD",
                status="overdue",
                due_date="2026-10-15",
            ),
            InvoiceRecord(
                invoice_id="INV-002",
                client_id="brightlabs",
                amount=800.00,
                currency="USD",
                status="paid",
                due_date="2026-09-01",
            ),
            InvoiceRecord(
                invoice_id="INV-003",
                client_id="atlas",
                amount=450.00,
                currency="USD",
                status="pending",
                due_date="2026-10-25",
            ),
        ]

    def get_invoices(self) -> list[InvoiceRecord]:
        return self._invoices

    def get_invoices_for_client(self, client_id: str) -> list[InvoiceRecord]:
        return [inv for inv in self._invoices if inv.client_id == client_id]

    def get_overdue_invoices(self) -> list[InvoiceRecord]:
        return [inv for inv in self._invoices if inv.status == "overdue"]


def get_invoice_provider() -> InvoiceProvider:
    """Factory returning the active invoice provider."""
    return DemoInvoiceProvider()