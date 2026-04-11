# CLAUDE.MD -- jakerbrown.github.io

**Project:** jakerbrown.github.io
**Branch:** main

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans`
- **Verify after** -- run code and confirm output at the end of every task
- **Quality gates** -- nothing ships below 80/100
- **[LEARN] tags** -- when corrected, save `[LEARN:category] wrong -> right` to MEMORY.md

---

## Commands

```bash
# R scripts
Rscript path/to/script.R

# Python scripts
python3 path/to/script.py

# Git workflow
git status && git diff --stat
```

---

## Quality Thresholds

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for review |
| 95 | Excellence | Aspirational |

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/commit [msg]` | Stage, commit, PR, merge |
| `/data-analysis [dataset]` | End-to-end R analysis |
| `/review-r [file]` | R code quality review |
| `/proofread [file]` | Grammar/typo/consistency review |
| `/deep-audit` | Repository-wide consistency audit |
| `/lit-review [topic]` | Literature search + synthesis |
| `/research-ideation [topic]` | Research questions + strategies |
| `/interview-me [topic]` | Interactive research interview |
| `/review-paper [file]` | Manuscript review |
| `/learn [skill-name]` | Extract discovery into persistent skill |
| `/context-status` | Show session health + context usage |

---

## Specialist Mapping

| Workflow Role | Agent | When to Use |
|--------------|-------|-------------|
| Code reviewer | r-reviewer | R script changes |
| Domain reviewer | domain-reviewer | Substantive correctness |
| Proofreader | proofreader | Writing quality |
| Verifier | verifier | Pre-commit checks |
