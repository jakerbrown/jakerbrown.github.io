Worked on publishing the Spencer underdog betting post from drafts into the live blog source folder.

Changed the post location from `blog/drafts/` to `blog/posts-src/`, rebuilt the blog pages, and confirmed the generated main blog page now includes the Spencer post with its linked figures.

This mattered because the post existed as a draft but was not part of the published blog build, so it would not go live without a publish commit.

Verified that the rebuild succeeded, that `blog/index.html` contains the Spencer post, and that the three referenced figure files exist under `files/spencer-underdog-betting/`. I did not verify the deployed site over the network in this run.
