Worked on a small wording cleanup in the Claude-to-Codex blog post.

Changed the line introducing the repository link from `Public repo:` to `You
can find the repo for this project here:` and rebuilt the generated blog page
so the visible site matches the source post.

This matters because the link now reads more naturally in the post body.

Verified by rebuilding with `python3 scripts/build_blog.py` and checking the
updated sentence in `blog/index.html`.
