# ClientPulse — Demo Video Script (Target: <2:50)

## 0:00–0:15 — Hook (best material first)
**Visual:** MCP Inspector or Alexa+ simulator screen, briefing card visible
**Voice/Alexa:**
> "Alexa, ask ClientPulse what needs my attention today."

**Response:**
> "Two clients need attention. Acme Design has been quiet for 14 days
> and has a $1,250 overdue invoice."

**Screen:** Briefing Card appears (gradient card, Acme Design + Northstar)

---

## 0:15–0:40 — Call prep
**Voice:**
> "Prep me for my call with Acme."

**Response:**
> "Your last conversation was two weeks ago. You promised a revised
> proposal. Their invoice is overdue, and your next call is tomorrow.
> Confirm the invoice status and the proposal during the call."

**Screen:** `prep_call` JSON result, highlight the `ai_insight` block

---

## 0:40–1:00 — Stale relationship detection
**Voice:**
> "Which clients have gone quiet?"

**Screen:** `list_stale_clients` result — Acme (14 days), Northstar (9 days)

---

## 1:00–1:20 — Persistent memory (key differentiator)
**Voice:**
> "Remember that I promised Acme the revised proposal Friday."

**Then:**
> "Prep me for Acme."

**Screen:** New commitment appears in `recent_notes` — proves state
persists across calls, not just single-turn Q&A

---

## 1:20–1:45 — Architecture reveal
**Screen:** Architecture diagram (from README)
**Voice-over (narrator, not Alexa):**
> "ClientPulse separates background intelligence from the live voice
> path. GHL and invoice data feed a rules-based scoring engine, then
> an AWS Strands agent and Amazon Bedrock generate a plain-language
> insight — cached in DynamoDB so Alexa+ gets a fast, low-latency
> response every time."

---

## 1:45–2:05 — MCP proof
**Screen:** Code editor, `src/server.py`
```python
from fastmcp import FastMCP
mcp = FastMCP(name="ClientPulse", ...)
```
**Screen:** MCP Inspector, "Connected — MCP 2025-11-25" visible

**Voice-over:**
> "ClientPulse is a real, self-hosted MCP server — spec 2025-11-25,
> Streamable HTTP — verified end-to-end with the official MCP Inspector."

---

## 2:05–2:25 — AWS Builder proof
**Screen:** Code editor, `src/agent/client_intelligence.py`
```python
from strands import Agent
from strands.models import BedrockModel
```
**Screen:** AWS Console — DynamoDB table, Cognito User Pool

**Voice-over:**
> "On AWS: Amazon Bedrock's Nova Micro model powers the reasoning,
> orchestrated through the AWS Strands Agents SDK. DynamoDB holds
> persistent client memory, and Cognito handles OAuth 2.1 account
> linking for Alexa+."

---

## 2:25–2:45 — Impact
**Voice-over:**
> "Freelancers rarely lose clients because they lack a CRM — they lose
> them because signals get lost across tools. ClientPulse turns those
> signals into the one next action that matters, before the
> relationship goes cold."

---

## 2:45–2:55 — Close
**Screen:** ClientPulse logo/title card
**Voice-over:**
> "ClientPulse. Built for Alexa+. Built on AWS."

---

## Production Notes
- Record actual MCP Inspector interactions (already verified working)
  rather than mocking the UI — authenticity matters for judges
- If live Alexa+ device access isn't available by recording time, use
  MCP Inspector as the "MCP client" and narrate that this is the
  standard way to verify an MCP server pre-Alexa+ integration
- Keep captions/text overlays for the JSON responses — judges skim fast
- Background music: subtle, non-distracting (freesound.org / YouTube
  Audio Library, royalty-free)