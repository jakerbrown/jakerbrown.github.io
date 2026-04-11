---
paths:
  - "**/*.R"
  - "**/*.py"
  - "**/*.tex"
  - "**/*.qmd"
  - "**/*.md"
---

# Quality Gates & Scoring Rubrics

## Thresholds

- **80/100 = Commit** -- good enough to save
- **90/100 = PR** -- ready for review/deployment
- **95/100 = Excellence** -- aspirational

## R Scripts (.R)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax errors | -100 |
| Critical | Domain-specific bugs | -30 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing set.seed() | -10 |
| Major | Missing figure generation | -5 |

## Documents (.tex, .qmd, .md)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Compilation/render failure | -100 |
| Critical | Broken citation | -15 |
| Critical | Typo in equation | -10 |
| Major | Notation inconsistency | -3 |
| Minor | Long lines (>100 chars) | -1 |

## Enforcement

- **Score < 80:** Block commit. List blocking issues.
- **Score < 90:** Allow commit, warn. List recommendations.
- User can override with justification.

## Quality Reports

Generated **only at merge time**. Use `templates/quality-report.md` for format.

## Tolerance Thresholds (Research)

<!-- Customize for your domain -->

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Point estimates | [e.g., 1e-6] | [Numerical precision] |
| Standard errors | [e.g., 1e-4] | [MC variability] |
| Coverage rates | [e.g., +/- 0.01] | [MC with B reps] |
