# Plan: Exact-Path Non-Article Filter Rule

## Summary
Add a simple URL-path rule to filter non-article pages (homepages and section/index pages) using two exact-match lists:

1. A `definite_false` list checked first and returning `False`
2. A `maybe` list checked second and returning `None`

The rule uses exact path equality only. No marker, substring, prefix, or regex matching.

## Scope and Constraints
1. Add one new rule module under `server/scraper/rules`.
2. Update rule order in `server/scraper/rules/runner.py`.
3. Do not change package structure (`__init__.py` remains untouched).
4. Do not add automated tests.

## Implementation Details

### 1) New Rule File
Create `server/scraper/rules/non_article_link_reject.py` with:

1. `DEFINITE_FALSE_PATHS` for exact paths that should be rejected.
2. `MAYBE_PATHS` for exact paths that should remain undecided.
3. `non_article_link_reject(article: ArticleInput) -> bool | None`.

### 2) URL Parsing and Normalization
In `non_article_link_reject`:

1. Parse `article.link` with `urlparse`.
2. Support links with and without scheme.
3. Lowercase the path.
4. Trim trailing slash for non-root paths.
5. Match only by exact path equality against the lists.

### 3) Decision Flow
Inside `non_article_link_reject(article)`:

1. Loop through `DEFINITE_FALSE_PATHS`.
2. If exact path match, return `False`.
3. Loop through `MAYBE_PATHS`.
4. If exact path match, return `None`.
5. If no match, return `None`.

### 4) Runner Integration
Update `server/scraper/rules/runner.py`:

1. Import `non_article_link_reject`.
2. Add it before `snippet_strong_non_local_reject` in `RULES`.

## Initial Path Lists

### `DEFINITE_FALSE_PATHS`
`/`, `/home`, `/homepage`, `/startseite`, `/search`, `/suche`, `/login`, `/account`, `/kontakt`, `/about`, `/impressum`, `/newsletter`, `/rss`, `/feed`, `/category`, `/categories`, `/tag`, `/tags`, `/topic`, `/topics`, `/thema`, `/themen`, `/kategorie`

### `MAYBE_PATHS`
`/news`, `/nachrichten`, `/latest`, `/archive`

## Interface Impact
1. Add internal function: `non_article_link_reject(article: ArticleInput) -> bool | None`.
2. No changes to `ArticleInput`.
3. No external API changes.

## Manual Validation (No Automated Tests)
1. Run the scraper and confirm homepage/section URLs are rejected early (`False`).
2. Confirm maybe-path URLs remain undecided (`None`) and continue in the existing flow.
3. Confirm normal article URLs still proceed to later rules and locality checks.

## Assumptions
1. "No markers" means no substring/prefix/regex matching.
2. Exact-path equality is the only URL-path matching strategy.
3. RSS fallback behavior remains unchanged.
