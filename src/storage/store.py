"""
Storage backend switcher.

Set STORAGE_BACKEND=dynamodb to use AWS DynamoDB (requires AWS access),
or STORAGE_BACKEND=local (default) to use local JSON file storage —
no AWS account needed. Both backends expose identical function
signatures, so calling code never needs to know which is active.
"""

import os

_BACKEND = os.environ.get("STORAGE_BACKEND", "local").lower()

if _BACKEND == "dynamodb":
    from src.storage.dynamodb import (
        get_client_health,
        save_client_health,
        get_client_note,
        save_client_note,
        get_client_notes,
        get_latest_insight,
        save_insight,
        get_daily_briefing_cache,
        save_daily_briefing_cache,
    )
else:
    from src.storage.local_json import (
        get_client_health,
        save_client_health,
        get_client_note,
        save_client_note,
        get_client_notes,
        get_latest_insight,
        save_insight,
        get_daily_briefing_cache,
        save_daily_briefing_cache,
    )