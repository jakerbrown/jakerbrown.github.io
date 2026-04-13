#!/usr/bin/env python3
"""Lightweight checks for Claude/Codex diary style preferences."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIARY_PATH = ROOT / "files" / "codex-diary" / "diary.md"
MAX_BULLET_WORDS = 28


def find_latest_entry(text: str) -> tuple[str, list[str]] | None:
    matches = list(
        re.finditer(
            r"^## (\d{4}-\d{2}-\d{2}(?: to \d{4}-\d{2}-\d{2})?)\n"
            r"(.*?)(?=^## \d{4}-\d{2}-\d{2}(?: to \d{4}-\d{2}-\d{2})?\n|\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
    )
    if not matches:
        return None
    latest = matches[-1]
    entry_date = latest.group(1)
    body = latest.group(2)
    bullets: list[str] = []
    current: str | None = None
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        if line.lstrip().startswith("- "):
            if current is not None:
                bullets.append(current.strip())
            current = line.lstrip()[2:].strip()
        elif current is not None and line.strip():
            current = f"{current} {line.strip()}"
    if current is not None:
        bullets.append(current.strip())
    return entry_date, bullets


def main() -> int:
    text = DIARY_PATH.read_text(encoding="utf-8")
    latest = find_latest_entry(text)
    if latest is None:
        print("No diary entries found.")
        return 0

    entry_date, bullets = latest
    issues: list[str] = []

    for idx, bullet in enumerate(bullets, start=1):
        if "`" in bullet:
            issues.append(f"{entry_date} bullet {idx}: avoid backticked names or jargon.")
        if re.search(r"\b(referenda|jakerbrown\.github\.io)\b", bullet):
            issues.append(f"{entry_date} bullet {idx}: replace repo names with project descriptions.")
        if len(bullet.split()) > MAX_BULLET_WORDS:
            issues.append(
                f"{entry_date} bullet {idx}: shorten bullet to about {MAX_BULLET_WORDS} words or fewer."
            )

    if issues:
        for issue in issues:
            print(issue)
        return 1

    print(f"{entry_date}: diary style checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
