#!/usr/bin/env python3
"""Collect daily Claude and Codex breadcrumbs and git activity across repos."""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIARY_ROOT = ROOT / "files" / "codex-diary"
REPO_CONFIG = DIARY_ROOT / "config" / "repos.txt"
CODEX_LOG_DIRS = (
    "memos/codex_activity",
    "quality_reports/codex_activity",
    "logs/codex_activity",
)
CLAUDE_LOG_DIRS = (
    "memos/claude_activity",
    "quality_reports/claude_activity",
    "logs/claude_activity",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def load_repos() -> list[Path]:
    repos: list[Path] = []
    for raw in REPO_CONFIG.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        repos.append(Path(line))
    return repos


def find_breadcrumbs(repo: Path, day: dt.date, dirs: tuple[str, ...]) -> list[Path]:
    matches: list[Path] = []
    date_prefix = day.isoformat()
    for rel in dirs:
        directory = repo / rel
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            if path.name.startswith(date_prefix):
                matches.append(path)
                continue
            modified = dt.date.fromtimestamp(path.stat().st_mtime)
            if modified == day:
                matches.append(path)
    return matches


def git_log(repo: Path, day: dt.date) -> list[str]:
    start = dt.datetime.combine(day, dt.time.min)
    end = start + dt.timedelta(days=1)
    cmd = [
        "git",
        "log",
        "--since",
        start.isoformat(),
        "--until",
        end.isoformat(),
        "--pretty=format:%h %s",
    ]
    try:
        out = subprocess.check_output(
            cmd,
            cwd=repo,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return []
    return [line for line in out.splitlines() if line.strip()]


def read_snippet(path: Path, limit: int = 12) -> list[str]:
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line:
            continue
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def build_report(day: dt.date) -> str:
    lines: list[str] = []
    lines.append(f"# Claude/Codex Diary Digest for {day.isoformat()}")
    lines.append("")
    lines.append(
        "Use this digest to write a short plain-language diary entry."
        " Group bullets under ### Claude and ### Codex headers (Claude first)."
        " Prefer outcomes and significance over implementation detail."
    )
    lines.append("")

    for repo in load_repos():
        if not repo.exists():
            continue
        claude_crumbs = find_breadcrumbs(repo, day, CLAUDE_LOG_DIRS)
        codex_crumbs = find_breadcrumbs(repo, day, CODEX_LOG_DIRS)
        commits = git_log(repo, day)
        if not claude_crumbs and not codex_crumbs and not commits:
            continue

        lines.append(f"## {repo.name}")
        lines.append("")

        if claude_crumbs:
            lines.append("### Claude Breadcrumbs")
            lines.append("")
            for path in claude_crumbs:
                rel = path.relative_to(repo)
                lines.append(f"- `{rel}`")
                for snippet in read_snippet(path):
                    lines.append(f"  - {snippet}")
            lines.append("")

        if codex_crumbs:
            lines.append("### Codex Breadcrumbs")
            lines.append("")
            for path in codex_crumbs:
                rel = path.relative_to(repo)
                lines.append(f"- `{rel}`")
                for snippet in read_snippet(path):
                    lines.append(f"  - {snippet}")
            lines.append("")

        if commits:
            lines.append("### Git Commits")
            lines.append("")
            for commit in commits[:12]:
                lines.append(f"- {commit}")
            lines.append("")

    if len(lines) <= 4:
        lines.append("No activity was found for the configured repos on this date.")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    day = dt.date.fromisoformat(args.date)
    report = build_report(day)
    if args.write:
        out_path = DIARY_ROOT / "daily_digest" / f"{day.isoformat()}.md"
        out_path.write_text(report, encoding="utf-8")
        print(out_path)
        return
    print(report, end="")


if __name__ == "__main__":
    main()
