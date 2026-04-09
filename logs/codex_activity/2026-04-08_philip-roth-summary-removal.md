Worked on a small cleanup to the Philip Roth post summary.

Removed the one-sentence summary text from the post front matter and rebuilt
the generated blog page so that summary no longer appears on the blog index.

This matters because the post now opens directly with the title, subtitle, and
body without the extra summary line.

Verified by rebuilding with `python3 scripts/build_blog.py` and confirming the
old summary sentence no longer appears in the source post or `blog/index.html`.
