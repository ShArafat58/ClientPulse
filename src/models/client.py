"""Client data models for ClientPulse."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Client:
    """A freelancer's client, synced from GHL."""

    client_id: str
    name: str
    last_contact_date: Optional[datetime] = None
    next_meeting: Optional[datetime] = None
    open_commitment: Optional[str] = None


@dataclass
class ClientHealth:
    """Computed relationship health for a client."""

    client_id: str
    days_silent: int
    invoice_overdue: bool
    relationship_score: int
    status: str  # "healthy" | "watch" | "needs_attention"
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ClientInsight:
    """AI-generated insight for a client, produced by Strands + Bedrock."""

    client_id: str
    priority: str
    reasons: list[str]
    recommended_action: str
    generated_at: datetime = field(default_factory=datetime.utcnow)