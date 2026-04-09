Updated the Philip Roth blog post to use the canonical public repository URL
for the replication package.

Changed the prompt and replication links from the moved
`jakerbrown/claude-code-my-workflow` repo path to
`jakerbrown/codex-my-workflow`, then rebuilt the blog.

This matters because the old links redirect, but the canonical path is clearer
for readers and avoids confusion about where the public code actually lives.

Verified by rebuilding with `python3 scripts/build_blog.py` and checking that
the rendered Roth post now points at `jakerbrown/codex-my-workflow`.
