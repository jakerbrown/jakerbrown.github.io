---
name: deep-audit
description: |
  Deep consistency audit of the entire repository infrastructure.
  Launches 4 parallel specialist agents to find factual errors, code bugs,
  count mismatches, and cross-document inconsistencies. Then fixes all issues
  and loops until clean.
  Use when: after making broad changes, before releases, or when user says
  "audit", "find inconsistencies", "check everything".
author: Claude Code Academic Workflow
version: 1.0.0
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task"]
---

# /deep-audit -- Repository Infrastructure Audit

Run a comprehensive consistency audit across the entire repository, fix all issues found, and loop until clean.

## When to Use

- After broad changes (new scripts, rules, hooks, documentation edits)
- Before releases or major commits
- When the user asks to "find inconsistencies", "audit", or "check everything"

## Workflow

### PHASE 1: Launch 4 Parallel Audit Agents

Launch these 4 agents simultaneously using `Task` with `subagent_type=general-purpose`:

#### Agent 1: Documentation Accuracy
Focus: README.md, CLAUDE.md, KNOWLEDGE_BASE.md, any guide files
- All numeric claims match reality (file counts, feature lists)
- All file paths mentioned actually exist on disk
- Code examples are syntactically correct
- Cross-references resolve
- No stale claims from previous versions

#### Agent 2: Hook & Config Quality
Focus: `.claude/hooks/*.py` and `.claude/hooks/*.sh`, `.claude/settings.json`
- No remaining `/tmp/` usage (should use `~/.claude/sessions/`)
- Hash length consistency (`[:8]` across all hooks)
- Proper error handling (fail-open pattern: top-level `try/except` with `sys.exit(0)`)
- JSON input/output correctness
- Exit code correctness (0 for non-blocking)
- `from __future__ import annotations` for Python 3.8+ compatibility

#### Agent 3: Skills and Rules Consistency
Focus: `.claude/skills/*/SKILL.md` and `.claude/rules/*.md`
- Valid YAML frontmatter in all files
- `allowed-tools` values are sensible
- Rule `paths:` reference existing directories
- No contradictions between rules
- CLAUDE.md references match actual skill/rule directories

#### Agent 4: Cross-Document Consistency
Focus: All documentation and configuration files
- Feature counts agree across all documents
- All links point to valid targets
- Directory tree in docs matches actual structure
- No stale references from previous versions

### PHASE 2: Triage Findings

Categorize each finding:
- **Genuine bug**: Fix immediately
- **False alarm**: Discard (document WHY it's false for future rounds)

### PHASE 3: Fix All Issues

Apply fixes in parallel where possible. For each fix:
1. Read the file first (required by Edit tool)
2. Apply the fix
3. Verify the fix (grep for stale values, check syntax)

### PHASE 4: Loop or Declare Clean

After fixing, launch a fresh set of agents to verify.
- If new issues found -> fix and loop again
- If zero genuine issues -> declare clean and report summary

**Max loops: 5** (to prevent infinite cycling)

## Output Format

After each round, report:

```
## Round N Audit Results

### Issues Found: X genuine, Y false alarms

| # | Severity | File | Issue | Status |
|---|----------|------|-------|--------|
| 1 | Critical | file.py:42 | Description | Fixed |
| 2 | Medium | file.md:100 | Description | Fixed |

### Verification
- [ ] No stale counts (grep confirms)
- [ ] All hooks have fail-open + future annotations
- [ ] Documentation renders successfully

### Result: [CLEAN | N issues remaining]
```
