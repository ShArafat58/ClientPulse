"""Invoice data models for ClientPulse."""

from dataclasses import dataclass


@dataclass
class Invoice:
    """A client invoice (real or demo-provided)."""

    invoice_id: str
    client_id: str
    amount: float
    currency: str
    status: str  # "paid" | "pending" | "overdue"
    due_date: str  # ISO date string