Worked on cleaning up the repo so the blog section can be launched from this
site without hidden generated files or broken post rendering.

Changed the ignore rules so the blog index, post sources, and blog README are
no longer hidden from git, while Python cache files stay ignored. Also updated
the lightweight blog generator so it correctly renders numbered lists and
images, then rebuilt the blog output.

This matters because the site is a static publish flow: the generated blog page
needs to be tracked, and newer posts with figures need to render correctly once
deployed.

Verified that `python3 scripts/build_blog.py` completes successfully and
rebuilds `blog/index.html` with the current posts. I did not create a commit or
push anything yet.
