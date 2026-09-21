"""Tests for the GHL provider interface."""

from src.integrations.ghl import get_ghl_provider


def test_get_clients_returns_five_demo_clients():
    provider = get_ghl_provider()
    clients = provider.get_clients()
    assert len(clients) == 5


def test_get_client_by_id():
    provider = get_ghl_provider()
    client = provider.get_client("acme")
    assert client is not None
    assert client.name == "Acme Design"
    assert client.open_commitment == "Send revised proposal"


def test_get_unknown_client_returns_none():
    provider = get_ghl_provider()
    assert provider.get_client("nonexistent") is None