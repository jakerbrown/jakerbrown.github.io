#!/usr/bin/env python3

from __future__ import annotations

import html
import math
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "blog" / "posts-src"
BLOG_DIR = ROOT / "blog"
PAGE_DIR = BLOG_DIR / "page"
DIARY_PATH = ROOT / "files" / "codex-diary" / "diary.md"
POSTS_PER_PAGE = 5
LAST_PUBLIC_DIARY_DATE = datetime.strptime("2026-04-12 23:59", "%Y-%m-%d %H:%M")


@dataclass
class Post:
    slug: str
    title: str
    date: datetime
    publish_at: datetime | None
    subtitle: str
    summary: str
    body_html: str
    source_name: str

    @property
    def display_date(self) -> str:
        return self.date.strftime("%B %-d, %Y")

    @property
    def display_timestamp(self) -> str:
        if self.date.hour == 0 and self.date.minute == 0:
            return self.display_date
        return self.date.strftime("%B %-d, %Y at %-I:%M %p")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "post"


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("Post is missing front matter.")

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError("Post front matter is not closed.")

    _, raw_meta, body = parts
    metadata: dict[str, str] = {}
    for line in raw_meta.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid front matter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, body.strip()


def parse_post_datetime(value: str) -> datetime:
    formats = (
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
    )
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported post date format: {value}")


def extract_footnotes(markdown_text: str) -> tuple[str, dict[str, str]]:
    footnotes: dict[str, str] = {}
    body_lines: list[str] = []

    for raw_line in markdown_text.splitlines():
        match = re.match(r"\[\^([^\]]+)\]:\s+(.*)", raw_line.strip())
        if match:
            footnotes[match.group(1)] = match.group(2).strip()
            continue
        body_lines.append(raw_line)

    return "\n".join(body_lines).strip(), footnotes


def protect_math(text: str) -> tuple[str, dict[str, str]]:
    placeholders: dict[str, str] = {}

    def store_math(value: str) -> str:
        key = f"@@MATH{len(placeholders)}@@"
        placeholders[key] = value
        return key

    protected = re.sub(
        r"(?<!\\)(\${1,2})(.+?)(?<!\\)\1",
        lambda match: store_math(match.group(0)),
        text,
    )
    return protected, placeholders


def restore_math(text: str, placeholders: dict[str, str]) -> str:
    restored = text
    for key, value in placeholders.items():
        restored = restored.replace(key, value)
    return restored


def render_inline(text: str, footnotes: dict[str, str] | None = None) -> str:
    protected_text, math_placeholders = protect_math(text)
    escaped = html.escape(protected_text)
    if footnotes:
        escaped = re.sub(
            r"\[\^([^\]]+)\]",
            lambda match: (
                f'<sup id="fnref-{match.group(1)}">'
                f'<a href="#fn-{match.group(1)}">{match.group(1)}</a>'
                "</sup>"
                if match.group(1) in footnotes
                else match.group(0)
            ),
            escaped,
        )
    escaped = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda match: (
            '<img class="post-image" '
            f'src="{html.escape(match.group(2), quote=True)}" '
            f'alt="{html.escape(match.group(1), quote=True)}">'
        ),
        escaped,
    )
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: (
            f'<a href="{html.escape(match.group(2), quote=True)}">'
            f"{match.group(1)}</a>"
        ),
        escaped,
    )
    return restore_math(escaped, math_placeholders)


def render_markdown(markdown_text: str) -> str:
    markdown_text, footnotes = extract_footnotes(markdown_text)
    lines = markdown_text.splitlines()
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    list_type: str | None = None
    in_code_block = False
    code_lines: list[str] = []
    in_display_math = False
    display_math_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(line.strip() for line in paragraph)
            blocks.append(f"<p>{render_inline(text, footnotes)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items, list_type
        if list_items and list_type:
            items = "".join(
                f"<li>{render_inline(item, footnotes)}</li>" for item in list_items
            )
            blocks.append(f"<{list_type}>{items}</{list_type}>")
            list_items = []
            list_type = None

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            code = "\n".join(html.escape(line) for line in code_lines)
            blocks.append(f"<pre><code>{code}</code></pre>")
            code_lines = []

    def flush_display_math() -> None:
        nonlocal display_math_lines
        if display_math_lines:
            math_text = "\n".join(display_math_lines)
            blocks.append(f'<div class="math-display">{math_text}</div>')
            display_math_lines = []

    for raw_line in lines:
        line = raw_line.rstrip()

        if line.startswith("```"):
            flush_paragraph()
            flush_list()
            if in_code_block:
                flush_code()
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(raw_line)
            continue

        stripped = line.strip()

        if in_display_math:
            display_math_lines.append(stripped)
            if stripped.endswith("$$") and stripped != "$$":
                flush_display_math()
                in_display_math = False
            continue

        if stripped == "$$":
            flush_paragraph()
            flush_list()
            in_display_math = True
            display_math_lines = ["$$"]
            continue

        if stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
            flush_paragraph()
            flush_list()
            display_math_lines = [stripped]
            flush_display_math()
            continue

        if not stripped:
            flush_paragraph()
            flush_list()
            continue

        ordered_list_match = re.match(r"(\d+)\.\s+(.*)", line)

        if list_items and raw_line[:1].isspace() and not line.lstrip().startswith("- ") and not ordered_list_match:
            list_items[-1] = f"{list_items[-1]} {line.strip()}"
            continue

        if line.startswith("# "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h2>{render_inline(line[2:].strip(), footnotes)}</h2>")
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h3>{render_inline(line[3:].strip(), footnotes)}</h3>")
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h4>{render_inline(line[4:].strip(), footnotes)}</h4>")
            continue

        if line.startswith("> "):
            flush_paragraph()
            flush_list()
            blocks.append(
                f"<blockquote><p>{render_inline(line[2:].strip(), footnotes)}</p></blockquote>"
            )
            continue

        if line.startswith("- "):
            flush_paragraph()
            if list_type not in (None, "ul"):
                flush_list()
            list_type = "ul"
            list_items.append(line[2:].strip())
            continue

        if ordered_list_match:
            flush_paragraph()
            if list_type not in (None, "ol"):
                flush_list()
            list_type = "ol"
            list_items.append(ordered_list_match.group(2).strip())
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_list()
    if in_code_block:
        flush_code()
    if in_display_math:
        flush_display_math()
    if footnotes:
        footnote_items = "".join(
            (
                f'<li id="fn-{note_id}">'
                f"{render_inline(note_text, footnotes)} "
                f'<a href="#fnref-{note_id}" aria-label="Back to text">↩</a>'
                "</li>"
            )
            for note_id, note_text in footnotes.items()
        )
        blocks.append(f'<section class="footnotes"><ol>{footnote_items}</ol></section>')

    return "\n".join(blocks)


def load_post(path: Path) -> Post:
    metadata, body = parse_front_matter(path.read_text())
    title = metadata["title"]
    date = parse_post_datetime(metadata["date"])
    publish_at = (
        parse_post_datetime(metadata["publish_at"])
        if metadata.get("publish_at")
        else None
    )
    subtitle = metadata.get("subtitle", "")
    summary = metadata.get("summary", "")
    slug = slugify(path.stem.split("_", 1)[-1])
    return Post(
        slug=slug,
        title=title,
        date=date,
        publish_at=publish_at,
        subtitle=subtitle,
        summary=summary,
        body_html=render_markdown(body),
        source_name=path.name,
    )


def simplify_diary_text(text: str) -> str:
    replacements = [
        (r"`[^`]*referenda[^`]*`", "an elections and redistricting project"),
        (r"`[^`]*jakerbrown\.github\.io[^`]*`", "a personal academic website and blog"),
        (r"\bthis website\b", "a personal academic website and blog"),
        (r"`([^`]+)`", r"\1"),
        (r"\bcross-repo\b", "cross-project"),
        (r"\brepo-local\b", "project-level"),
        (r"\bon-disk guidance\b", "written guidance"),
        (r"\bspecialist-review roles\b", "review roles"),
        (r"\bdurable breadcrumbs\b", "saved notes"),
        (r"\bephemeral chat memory\b", "chat history"),
        (r"\bcentral digest workflow\b", "central summary workflow"),
        (r"\bparticipating repos\b", "participating projects"),
        (r"\blightweight overlay\b", "lighter setup"),
        (r"\brepo\b", "project"),
    ]

    def apply_replacements(value: str) -> str:
        updated = value
        for pattern, replacement in replacements:
            updated = re.sub(pattern, replacement, updated)
        updated = re.sub(r"\s+", " ", updated).strip()
        return updated

    def simplify_bullet(bullet: str) -> str:
        bullet = apply_replacements(bullet)

        bullet = re.sub(
            r"Mapped out and advanced a bigger Codex workflow upgrade in an elections and redistricting project, moving it from .*? with better structure and review support\.",
            "Advanced a Codex workflow upgrade for an elections and redistricting project, with better structure and review support.",
            bullet,
        )
        bullet = re.sub(
            r"Landed several practical an elections and redistricting project workflow improvements, including .*? future work is easier to recover and run consistently\.",
            "Added workflow improvements for an elections and redistricting project, with clearer guidance and review structure.",
            bullet,
        )
        bullet = re.sub(
            r"Built a reliable cross-project Codex diary system so daily work can be summarized from saved notes instead of chat history\.",
            "Built a cross-project Codex diary system so daily work can be summarized from saved notes instead of chat history.",
            bullet,
        )
        bullet = re.sub(
            r"Added a central summary workflow in this website, created standard breadcrumb folders across participating projects, and turned on a nightly Codex automation to write concise end-of-day diary entries\.",
            "Set up a nightly summary workflow on a personal academic website and blog so daily Codex work can be collected and turned into diary entries.",
            bullet,
        )
        bullet = re.sub(
            r"Set up a shared nightly summary workflow on this website so daily Codex work can be collected and turned into concise diary entries\.",
            "Set up a nightly summary workflow on a personal academic website and blog so daily Codex work can be collected and turned into diary entries.",
            bullet,
        )

        bullet = bullet.replace(
            " in an elections and redistricting project,",
            " for an elections and redistricting project,",
        )
        bullet = re.sub(r"\s+", " ", bullet).strip()
        if bullet and bullet[-1] not in ".!?":
            bullet += "."
        return bullet

    output_lines: list[str] = []
    current_bullet: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            if current_bullet is not None:
                output_lines.append(f"- {simplify_bullet(current_bullet)}")
                current_bullet = None
            continue
        if line.lstrip().startswith("### "):
            if current_bullet is not None:
                output_lines.append(f"- {simplify_bullet(current_bullet)}")
                current_bullet = None
            output_lines.append(line)
            continue
        if line.lstrip().startswith("- "):
            if current_bullet is not None:
                output_lines.append(f"- {simplify_bullet(current_bullet)}")
            current_bullet = line.lstrip()[2:].strip()
            continue
        if current_bullet is not None:
            current_bullet = f"{current_bullet} {line.strip()}"
        else:
            output_lines.append(apply_replacements(line))

    if current_bullet is not None:
        output_lines.append(f"- {simplify_bullet(current_bullet)}")

    return "\n".join(output_lines)


def is_publishable_diary_entry(body: str) -> bool:
    normalized = re.sub(r"\s+", " ", body).strip().lower()
    if not normalized:
        return False

    no_activity_phrases = (
        "no activity was found for the configured repos on this date.",
        "no codex work today.",
        "no codex activity today.",
        "no codex work was recorded today.",
        "no diary entry today.",
        "no claude or codex work today.",
        "no claude/codex activity today.",
    )
    if normalized in no_activity_phrases:
        return False

    bullet_lines = [
        line for line in body.splitlines() if line.lstrip().startswith("- ")
    ]
    if not bullet_lines:
        return False

    stripped_bullets = [
        re.sub(r"\s+", " ", line.lstrip()[2:].strip()).lower() for line in bullet_lines
    ]
    if stripped_bullets and all(
        bullet in no_activity_phrases for bullet in stripped_bullets
    ):
        return False

    return True


def load_codex_diary_posts() -> list[Post]:
    if not DIARY_PATH.exists():
        return []

    text = DIARY_PATH.read_text(encoding="utf-8")
    now = datetime.now()
    matches = list(
        re.finditer(
            r"^## (\d{4}-\d{2}-\d{2}(?: to \d{4}-\d{2}-\d{2})?)\n"
            r"(.*?)(?=^## \d{4}-\d{2}-\d{2}(?: to \d{4}-\d{2}-\d{2})?\n|\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
    )

    posts: list[Post] = []
    for match in matches:
        date_label = match.group(1)
        body = match.group(2).strip()
        if not is_publishable_diary_entry(body):
            continue

        if " to " in date_label:
            start_iso, end_iso = date_label.split(" to ", maxsplit=1)
            date = datetime.strptime(f"{end_iso} 21:30", "%Y-%m-%d %H:%M")
            start_date = datetime.strptime(start_iso, "%Y-%m-%d")
            display_date = (
                f"{start_date.strftime('%B')} {start_date.day}, {start_date.year}"
                f" to {date.strftime('%B')} {date.day}, {date.year}"
            )
            subtitle = "AI summary of the last three days of Claude and Codex work."
            slug = f"codex-diary-{start_iso}-to-{end_iso}"
        else:
            date = datetime.strptime(f"{date_label} 21:30", "%Y-%m-%d %H:%M")
            display_date = f"{date.strftime('%B')} {date.day}, {date.year}"
            subtitle = "AI summary of today's Claude and Codex work."
            slug = f"codex-diary-{date_label}"
        if date > LAST_PUBLIC_DIARY_DATE:
            continue
        if date > now:
            continue
        simplified_body = simplify_diary_text(body)
        posts.append(
            Post(
                slug=slug,
                title=f"Claude/Codex diary - {display_date}",
                date=date,
                publish_at=None,
                subtitle=subtitle,
                summary="",
                body_html=render_markdown(simplified_body),
                source_name=f"files/codex-diary/diary.md#{date_label}",
            )
        )

    return posts


def page_path(page_number: int) -> Path:
    if page_number == 1:
        return BLOG_DIR / "index.html"
    return PAGE_DIR / str(page_number) / "index.html"


def page_url(page_number: int) -> str:
    if page_number == 1:
        return "/blog/"
    return f"/blog/page/{page_number}/"


def page_template(title: str, body: str, description: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description, quote=True)}">
    <link rel="stylesheet" href="/css/site-base.css">
    <link rel="stylesheet" href="/css/blog.css">
    <script>
      window.MathJax = {{
        tex: {{
          inlineMath: [['$', '$']],
          displayMath: [['$$', '$$']],
          processEscapes: true
        }},
        options: {{
          skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
        }}
      }};
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
  </head>
  <body>
    <div class="content blog-content">
{body}
    </div>
  </body>
</html>
"""


def render_post(post: Post, page_number: int) -> str:
    permalink = f"{page_url(page_number)}#{post.slug}"
    summary_html = ""
    if post.summary:
        summary_html = f'\n        <p class="blog-summary">{render_inline(post.summary)}</p>'
    footer_html = f'\n        <p class="post-meta">Posted: {post.display_timestamp}</p>'
    subtitle_html = ""
    if post.subtitle:
        subtitle_html = f'\n        <p class="post-subtitle">{render_inline(post.subtitle)}</p>'
    return f"""      <article id="{post.slug}" class="post-card">
        <h2 class="post-card-title"><a href="{permalink}">{html.escape(post.title)}</a></h2>
        {subtitle_html}{summary_html}
        <div class="post-body">
          {post.body_html.replace(chr(10), chr(10) + "          ")}
        </div>{footer_html}
      </article>"""


def render_pagination(current_page: int, total_pages: int) -> str:
    if total_pages <= 1:
        return ""

    links: list[str] = []
    if current_page > 1:
        links.append(f'<a href="{page_url(current_page - 1)}">Newer Posts</a>')
    if current_page < total_pages:
        links.append(f'<a href="{page_url(current_page + 1)}">Older Posts</a>')

    joined = " | ".join(links)
    return f"""      <nav class="pagination" aria-label="Blog pagination">
        <p>{joined}</p>
      </nav>
"""


def build_page(page_number: int, posts: list[Post], total_pages: int) -> None:
    rendered_posts = "\n".join(render_post(post, page_number) for post in posts)
    body = f"""      <p class="site-links"><a href="/">Home</a> | <a href="mailto:jbrown13@bu.edu">Email</a></p>
      <p class="lede">Data science, teaching, and other stuff.</p>
{rendered_posts}
{render_pagination(page_number, total_pages)}"""
    description = "Data science, teaching, and other stuff."
    path = page_path(page_number)
    path.parent.mkdir(parents=True, exist_ok=True)
    title = "Blog" if page_number == 1 else f"Blog | Page {page_number}"
    path.write_text(page_template(title, body, description))


def clean_generated_dirs(total_pages: int) -> None:
    posts_dir = BLOG_DIR / "posts"
    if posts_dir.exists():
        shutil.rmtree(posts_dir)

    if PAGE_DIR.exists():
        for child in PAGE_DIR.iterdir():
            if child.is_dir() and child.name.isdigit() and int(child.name) > total_pages:
                shutil.rmtree(child)


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    BLOG_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    posts = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        post = load_post(path)
        visible_at = post.publish_at or post.date
        if visible_at > now:
            continue
        posts.append(post)
    posts.extend(load_codex_diary_posts())
    posts.sort(key=lambda post: post.date, reverse=True)

    total_pages = max(1, math.ceil(len(posts) / POSTS_PER_PAGE))
    clean_generated_dirs(total_pages)

    for page_number in range(1, total_pages + 1):
        start = (page_number - 1) * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        build_page(page_number, posts[start:end], total_pages)

    print(f"Built {len(posts)} blog post(s) across {total_pages} page(s).")
    for page_number in range(1, total_pages + 1):
        print(f"- {page_path(page_number).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
