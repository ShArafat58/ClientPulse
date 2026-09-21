# ClientPulse

Juggling dozens of clients? ClientPulse gives you a morning briefing, preps every call, and warns you when a client's gone quiet, right through Alexa+.

## Status
🚧 In development — Amazon Developer Hackathon 2026 (Alexa+ Track + AWS Builder mini-challenge)

## Why ClientPulse
Freelancers rarely lose clients because they lack a CRM. They lose them because
important signals — CRM notes, invoices, meetings, commitments — are scattered
across tools and easy to miss. ClientPulse turns those scattered signals into
the one next action a freelancer needs to take, voice-first, through Alexa+.

## What It Does
- **Daily briefing** — what needs your attention today, in one glance
- **Call prep** — instant context before any client call, plus an AI-generated
  priority explanation and recommended next action
- **Invoice tracking** — never miss an overdue payment
- **Stale client detection** — spot relationships going quiet before they go cold
- **Persistent memory** — remembers commitments and notes across sessions

## Architecture
                BACKGROUND (precomputed, not on the voice request path)

GHL + Invoice data → Rules-based relationship scoring → Strands Agent
→ Amazon Bedrock (Nova Micro) → Client insight → DynamoDB (cached)

                RUNTIME (fast path, <500ms target for Alexa+)

Alexa+ → FastMCP (Streamable HTTP) → DynamoDB read → Structured response
→ Alexa+ voice response + MCP App visual card


This separation is the core technical decision behind ClientPulse: Alexa+ MCP
requests read pre-scored, pre-cached data instead of calling an LLM live,
keeping latency low while still delivering AI-generated insight.

## Alexa+ MCP Implementation
- MCP spec: 2025-11-25+
- Transport: Streamable HTTP
- Server: Python + [FastMCP](https://gofastmcp.com)
- Verified end-to-end with the official MCP Inspector (5 tools, all
  discoverable and callable)

```python
from fastmcp import FastMCP

mcp = FastMCP(name="ClientPulse", ...)

@mcp.tool()
def prep_call(client_id: str) -> dict:
    ...
```

## AWS Builder Integration
- **Amazon Bedrock** (Nova Micro) — client insight generation: prioritization,
  plain-language explanation, and one recommended next action. The model
  never computes the priority score itself — that's deterministic, rules-based
  scoring (see `src/scoring/relationship.py`) — the model only explains and
  prioritizes.
- **AWS Strands Agents SDK** — orchestrates the client-intelligence pipeline
  (`src/agent/client_intelligence.py`)
- **Amazon DynamoDB** — persistent client memory (health scores, notes,
  cached insights, daily briefings), single-table design
- **AWS Lambda** — MCP server hosting, container-based deployment with
  AWS Lambda Web Adapter for Streamable HTTP support
- **Amazon Cognito** — OAuth 2.1 (client_credentials grant) for MCP
  service-level authentication, verified end-to-end

## Agentic Workflow
Rather than a single LLM call, ClientPulse separates deterministic logic from
AI reasoning:
- **Python (rules)**: days-silent calculation, invoice-overdue check,
  meeting-proximity check, relationship score
- **Bedrock (via Strands)**: turns those signals into a human-readable
  explanation and one concrete recommended action

This keeps cost and latency low, avoids hallucinated priority scores, and
keeps every recommendation explainable and auditable.

## MCP Tools

| Tool | Description |
|---|---|
| `get_daily_briefing()` | Today's overview: clients needing attention, overdue invoices, upcoming calls |
| `prep_call(client_id)` | Full call-prep context + AI-generated insight |
| `check_invoices()` | All overdue invoices with client names and amounts |
| `list_stale_clients()` | Clients with no meaningful contact in 7+ days |
| `record_client_note(client_id, note)` | Persist a note/commitment, remembered in future `prep_call` calls |

## Data Sources — Hackathon Scope
This build uses seeded demo data behind clean provider interfaces:

- **CRM (GHL)**: `GHLProvider` interface with `DemoGHLProvider` implementation
  (5 realistic seeded clients). A real adapter (`RealGHLProvider`) can be
  added using the GHL REST API without changing any calling code.
- **Invoices**: `InvoiceProvider` interface with `DemoInvoiceProvider`.
  Production adapters can connect to Stripe, QuickBooks, or GHL invoicing.

This keeps the demo self-contained and reproducible for judges while making
the production integration point explicit.

## Setup (Local Development)

```bash
git clone https://github.com/ShArafat58/ClientPulse.git
cd ClientPulse
pip install -r requirements.txt
cp .env.example .env
```

Start local DynamoDB (Docker):
```bash
docker run -d -p 8001:8000 --name clientpulse-dynamodb amazon/dynamodb-local
python scripts/create_table.py
```

Run the MCP server:
```bash
python -m src.server
```

Verify with [MCP Inspector](https://github.com/modelcontextprotocol/inspector):
```bash
npx @modelcontextprotocol/inspector
```
Connect to `http://localhost:8000/mcp` via Streamable HTTP.

## Deployment (AWS)
The MCP server is containerized for AWS Lambda using the
[AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter):

```bash
docker build -t clientpulse-mcp .
docker tag clientpulse-mcp:latest <ecr-repo-uri>:latest
docker push <ecr-repo-uri>:latest
aws lambda create-function --function-name clientpulse-mcp \
  --package-type Image --code ImageUri=<ecr-repo-uri>:latest \
  --role <lambda-execution-role-arn> --timeout 30 --memory-size 512
```

## Testing
```bash
pytest tests/ -v
```

## Cost Design
Built to stay within AWS Free Tier / Free Plan credits:
- DynamoDB: pay-per-request, always-free tier covers demo-scale usage
- Lambda: well within the 1M free requests/month allowance
- Bedrock: capped at `MAX_BEDROCK_CALLS_PER_SYNC=20` per background sync
- No NAT Gateway, no provisioned concurrency, no always-on compute

## Privacy & Security
- OAuth 2.1 (client_credentials grant) via Amazon Cognito for service-level
  authentication
- No real client data used — all CRM and invoice data is seeded/demo data
- AWS credentials are never committed; `.env` is gitignored

## Hackathon Scope
Built during the Amazon Developer Hackathon 2026 (Sept–Oct 2026) as a solo
entry. See `docs/friction-log.md` for a full log of issues encountered and
worked around during development.

## Product Feedback
See `docs/product-feedback.md`.

## Friction Log
See `docs/friction-log.md`.

## License
MIT — see `LICENSE`.