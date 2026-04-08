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


@dataclass
class Post:
    slug: str
    title: str
    date: datetime
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


def render_inline(text: str) -> str:
    escaped = html.escape(text)
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
    return escaped


def render_markdown(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    in_code_block = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(line.strip() for line in paragraph)
            blocks.append(f"<p>{render_inline(text)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            items = "".join(f"<li>{render_inline(item)}</li>" for item in list_items)
            blocks.append(f"<ul>{items}</ul>")
            list_items = []

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            code = "\n".join(html.escape(line) for line in code_lines)
            blocks.append(f"<pre><code>{code}</code></pre>")
            code_lines = []

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

        if not line.strip():
            flush_paragraph()
            flush_list()
            continue

        if list_items and raw_line[:1].isspace() and not line.lstrip().startswith("- "):
            list_items[-1] = f"{list_items[-1]} {line.strip()}"
            continue

        if line.startswith("# "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h2>{render_inline(line[2:].strip())}</h2>")
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h3>{render_inline(line[3:].strip())}</h3>")
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h4>{render_inline(line[4:].strip())}</h4>")
            continue

        if line.startswith("> "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<blockquote><p>{render_inline(line[2:].strip())}</p></blockquote>")
            continue

        if line.startswith("- "):
            flush_paragraph()
            list_items.append(line[2:].strip())
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_list()
    if in_code_block:
        flush_code()

    return "\n".join(blocks)


def load_post(path: Path) -> Post:
    metadata, body = parse_front_matter(path.read_text())
    title = metadata["title"]
    date = parse_post_datetime(metadata["date"])
    subtitle = metadata.get("subtitle", "")
    summary = metadata.get("summary", "")
    slug = slugify(path.stem.split("_", 1)[-1])
    return Post(
        slug=slug,
        title=title,
        date=date,
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

    paragraphs: list[str] = []
    bullets: list[str] = []
    current_bullet: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            if current_bullet is not None:
                bullets.append(simplify_bullet(current_bullet))
                current_bullet = None
            continue
        if line.lstrip().startswith("- "):
            if current_bullet is not None:
                bullets.append(simplify_bullet(current_bullet))
            current_bullet = line.lstrip()[2:].strip()
            continue
        if current_bullet is not None:
            current_bullet = f"{current_bullet} {line.strip()}"
        else:
            paragraphs.append(apply_replacements(line))

    if current_bullet is not None:
        bullets.append(simplify_bullet(current_bullet))

    output_lines: list[str] = []
    for paragraph in paragraphs:
        output_lines.append(paragraph)
    for bullet in bullets:
        output_lines.append(f"- {bullet}")
    return "\n".join(output_lines)


def load_codex_diary_posts() -> list[Post]:
    if not DIARY_PATH.exists():
        return []

    text = DIARY_PATH.read_text(encoding="utf-8")
    matches = list(
        re.finditer(
            r"^## (\d{4}-\d{2}-\d{2})\n(.*?)(?=^## \d{4}-\d{2}-\d{2}\n|\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
    )

    posts: list[Post] = []
    for match in matches:
        iso_date = match.group(1)
        body = match.group(2).strip()
        if not body:
            continue

        date = datetime.strptime(f"{iso_date} 21:30", "%Y-%m-%d %H:%M")
        display_date = date.strftime("%B %-d, %Y")
        subtitle = "AI summary of today's Codex work."
        simplified_body = simplify_diary_text(body)
        posts.append(
            Post(
                slug=f"codex-diary-{iso_date}",
                title=f"Codex diary - {display_date}",
                date=date,
                subtitle=subtitle,
                summary="",
                body_html=render_markdown(simplified_body),
                source_name=f"files/codex-diary/diary.md#{iso_date}",
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
    subtitle_html = ""
    if post.subtitle:
        subtitle_html = f'\n        <p class="post-subtitle">{render_inline(post.subtitle)}</p>'
    meta_html = f'\n        <p class="post-meta">{post.display_timestamp}</p>'
    if post.subtitle:
        meta_html = ""
    return f"""      <article id="{post.slug}" class="post-card">
        <h2 class="post-card-title"><a href="{permalink}">{html.escape(post.title)}</a></h2>
        {meta_html}{subtitle_html}{summary_html}
        <div class="post-body">
          {post.body_html.replace(chr(10), chr(10) + "          ")}
        </div>
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

    posts = [load_post(path) for path in sorted(SOURCE_DIR.glob("*.md"))]
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
