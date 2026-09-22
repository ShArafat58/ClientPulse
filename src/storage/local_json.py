"""
Local JSON-file storage backend for ClientPulse.

Drop-in replacement for the DynamoDB storage layer, using the same
function signatures, so the rest of the codebase (tools, workers) needs
no changes. Data persists to a single JSON file on disk.

This lets the full product run and demo without any AWS dependency,
while keeping the DynamoDB-based implementation (src/storage/dynamodb.py)
as the production path once AWS access is available.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

DATA_FILE = Path(os.environ.get("LOCAL_STORAGE_FILE", "data/local_store.json"))


def _load() -> dict:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


def _key(pk: str, sk: str) -> str:
    return f"{pk}|{sk}"


def put_item(pk: str, sk: str, data: dict[str, Any]) -> None:
    store = _load()
    store[_key(pk, sk)] = {"PK": pk, "SK": sk, **data}
    _save(store)


def get_item(pk: str, sk: str) -> Optional[dict[str, Any]]:
    store = _load()
    return store.get(_key(pk, sk))


def query_by_pk(pk: str, sk_prefix: Optional[str] = None) -> list[dict[str, Any]]:
    store = _load()
    items = [v for k, v in store.items() if v["PK"] == pk]
    if sk_prefix:
        items = [v for v in items if v["SK"].startswith(sk_prefix)]
    return items


def get_client_health(client_id: str) -> Optional[dict[str, Any]]:
    return get_item(f"CLIENT#{client_id}", "HEALTH")


def save_client_health(client_id: str, health_data: dict[str, Any]) -> None:
    health_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    put_item(f"CLIENT#{client_id}", "HEALTH", health_data)


def get_client_note(client_id: str, timestamp: str) -> Optional[dict[str, Any]]:
    return get_item(f"CLIENT#{client_id}", f"NOTE#{timestamp}")


def save_client_note(client_id: str, note: str) -> str:
    timestamp = datetime.now(timezone.utc).isoformat()
    put_item(f"CLIENT#{client_id}", f"NOTE#{timestamp}", {"note": note})
    return timestamp


def get_client_notes(client_id: str) -> list[dict[str, Any]]:
    return query_by_pk(f"CLIENT#{client_id}", "NOTE#")


def get_latest_insight(client_id: str) -> Optional[dict[str, Any]]:
    return get_item(f"CLIENT#{client_id}", "INSIGHT#LATEST")


def save_insight(client_id: str, insight_data: dict[str, Any]) -> None:
    put_item(f"CLIENT#{client_id}", "INSIGHT#LATEST", insight_data)


def get_daily_briefing_cache(user_id: str, date: str) -> Optional[dict[str, Any]]:
    return get_item(f"USER#{user_id}", f"BRIEFING#{date}")


def save_daily_briefing_cache(user_id: str, date: str, briefing_data: dict[str, Any]) -> None:
    put_item(f"USER#{user_id}", f"BRIEFING#{date}", briefing_data)