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