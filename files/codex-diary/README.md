# Codex Diary

This directory holds a durable diary of Codex work across repos.

## Goal

Produce one dated entry per automation window with a short set of plain-language
bullets that capture what Codex helped accomplish without turning into a
technical log dump.

## Workflow

1. Each participating repo writes short local breadcrumb entries for non-trivial
   Codex work.
2. An automation scans those breadcrumbs and recent git history.
3. The automation writes a digest to `daily_digest/YYYY-MM-DD.md` for a
   one-day window or `daily_digest/YYYY-MM-DD_to_YYYY-MM-DD.md` for a
   multi-day window.
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

- 3 to 8 bullets per entry
- no more than roughly half a page
- interesting and specific
- not overly technical
- not padded or repetitive
- prefer plain-language descriptions of the work over repo names, file names, or internal tool names
- if a project needs to be identified, describe it by topic or purpose rather than by repository name
- summarize outcomes and purpose rather than implementation mechanics
- prefer "worked on X for Y" over "did X, which meant Y"
- prioritize substantive work from research and analysis repos before workflow
  or website maintenance
- use at most one bullet from `codex-my-workflow` on any given day
- use at most one bullet from `jakerbrown.github.io` on any given day
- stay brief: prefer more bullets with less text in each one
- most bullets should be a single short sentence
- keep most bullets to the first clause: what was done, and for what project
- if a bullet starts accumulating clauses, split it into two bullets instead
- avoid the common pattern "did X, then explained what doing X accomplished"
- allow enough specificity that a regular reader can understand the general
  kind of project or research area involved
- keep the tone matter-of-fact and avoid piling on adjectives
- write for readers who are curious about how AI systems support research work
- when useful, mention how Codex changed the workflow, decision process, or
  pace of progress
- prefer a calm diary voice over an explanatory AI-systems voice
- each bullet should usually be one clean idea, not a chain of clauses
- if the day includes enough activity elsewhere, let `codex-my-workflow` and
  `jakerbrown.github.io` recede into brief supporting context rather than
  dominate the entry
- treat any deliberate manual edit to `diary.md` as a strong signal about the
  user's wording and topic preferences
- when such an edit appears, add a short note to
  `config/style_preferences.md` explaining the inferred preference, unless the
  edit was plainly an accidental wipe or similar mistake

The canonical style rules live in `config/style_preferences.md`.

## Files

- `config/repos.txt`: repos included in the diary scan
- `config/style_preferences.md`: durable diary tone and naming rules
- `daily_digest/`: generated source material for each diary window
- `diary.md`: the running diary itself
