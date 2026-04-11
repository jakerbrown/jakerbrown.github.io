Worked on rebuilding and publishing the site so the latest posts can go live.

Changed the generated site output by rerunning the blog build, then prepared a
publish commit from the refreshed files in the site repo.

This mattered because recent source changes do not show up on the live site
until the generated pages are rebuilt and pushed.

Verification for this pass was the local site rebuild plus a review of the git
diff before committing. Live deployment depends on the push reaching GitHub
Pages.
