"""
GHL (GoHighLevel) CRM integration for ClientPulse.

Defines a provider interface so the hackathon build can run against
demo data while keeping a clear path to a real GHL adapter.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional


@dataclass
class GHLClientRecord:
    """A client/contact record as returned by a GHL provider."""

    client_id: str
    name: str
    last_contact_date: datetime
    next_meeting: Optional[datetime]
    open_commitment: Optional[str]


class GHLProvider(ABC):
    """Interface any GHL data source must implement."""

    @abstractmethod
    def get_clients(self) -> list[GHLClientRecord]:
        """Return all tracked clients."""

    @abstractmethod
    def get_client(self, client_id: str) -> Optional[GHLClientRecord]:
        """Return a single client by id."""


class DemoGHLProvider(GHLProvider):
    """
    Seeded, deterministic client data for the hackathon demo.

    Replace with RealGHLProvider (GHL REST API + API key) for production use.
    Data is designed to exercise every ClientPulse feature:
    overdue invoice, quiet client, healthy client, and open commitment.
    """

    def __init__(self) -> None:
        now = datetime.now(timezone.utc)
        self._clients = [
            GHLClientRecord(
                client_id="acme",
                name="Acme Design",
                last_contact_date=now - timedelta(days=14),
                next_meeting=now + timedelta(days=1),
                open_commitment="Send revised proposal",
            ),
            GHLClientRecord(
                client_id="northstar",
                name="Northstar",
                last_contact_date=now - timedelta(days=9),
                next_meeting=None,
                open_commitment=None,
            ),
            GHLClientRecord(
                client_id="brightlabs",
                name="BrightLabs",
                last_contact_date=now - timedelta(days=1),
                next_meeting=now + timedelta(hours=5),
                open_commitment=None,
            ),
            GHLClientRecord(
                client_id="pixelworks",
                name="PixelWorks",
                last_contact_date=now - timedelta(days=2),
                next_meeting=None,
                open_commitment=None,
            ),
            GHLClientRecord(
                client_id="atlas",
                name="Atlas",
                last_contact_date=now - timedelta(days=5),
                next_meeting=None,
                open_commitment="Share updated timeline",
            ),
        ]

    def get_clients(self) -> list[GHLClientRecord]:
        return self._clients

    def get_client(self, client_id: str) -> Optional[GHLClientRecord]:
        for client in self._clients:
            if client.client_id == client_id:
                return client
        return None


def get_ghl_provider() -> GHLProvider:
    """
    Factory returning the active GHL provider.

    Hackathon build uses DemoGHLProvider. A RealGHLProvider (GHL REST API,
    api_key-based) can be swapped in here without touching calling code.
    """
    return DemoGHLProvider()