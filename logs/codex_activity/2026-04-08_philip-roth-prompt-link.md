Worked on replacing the Philip Roth post's prompt placeholder with a real
public link.

Published the prompt file in the workflow repo, then updated the site post to
link to the live `CODEX_PROMPT.md` file on GitHub and rebuilt the generated
blog page.

This matters because readers can now open the original prompt directly from the
post instead of seeing a placeholder.

Verified by rebuilding with `python3 scripts/build_blog.py` and confirming the
GitHub prompt URL appears in the source post.
