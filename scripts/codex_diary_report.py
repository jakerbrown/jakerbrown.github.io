#!/usr/bin/env python3
"""Collect Claude and Codex breadcrumbs and git activity across repos."""

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
    parser.add_argument("--days", type=int, default=1)
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


def window_days(end_day: dt.date, days: int) -> list[dt.date]:
    if days < 1:
        raise ValueError("--days must be at least 1")
    start_day = end_day - dt.timedelta(days=days - 1)
    return [start_day + dt.timedelta(days=offset) for offset in range(days)]


def digest_stem(days: list[dt.date]) -> str:
    if len(days) == 1:
        return days[0].isoformat()
    return f"{days[0].isoformat()}_to_{days[-1].isoformat()}"


def build_report(end_day: dt.date, days: int) -> str:
    report_days = window_days(end_day, days)
    lines: list[str] = []
    if len(report_days) == 1:
        label = report_days[0].isoformat()
    else:
        label = f"{report_days[0].isoformat()} to {report_days[-1].isoformat()}"
    lines.append(f"# Claude/Codex Diary Digest for {label}")
    lines.append("")
    lines.append(
        "Use this digest to write a short plain-language diary entry covering"
        f" the last {len(report_days)} day{'s' if len(report_days) != 1 else ''}."
        " Group bullets under ### Claude and ### Codex headers (Claude first)."
        " Prefer outcomes and significance over implementation detail."
    )
    lines.append("")

    for repo in load_repos():
        if not repo.exists():
            continue
        repo_lines: list[str] = []
        for day in report_days:
            claude_crumbs = find_breadcrumbs(repo, day, CLAUDE_LOG_DIRS)
            codex_crumbs = find_breadcrumbs(repo, day, CODEX_LOG_DIRS)
            commits = git_log(repo, day)
            if not claude_crumbs and not codex_crumbs and not commits:
                continue

            repo_lines.append(f"### {day.isoformat()}")
            repo_lines.append("")

            if claude_crumbs:
                repo_lines.append("#### Claude Breadcrumbs")
                repo_lines.append("")
                for path in claude_crumbs:
                    rel = path.relative_to(repo)
                    repo_lines.append(f"- `{rel}`")
                    for snippet in read_snippet(path):
                        repo_lines.append(f"  - {snippet}")
                repo_lines.append("")

            if codex_crumbs:
                repo_lines.append("#### Codex Breadcrumbs")
                repo_lines.append("")
                for path in codex_crumbs:
                    rel = path.relative_to(repo)
                    repo_lines.append(f"- `{rel}`")
                    for snippet in read_snippet(path):
                        repo_lines.append(f"  - {snippet}")
                repo_lines.append("")

            if commits:
                repo_lines.append("#### Git Commits")
                repo_lines.append("")
                for commit in commits[:12]:
                    repo_lines.append(f"- {commit}")
                repo_lines.append("")

        if not repo_lines:
            continue

        lines.append(f"## {repo.name}")
        lines.append("")
        lines.extend(repo_lines)

    if len(lines) <= 4:
        lines.append(
            "No activity was found for the configured repos in this date window."
        )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    day = dt.date.fromisoformat(args.date)
    report_days = window_days(day, args.days)
    report = build_report(day, args.days)
    if args.write:
        out_path = DIARY_ROOT / "daily_digest" / f"{digest_stem(report_days)}.md"
        out_path.write_text(report, encoding="utf-8")
        print(out_path)
        return
    print(report, end="")


if __name__ == "__main__":
    main()
