# Friction Log — ClientPulse

## Entry 1

**Date:** 2026-09-21
**Task:** Run pytest against src/server.py
**Expected:** Tests import src.server successfully
**Actual:** ModuleNotFoundError: No module named 'src'
**Severity:** Low
**Workaround:** Added pyproject.toml with pythonpath config + src/__init__.py
**Suggested improvement:** FastMCP/pytest quickstart docs could mention src-layout pytest config for new projects

## Entry 2

**Date:** 2026-09-21
**Task:** Implement relationship scoring status thresholds
**Expected:** Score of 1 (mid-range signal) classifies as "watch"
**Actual:** Off-by-one boundary bug classified score=1 as "healthy"
**Severity:** Low
**Workaround:** Fixed threshold logic (score == 0 → healthy, else tiered)
**Suggested improvement:** N/A — internal logic bug, caught by test coverage

## Entry 3

**Date:** 2026-09-21
**Task:** Create DynamoDB table in AWS (real account, not local)
**Expected:** Table creates in us-east-1 with IAM permissions granted
**Actual:** AccessDeniedException with "explicit deny in a service control policy" — new AWS accounts (via the "reimagined getting started" signup flow) are placed in an Organization with region-restriction SCPs. us-east-1 and us-west-2 only allow a narrow set of services (billing, IAM, Bedrock); most compute/database services are denied in those regions.
**Severity:** High (blocked all AWS resource creation for ~1 hour)
**Workaround:** Discovered ap-southeast-2 region has no such restriction in the applied SCP. Switched all resource creation (DynamoDB, Lambda, Cognito, EventBridge) to ap-southeast-2, kept Bedrock calls in us-east-1 (explicitly allowed there).
**Suggested improvement:** AWS's new account signup flow should surface region/service restrictions more clearly before builders hit AccessDeniedException, especially since the default region shown in console (Stockholm) wasn't even one of the "allowed" regions in the SCP.

## Entry 4

**Date:** 2026-09-21
**Task:** Invoke Amazon Bedrock Nova Micro model for the first time
**Expected:** Model responds immediately (page said models are auto-enabled)
**Actual:** AccessDeniedException — "Your account is currently being verified... normally takes less than 2 hours"
**Severity:** Medium (blocks Bedrock/Strands work temporarily, not permanently)
**Workaround:** Proceeding with non-Bedrock-dependent tasks (Cognito, MCP visual card) while waiting for verification
**Suggested improvement:** The "Model access page has been retired" messaging implies instant access, but doesn't mention the account verification step new accounts go through — this caused confusion

## Entry 5

**Date:** 2026-09-21
**Task:** Test Cognito OAuth client_credentials token endpoint
**Expected:** curl works directly
**Actual:** PowerShell's `curl` alias (Invoke-WebRequest) doesn't support -X/-d flags like real curl
**Severity:** Low
**Workaround:** Used `curl.exe` explicitly to invoke the real curl binary instead of the PowerShell alias
**Suggested improvement:** N/A — Windows/PowerShell environment quirk, not an AWS issue

## Entry 6

**Date:** 2026-09-21
**Task:** Invoke Bedrock Nova Micro model (via direct model ID and inference profile)
**Expected:** Model responds after account verification completed
**Actual:** ValidationException: "Operation not allowed" — a known account-level security restriction on new AWS accounts (confirmed via AWS re:Post), requiring an AWS Support case to resolve; not fixable via IAM/SCP changes
**Severity:** High (blocks core AWS Builder mini-challenge requirement)
**Workaround:** Opened AWS Support case (ID: 179000934700535), proceeding with non-Bedrock-dependent work (Lambda, Cognito, MCP visual card) while awaiting resolution
**Suggested improvement:** AWS should surface this restriction proactively (e.g., in the Bedrock console) rather than only via a cryptic InvokeModel error after model access appears fully enabled

## Entry 7

**Date:** 2026-09-21
**Task:** Package FastMCP server as a Lambda-ready Docker container using AWS Lambda Web Adapter
**Expected:** public.ecr.aws/lambda/python base image + Web Adapter extension works together
**Actual:** Lambda base image's built-in runtime client conflicts with the Web Adapter, causing "entrypoint requires the handler name to be the first argument" and empty responses on invocation
**Severity:** Medium
**Workaround:** Switched base image to plain public.ecr.aws/docker/library/python:3.12-slim, keeping only the Web Adapter extension layer — this is the correct pattern per AWS docs for web-app-style Lambda containers
**Suggested improvement:** AWS's Lambda Web Adapter examples should more clearly warn against combining it with the Lambda base runtime images

## Entry 8

**Date:** 2026-09-21
**Task:** Create Lambda function (both zip-based and container-image-based) via CLI
**Expected:** Function creates successfully with attached IAM role
**Actual:** AccessDeniedException with null message on CreateFunction — confirmed via community research (AWS re:Post) to be a known, hard-to-diagnose account-level restriction unrelated to IAM/SCP permissions (IAM Policy Simulator shows "allowed" even when blocked)
**Severity:** High (blocks Lambda deployment, likely same root cause as Bedrock restriction)
**Workaround:** Added details to existing AWS Support case (ID: 179000934700535); proceeding with local development and code that doesn't require live Lambda while awaiting support response
**Suggested improvement:** AWS should provide clearer, more specific error messages for account-level restrictions rather than a generic "None" message that looks identical to a permissions misconfiguration