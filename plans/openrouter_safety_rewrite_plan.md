# Plan: OpenRouter Safety Rewrite (Core First, Single Free Autorouter)

## Summary
Refactor the OpenRouter integration into a typed, safer LLM gateway and migrate all app call sites to it in phases.  
The rewrite keeps one route only (`openrouter/free`), retries on that same route, and never switches to a fallback model.

## Goals
1. Make LLM behavior deterministic enough for scraper decisions via strict output contracts.
2. Improve reliability with bounded retries and clear failure reasons.
3. Prevent unsafe model output handling in badges/report flows.
4. Centralize OpenRouter access so all usage follows one hardened path.

## Scope and Constraints
1. In scope: app code under `server/` and UI report rendering safety.
2. Out of scope: secrets rotation/ops hardening and external infra changes.
3. Retry strategy: single provider route only; no fallback model switching.
4. Report output contract: plain text only (no model-authored HTML).
5. Tests: no new automated tests; manual validation only.
6. Compatibility: breaking cleanup is allowed if final behavior is coherent.

## Current Risks to Address
1. `server/openrouter/openrouter_client.py` swallows broad exceptions and returns unvalidated free-form text.
2. `server/content_scraper.py` decisions depend on exact raw string matches (`Smart`, `Local`) without schema validation.
3. `server/openrouter/badges.py` parses comma-separated IDs from untrusted model text.
4. `server/openrouter/report.py` stores model output as HTML.
5. `ui/components/report.php` renders report content directly.
6. API keys are read at import time in some modules, creating brittle startup/runtime behavior.

## Target Architecture

### 1) New LLM module
Create `server/llm/`:
1. `contracts.py`: typed request/response objects and error codes.
2. `provider.py`: provider interface.
3. `openrouter_provider.py`: OpenRouter implementation.
4. `gateway.py`: retry orchestration, validation, and result mapping.
5. `prompts.py`: centralized prompts per task.
6. `parsers.py`: strict JSON parsing and schema checks.

### 2) Typed task contracts
Use task-specific JSON outputs only:
1. `snippet_locality`: `{"decision":"LOCAL|NOT_LOCAL","reason":"..."}`
2. `full_content_locality`: `{"decision":"LOCAL|NOT_LOCAL","reason":"..."}`
3. `badge_classification`: `{"badge_ids":["id1","id2"]}`
4. `report_summary`: `{"summary":"plain text"}`

### 3) Single-route retry policy
For every task:
1. Attempt 1: configured route (`OPENROUTER_MODEL`, default `openrouter/free`)
2. Attempt 2: same route
3. Attempt 3: same route

Retryable conditions:
1. Timeout/network transport failure
2. 429/5xx provider response
3. Empty output
4. Invalid JSON or schema mismatch

Non-retryable conditions:
1. Missing API key
2. 401/403 auth/config errors

## Implementation Phases

### Phase 1: Harden Core Gateway
1. Implement `server/llm/*` module and response envelopes:
   `TaskResult(ok, value, reason_code, attempts, provider, model, request_id, latency_ms)`.
2. Add timeout and max-attempt config:
   - `OPENROUTER_MODEL` (default `openrouter/free`)
   - `LLM_TIMEOUT_SECONDS` (default 20)
   - `LLM_MAX_ATTEMPTS` (default 3)
3. Add minimal structured logs without full prompt dumps:
   - task, attempt, model, latency, reason_code, request_id.

### Phase 2: Compatibility Bridge
1. Keep `server/openrouter/openrouter_client.py` as a shim that delegates to `server/llm/gateway.py`.
2. Keep old function shape temporarily so call sites migrate incrementally.
3. Move API key resolution to runtime call boundaries instead of import-time globals.

### Phase 3: Migrate Call Sites
1. `server/content_scraper.py`
   - Replace free-form string checks with typed locality task results.
   - Fail closed when locality classification is invalid/unavailable.
2. `server/openrouter/badges.py`
   - Replace comma parsing with JSON array parsing.
   - Drop unknown badge IDs safely; never crash pipeline.
3. `server/openrouter/report.py`
   - Request plain-text summary output only.
   - On complete LLM failure, generate deterministic fallback summary from article titles/sources.
4. `server/scraper/filters.py` and `server/scraper/storage.py`
   - Remove module-level API key globals and resolve keys during function execution.

### Phase 4: UI and Cleanup
1. `ui/components/report.php`
   - Render escaped plain text only (`htmlspecialchars`, linebreak-safe formatting).
2. Remove dead prompt/HTML assumptions from report flow.
3. Keep `/report` and `/oldreport` endpoints, but data semantics become plain text summary.

## Public Interface and Behavior Changes
1. Internal API addition: `server/llm/gateway.py` task-based execution entrypoint.
2. Report content format changes from model HTML to plain text.
3. No fallback model semantics anywhere in config, logs, or runtime behavior.

## Failure Handling Matrix
1. Snippet locality failure/invalid output: reject article (`False`).
2. Full-content locality failure/invalid output: reject article (`False`).
3. Badge classification failure: continue with empty badges.
4. Report summary failure after retries: save deterministic fallback summary.

## Manual Validation (No Automated Tests)
1. Happy path: scraper run completes; local articles saved; badges and report present.
2. Invalid model output: confirm same-route retry and eventual safe fallback behavior.
3. Simulated 429/5xx: confirm up to 3 attempts on the same route only.
4. Missing/invalid API key: confirm non-retryable error handling and clear reason output.
5. UI report rendering: verify report text is escaped and scripts/tags do not execute.
6. Legacy path audit: ensure no remaining direct free-form OpenRouter calls bypass gateway.

## Deliverables
1. New `server/llm/` module with contracts, provider adapter, gateway, and parsers.
2. Updated OpenRouter call sites in scraper, badges, and report paths.
3. Safe plain-text report rendering in UI.
4. Updated docs (README section) describing new env vars and retry behavior.

## Assumptions
1. Free autorouter may route to different underlying free models internally between attempts.
2. Retrying the same route is sufficient; no explicit secondary model is desired.
3. Deterministic fallback report text is acceptable when LLM output is unavailable.
