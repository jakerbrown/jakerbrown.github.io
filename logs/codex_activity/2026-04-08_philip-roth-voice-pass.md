Worked on a voice cleanup pass for the Philip Roth post.

Rewrote the first-person research language so the analysis and methods are
described as Codex's work, while Goodreads and reading-history references are
described as Jacob's. Rebuilt the blog page so the generated site reflects the
same wording.

This matters because the post now attributes the research process and the book
history more clearly and consistently.

Verified by rebuilding with `python3 scripts/build_blog.py` and checking the
updated wording in both the source post and `blog/index.html`.
