Worked on the blog ordering and diary timing before the evening diary entry is
ready.

Changed the blog generator so Codex diary entries only appear once the local
build time has actually reached their 9:30 PM publish timestamp. Also moved the
Philip Roth post later in the evening so it appears above the Claude workflow
post on the blog page.

This matters because the temporary diary draft is no longer showing up early,
and the featured post order now matches the launch priority.

Verified by rebuilding with `python3 scripts/build_blog.py` and checking that
`blog/index.html` shows three posts, with the Philip Roth post first and no
Codex diary entry yet.
