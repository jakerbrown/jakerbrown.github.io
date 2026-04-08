# Codex Diary

This directory holds a durable daily diary of Codex work across repos.

## Goal

Produce one dated entry per day with a short set of plain-language bullets that
capture what Codex helped accomplish without turning into a technical log dump.

## Workflow

1. Each participating repo writes short local breadcrumb entries for non-trivial
   Codex work.
2. A nightly automation scans those breadcrumbs and the day's git history.
3. The automation writes a digest to `daily_digest/YYYY-MM-DD.md`.
4. Codex turns that digest into a polished diary entry in `diary.md`.

## Breadcrumb contract

Each repo should write breadcrumb entries under one of these local directories:

- `memos/codex_activity/`
- `quality_reports/codex_activity/`
- `logs/codex_activity/`

Preferred filename pattern:

- `YYYY-MM-DD_slug.md`

Each breadcrumb should stay short and answer:

- what was worked on
- what changed
- why it mattered
- what got verified or left unfinished

Use plain English. Be concrete, but do not drown the diary in low-level
implementation details.

## Diary style

- 3 to 8 bullets per day
- no more than roughly half a page
- interesting and specific
- not overly technical
- not padded or repetitive

## Files

- `config/repos.txt`: repos included in the nightly scan
- `daily_digest/`: generated daily source material for the diary
- `diary.md`: the running diary itself
