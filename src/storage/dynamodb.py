"""
DynamoDB access layer for ClientPulse.

Single table design:
  PK                   SK
  USER#<user_id>       PROFILE
  CLIENT#<client_id>   PROFILE
  CLIENT#<client_id>   HEALTH
  CLIENT#<client_id>   INSIGHT#LATEST
  CLIENT#<client_id>   NOTE#<timestamp>
  CLIENT#<client_id>   INVOICE#<invoice_id>
  USER#<user_id>       BRIEFING#<date>
"""

import os
from datetime import datetime, timezone
from typing import Any, Optional

import boto3

TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "ClientPulse")

USE_LOCAL = os.environ.get("USE_LOCAL_DYNAMODB", "true").lower() == "true"

if USE_LOCAL:
    _dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://localhost:8001",
        region_name="us-east-1",
        aws_access_key_id="local",
        aws_secret_access_key="local",
    )
else:
    _dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1"))

_table = _dynamodb.Table(TABLE_NAME)


def put_item(pk: str, sk: str, data: dict[str, Any]) -> None:
    """Write an item to the ClientPulse table."""
    item = {"PK": pk, "SK": sk, **data}
    _table.put_item(Item=item)


def get_item(pk: str, sk: str) -> Optional[dict[str, Any]]:
    """Read a single item by PK/SK."""
    response = _table.get_item(Key={"PK": pk, "SK": sk})
    return response.get("Item")


def query_by_pk(pk: str, sk_prefix: Optional[str] = None) -> list[dict[str, Any]]:
    """Query all items under a PK, optionally filtered by SK prefix."""
    if sk_prefix:
        response = _table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
            ExpressionAttributeValues={":pk": pk, ":sk": sk_prefix},
        )
    else:
        response = _table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={":pk": pk},
        )
    return response.get("Items", [])


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