Adjusted the same-day blog post ordering so the Philip Roth post stays above
the Claude-to-Codex post once both are visible.

Changed the Claude/Codex source post timestamp to slightly earlier than the
Roth post, rebuilt the blog index, and checked the rendered order.

This matters because same-day posts are ordered by timestamp, and the desired
launch order was Roth first, Claude second, with the coyote post still held for
tomorrow.

Verified by rebuilding with `python3 scripts/build_blog.py` and confirming in
`blog/index.html` that the Roth post appears above the Claude/Codex post.
