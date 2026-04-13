Worked on the Codex diary cadence and window size.

Changed the diary automation and repo-side diary tooling so the active Codex
diary now runs every three days and prepares a three-day digest instead of a
single-day one. Updated the supporting docs and blog-side diary parsing so
date-range diary entries still render cleanly.

This mattered because the scheduler and the digest logic needed to agree on the
same window, or the automation would have kept producing one-day diary posts on
a three-day schedule.

Verified by updating the active automation in Codex, running a sample
three-day digest, compiling the touched Python scripts, and rerunning the diary
style check. I did not rebuild the whole blog in this pass.
