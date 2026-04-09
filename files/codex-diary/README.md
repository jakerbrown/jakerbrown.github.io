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
4. Codex turns that digest into a polished diary entry in `diary.md`, following
   `config/style_preferences.md`.
5. A quick style check can be run with `python3 scripts/check_codex_diary_style.py`.

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
- prefer plain-language descriptions of the work over repo names, file names, or internal tool names
- if a project needs to be identified, describe it by topic or purpose rather than by repository name
- summarize outcomes and purpose rather than implementation mechanics
- stay brief: prefer more bullets with less text in each one
- most bullets should be a single short sentence
- if a bullet starts accumulating clauses, split it into two bullets instead
- allow enough specificity that a regular reader can understand the general
  kind of project or research area involved
- keep the tone matter-of-fact and avoid piling on adjectives
- write for readers who are curious about how AI systems support research work
- when useful, mention how Codex changed the workflow, decision process, or
  pace of progress
- prefer a calm diary voice over an explanatory AI-systems voice
- each bullet should usually be one clean idea, not a chain of clauses

The canonical style rules live in `config/style_preferences.md`.

## Files

- `config/repos.txt`: repos included in the nightly scan
- `config/style_preferences.md`: durable diary tone and naming rules
- `daily_digest/`: generated daily source material for the diary
- `diary.md`: the running diary itself
