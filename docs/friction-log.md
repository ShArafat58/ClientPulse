# Friction Log — ClientPulse

## Entry 1

**Date:** 2026-09-21
**Task:** Run pytest against src/server.py
**Expected:** Tests import src.server successfully
**Actual:** ModuleNotFoundError: No module named 'src'
**Severity:** Low
**Workaround:** Added pyproject.toml with pythonpath config + src/__init__.py
**Suggested improvement:** FastMCP/pytest quickstart docs could mention src-layout pytest config for new projects