# Product Feedback — ClientPulse (Amazon Developer Hackathon 2026)

## Tools, APIs, and SDKs Used
- **MCP (Model Context Protocol)** via FastMCP (Python), spec 2025-11-25,
  Streamable HTTP transport
- **AWS Strands Agents SDK** — client-intelligence orchestration
- **Amazon Bedrock** (Nova Micro) — reasoning/explanation layer
- **Amazon DynamoDB** — persistent client memory (single-table design)
- **AWS Lambda** (container image + Lambda Web Adapter) — MCP server hosting
- **Amazon Cognito** — OAuth 2.1 client_credentials flow for MCP auth
- **Amazon ECR** — container image registry
- **AWS Organizations / IAM** — encountered directly while resolving
  account-level restrictions (see below)

## What Worked Well
- **FastMCP** made standing up a spec-compliant MCP server with Streamable
  HTTP fast — a working server with real tools took under an hour once the
  library was installed.
- **MCP Inspector** was excellent for verification: connecting, listing
  tools, and calling them with structured JSON input/output gave immediate,
  trustworthy confidence that the server behaved correctly before any
  Alexa+ integration was attempted.
- **DynamoDB Local** (Docker) allowed fast local iteration without touching
  real AWS resources or incurring any cost during early development.
- **Strands' model-agnostic design** made it straightforward to write a
  mock model for offline development and swap in a real `BedrockModel`
  later with a single environment variable — this decoupling turned out to
  be essential given the account restrictions described below.
- The separation of deterministic rules-based scoring from LLM-based
  explanation (rather than asking a model to do both) kept the system
  fast, cheap, and explainable — and made local mock development
  realistic enough to build the entire pipeline before Bedrock access
  was confirmed.

## What Needs Work
- **New AWS account restrictions were the single biggest friction point.**
  A newly created AWS account (via the current "reimagined" sign-up flow)
  is placed in a sandboxed Organization with Service Control Policies that
  silently block most compute/database services in the console's default
  region (Stockholm) and even in us-east-1/us-west-2, with no proactive
  warning. Discovering the one unrestricted region (ap-southeast-2)
  required manually reading raw SCP JSON via the CLI.
- **Bedrock and Lambda both returned account-level `AccessDeniedException`
  errors with no descriptive message** ("Operation not allowed" / "None"),
  even with full IAM permissions and confirmed model availability. Multiple
  independent AWS re:Post threads confirm this is a known, common issue for
  new accounts, resolvable only via an AWS Support case — with no visibility
  into how long resolution takes on the Basic Support plan.
- The "Model access page has been retired... models are now automatically
  enabled" messaging in the Bedrock console was misleading in this context:
  it implied instant access but didn't mention the account verification
  step new accounts go through.
- AWS Lambda Web Adapter documentation doesn't clearly warn against
  combining it with the `public.ecr.aws/lambda/*` base images — the two
  runtime patterns conflict and produce a confusing error.

## Onboarding Experience
Getting a first "hello world" MCP tool running locally was smooth and fast.
Getting the same server deployed on real AWS infrastructure was
significantly slower — not due to the AWS services' own complexity, but
due to new-account restrictions that aren't surfaced clearly until you hit
them via cryptic API errors. A new builder without prior AWS experience
would likely give up before finding the region-restriction workaround or
knowing to open a support case.

## Would We Build With It Again?
Yes. FastMCP, Strands, and Bedrock are each genuinely pleasant to build
with once account-level access is unblocked, and the architecture (rules +
LLM explanation, cached for low-latency voice responses) scales well beyond
the hackathon scope. The account onboarding friction is a one-time cost;
it would not recur on a mature account.