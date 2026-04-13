Removed the "Related file" lines from the place-effects blog post while keeping the DAG images.

Edited the published post source to drop the extra file-link lines under each image, rebuilt the blog pages, and checked that the generated HTML now keeps only the embedded images.

This mattered because those extra lines were clutter around figures that already had the relevant image right there in the post.

Verified that the rebuilt `blog/index.html` no longer includes any `Related file:` lines for this post. I left the images and the rest of the post unchanged.
