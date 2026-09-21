"""Invoice provider interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class InvoiceRecord:
    invoice_id: str
    client_id: str
    amount: float
    currency: str
    status: str  # "paid" | "pending" | "overdue"
    due_date: str  # ISO date string


class InvoiceProvider(ABC):
    """Interface any invoicing data source must implement."""

    @abstractmethod
    def get_invoices(self) -> list[InvoiceRecord]:
        """Return all invoices."""

    @abstractmethod
    def get_invoices_for_client(self, client_id: str) -> list[InvoiceRecord]:
        """Return invoices for a specific client."""

    @abstractmethod
    def get_overdue_invoices(self) -> list[InvoiceRecord]:
        """Return all overdue invoices."""