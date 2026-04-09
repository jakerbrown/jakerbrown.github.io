Fixed blog footnote rendering so Markdown footnotes no longer appear as raw `[^1]` text in published posts.

Added basic footnote support to the blog generator and rebuilt the site to verify the Knausgaard post now shows a linked superscript note with a footnote block.

This mattered because the live post was showing raw Markdown instead of readable note formatting, which made the post look broken.

Verified the generated homepage renders the Knausgaard note correctly. I did not commit or push because `scripts/build_blog.py` already had other uncommitted local changes mixed into the same file.
