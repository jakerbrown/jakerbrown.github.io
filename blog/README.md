# Blog workflow

Write posts in `blog/posts-src/` as Markdown files named like
`YYYY-MM-DD_slug.md`.

Each post should start with:

```md
---
title: Your Title
date: 2026-04-08 09:00
summary: One-sentence summary for the page and metadata.
---
```

The `date` field can be either `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`. Including a
time is the best way to preserve ordering when multiple posts happen on the
same day.

Then add the body in Markdown below the front matter.

To publish a new post:

1. Add a new Markdown file in `blog/posts-src/`.
2. Run `python3 scripts/build_blog.py`.
3. Commit the source file and the generated files under `blog/`.
4. Push to GitHub Pages as usual.

The generator rebuilds the blog as paginated long-form pages:

- `blog/index.html` for the newest posts
- `blog/page/2/index.html`, `blog/page/3/index.html`, and so on for older posts

Posts are rendered on those pages directly rather than as separate standalone
post URLs.

The generator also automatically includes dated entries from
`files/codex-diary/diary.md` as blog posts titled `Codex diary`, using the
entry date as the subtitle.
