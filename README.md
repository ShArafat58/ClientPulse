# ClientPulse

Juggling dozens of clients? ClientPulse gives you a morning briefing, preps every call, and warns you when a client's gone quiet, right through Alexa+.

## Status
🚧 In development — Amazon Developer Hackathon 2026 (Alexa+ Track + AWS Builder mini-challenge)

## What It Does
ClientPulse is a voice-first client-ops assistant for freelancers and small agencies, built as a real MCP server for Alexa+.

- **Daily briefing** — what needs your attention today
- **Call prep** — instant context before any client call
- **Invoice tracking** — never miss an overdue payment
- **Stale client detection** — spot relationships going cold
- **Persistent memory** — remembers commitments across sessions

## Tech Stack
- MCP Server: Python + FastMCP (spec 2025-11-25+, Streamable HTTP)
- Hosting: AWS Lambda + Function URL
- Auth: Amazon Cognito (OAuth 2.1 + PKCE)
- Memory: Amazon DynamoDB
- CRM: GoHighLevel (GHL) API
- Agent: AWS Strands SDK
- Model: Amazon Bedrock (Nova Micro)

## Data Sources — Hackathon Scope

This build uses seeded demo data behind clean provider interfaces:

- **CRM (GHL)**: `GHLProvider` interface with `DemoGHLProvider` implementation.
  A real adapter (`RealGHLProvider`) can be added using the GHL REST API
  without changing any calling code.
- **Invoices**: `InvoiceProvider` interface with `DemoInvoiceProvider`.
  Production adapters can connect to Stripe, QuickBooks, or GHL invoicing.

This keeps the demo self-contained and reproducible for judges while
showing the exact integration point for production use.

## License
MIT

