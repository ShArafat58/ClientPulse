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