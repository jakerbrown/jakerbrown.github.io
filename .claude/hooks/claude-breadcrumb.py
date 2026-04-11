#!/usr/bin/env python3
"""
Claude Code Breadcrumb Writer (Stop Hook)

Writes a breadcrumb file to claude_activity/ at session end, parallel to the
Codex breadcrumb system in codex_activity/. The nightly sweep script collects
both directories.

Breadcrumb format matches Codex: plain-English prose describing what was done,
what changed, why it mattered, and what was verified.

Hook Event: Stop
Returns: Exit code 0 (non-blocking) or writes breadcrumb and exits 0.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Candidate directories — mirrors the codex_activity convention
CANDIDATE_DIRS = (
    "memos/claude_activity",
    "quality_reports/claude_activity",
    "logs/claude_activity",
)

# Parallel Codex dirs — used to detect which base dir the repo uses
CODEX_DIRS = (
    "memos/codex_activity",
    "quality_reports/codex_activity",
    "logs/codex_activity",
)


def get_project_dir() -> str:
    """Get project directory from hook input or environment."""
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # If stop_hook_active, avoid infinite loops
    if hook_input.get("stop_hook_active", False):
        return ""

    return hook_input.get("cwd", os.environ.get("CLAUDE_PROJECT_DIR", ""))


def find_breadcrumb_dir(project_dir: str) -> Path | None:
    """Find or create the claude_activity directory matching the repo's layout."""
    root = Path(project_dir)

    # First check if claude_activity already exists somewhere
    for rel in CANDIDATE_DIRS:
        d = root / rel
        if d.exists():
            return d

    # Match whichever codex_activity dir exists
    for codex_rel, claude_rel in zip(CODEX_DIRS, CANDIDATE_DIRS):
        if (root / codex_rel).exists():
            d = root / claude_rel
            d.mkdir(parents=True, exist_ok=True)
            return d

    # Default: logs/claude_activity
    d = root / "logs" / "claude_activity"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_recent_git_activity(project_dir: str, limit: int = 5) -> list[str]:
    """Get recent commits from this session (last 2 hours)."""
    try:
        out = subprocess.check_output(
            ["git", "log", "--since=2 hours ago", "--pretty=format:%s", f"-{limit}"],
            cwd=project_dir,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return [line for line in out.splitlines() if line.strip()]
    except Exception:
        return []


def get_changed_files(project_dir: str) -> list[str]:
    """Get files changed in recent commits."""
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD~3..HEAD"],
            cwd=project_dir,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return [line for line in out.splitlines() if line.strip()][:10]
    except Exception:
        return []


def find_session_log(project_dir: str) -> str | None:
    """Read the most recent session log for context."""
    root = Path(project_dir)
    for candidate in (
        "quality_reports/session_logs",
        "memos/session_logs",
        "plans/session_logs",
        "logs/session_logs",
    ):
        d = root / candidate
        if not d.exists():
            continue
        logs = sorted(d.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
        if logs:
            try:
                content = logs[0].read_text(encoding="utf-8", errors="ignore")
                # Return last ~500 chars for context
                return content[-500:] if len(content) > 500 else content
            except Exception:
                pass
    return None


def slugify(text: str) -> str:
    """Create a URL-safe slug from text."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] if slug else "session"


def build_breadcrumb(project_dir: str) -> str | None:
    """Build breadcrumb content from git activity and session state."""
    commits = get_recent_git_activity(project_dir)
    changed_files = get_changed_files(project_dir)

    if not commits and not changed_files:
        return None

    lines: list[str] = []

    # Summarize what was worked on
    if commits:
        lines.append(f"Worked on: {commits[0]}.")
        if len(commits) > 1:
            lines.append("")
            lines.append("Also: " + "; ".join(commits[1:3]) + ".")

    # What changed
    if changed_files:
        lines.append("")
        file_summary = ", ".join(changed_files[:5])
        if len(changed_files) > 5:
            file_summary += f", and {len(changed_files) - 5} more"
        lines.append(f"Changed: {file_summary}.")

    # Session log context
    session_context = find_session_log(project_dir)
    if session_context:
        # Extract the last meaningful line from session log
        meaningful = [
            line.strip()
            for line in session_context.splitlines()
            if line.strip() and not line.startswith("#") and not line.startswith("---")
        ]
        if meaningful:
            lines.append("")
            lines.append(f"Context: {meaningful[-1][:200]}")

    return "\n".join(lines)


def main() -> None:
    project_dir = get_project_dir()
    if not project_dir:
        sys.exit(0)

    breadcrumb_dir = find_breadcrumb_dir(project_dir)
    if not breadcrumb_dir:
        sys.exit(0)

    content = build_breadcrumb(project_dir)
    if not content:
        sys.exit(0)

    today = datetime.now().strftime("%Y-%m-%d")
    commits = get_recent_git_activity(project_dir, limit=1)
    slug = slugify(commits[0]) if commits else "session"
    filename = f"{today}_{slug}.md"

    # Don't overwrite existing breadcrumbs
    out_path = breadcrumb_dir / filename
    counter = 1
    while out_path.exists():
        out_path = breadcrumb_dir / f"{today}_{slug}-{counter}.md"
        counter += 1

    try:
        out_path.write_text(content, encoding="utf-8")
    except IOError:
        pass

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Fail open — never block Claude due to a hook bug
        sys.exit(0)
