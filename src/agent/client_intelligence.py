"""
Client Intelligence Agent — orchestrates client signal analysis using
AWS Strands + Amazon Bedrock (Nova Micro), with a mock fallback for
local development while Bedrock account access is pending.
"""

import json
import os

from src.agent.prompts import SYSTEM_PROMPT, build_user_prompt
from src.agent.mock_model import MockInsightModel

USE_MOCK_BEDROCK = os.environ.get("USE_MOCK_BEDROCK", "true").lower() == "true"


def _get_real_agent():
    """Lazily construct the real Strands Agent backed by Bedrock Nova Micro."""
    from strands import Agent
    from strands.models import BedrockModel

    model = BedrockModel(
        model_id=os.environ.get("BEDROCK_MODEL_ID", "us.amazon.nova-micro-v1:0"),
        region_name=os.environ.get("AWS_REGION", "ap-southeast-2"),
    )
    return Agent(model=model, system_prompt=SYSTEM_PROMPT)


def generate_client_insight(client_signals: dict) -> dict:
    """
    Given deterministic, rules-scored client signals, produce a structured
    insight: priority, human-readable reasons, and one recommended action.

    client_signals must include: name, days_silent, invoice_overdue,
    open_commitment, meeting_within_24h, score, status.
    """
    if USE_MOCK_BEDROCK:
        return MockInsightModel().generate(client_signals)

    agent = _get_real_agent()
    prompt = build_user_prompt(client_signals)
    response = agent(prompt)

    try:
        return json.loads(str(response))
    except json.JSONDecodeError:
        # Fallback: if the model didn't return clean JSON, degrade gracefully
        return {
            "priority": client_signals["status"],
            "reasons": ["Unable to parse model response"],
            "recommended_action": "Review this client manually.",
        }