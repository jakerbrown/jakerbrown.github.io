Worked on the Philip Roth blog post link update and site rebuild.

Changed the Roth source post to use the corrected replication link and fixed
the prompt link, then updated the blog generator so future-dated source posts
do not publish early. Moved the coyote post to tomorrow morning and rebuilt the
site.

This matters because the Roth post can go live now without accidentally
publishing the coyote post ahead of schedule.

Verified by rebuilding with `python3 scripts/build_blog.py` and checking that
the generated blog index includes the Roth post but not the coyote post.
