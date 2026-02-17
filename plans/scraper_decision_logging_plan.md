# Plan: Scraper-First Decision Logging (Fetch to DB Save)

## Summary
Add high-signal logging only for the scraper path so each article has a complete, readable trail:

1. where it entered
2. which stage accepted/rejected/skipped it
3. whether it reached DB save
4. final outcome reason

This plan avoids detailed per-rule execution logs. Rule stage is logged only at decision boundary.

## Scope
Instrument only the scraper flow and direct dependencies used during a run:

1. `server/scraper/pipeline.py`
2. `server/scraper/fetchers.py`
3. `server/scraper/enrichment.py`
4. `server/scraper/filters.py`
5. `server/scraper/storage.py`
6. `server/scraper/server.py` and `server/run_scraper.py` entrypoints
7. `server/scraper/rules/runner.py` only for final rule-gate outcome context (not per-rule logs)

Out of scope:

1. `server/server.py` web API logs
2. Non-scraper legacy script cleanup
3. DB schema changes for log persistence

## Logging Design

### 1) Outputs
1. Console readable logs (for `docker compose logs -f scraper`)
2. Rotating JSON file in temp directory for deeper history

Default config:

1. `LOG_DIR=/tmp/news3001-logs`
2. `LOG_MAX_BYTES=20971520` (20MB)
3. `LOG_BACKUP_COUNT=5`
4. `LOG_LEVEL=INFO`
5. `SCRAPER_DEBUG_TRACE=false` (extra fields only when true)

### 2) Correlation IDs
Every run/article log includes:

1. `run_id` generated at run start
2. `article_id` generated from normalized link hash
3. `source_type` (`google` or `rss`)

### 3) Event Contract
Standard fields:

1. `event`
2. `stage`
3. `outcome` (`pass`, `reject`, `skip`, `saved`, `error`, `undecided`)
4. `reason`
5. `run_id`
6. optional `article_id`, `link`, `source`, `duration_ms`, `counts`

## Pipeline Instrumentation (Exact Stages)

### Run-Level
1. `run.start`: start timestamp, config snapshot (safe subset)
2. `run.fetch.google.done`: count fetched
3. `run.fallback.triggered` / `run.fallback.skipped`
4. `run.finish`: totals by stage and final saved count

### Article-Level (Google path)
For each article:

1. `article.start`
2. `article.enrichment`
   1. `reject` if scrape content missing
   2. `pass` with truncated-length info if available
3. `article.rule_gate`
   1. `reject` if rule gate returns false
   2. `undecided` if returns none
4. `article.snippet_locality`
   1. `pass` or `reject`
5. `article.deep_locality`
   1. `pass` or `reject`
6. `article.save_news`
   1. `saved` with `news_id`
7. `article.finish`
   1. final outcome + terminal stage reason

### Article-Level (RSS fallback path)
Same terminal structure:

1. `article.start`
2. `article.enrichment`
3. `article.save_news`
4. `article.finish`

## Rule Boundary Logging (No Per-Rule Execution Logs)
In `runner` and `pipeline`:

1. Keep rule execution internals silent.
2. Return/propagate only gate-level result context to pipeline:
   1. decision (`False` or `None`)
   2. matched terminal rule name when decision is `False`
3. Pipeline logs one `article.rule_gate` event with:
   1. `outcome=reject` or `undecided`
   2. reason like `rule_gate_reject:<rule_name>` when available

## Public Interfaces / Type Changes
1. Internal return shape change in rules runner:
   1. from `bool | None`
   2. to a lightweight structured result (e.g. tuple/dataclass) containing decision + optional matched rule name
2. `/run` response from scraper service adds:
   1. `run_id`
   2. `log_file` path for quick lookup

No external DB/API schema changes.

## Failure Handling
1. Wrap stage boundaries with exception logging (`event=article.error` + stage context)
2. Ensure each started article emits exactly one `article.finish`
3. Include traceback in JSON file logs; concise error line in console logs

## Validation Scenarios
1. Rule reject path:
   1. article has `start` -> `enrichment pass` -> `rule_gate reject` -> `finish reject`
2. Snippet reject path:
   1. rule gate undecided then snippet reject with clear reason
3. Deep locality reject path:
   1. passes earlier checks, fails at deep check, finish reject
4. Saved path:
   1. all passes + `save_news saved` + `finish saved`
5. Fallback path:
   1. `run.fallback.triggered` present and fallback articles fully traced
6. Rotation:
   1. after enough runs, confirm 5 rotated files of 20MB each

## Assumptions and Defaults
1. Focus is scraper observability, not full-backend logging parity.
2. Rule internals remain unlogged by design; only boundary decisions are logged.
3. Default verbosity remains readable (`INFO`), with optional deeper trace via `SCRAPER_DEBUG_TRACE=true`.
