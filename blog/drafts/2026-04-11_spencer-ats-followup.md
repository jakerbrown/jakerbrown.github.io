---
title: Automation experiment IV: Spencer wanted to know if this held up against the spread
subtitle: Jacob: This is a direct follow-up to the original Spencer betting post. The first pass asked about moneyline underdogs. Spencer then asked the sharper next question: what happens against the spread? This extension was again run by Codex, with the main caveat that the public archive stores NFL and NBA spreads but not the associated spread juice, so the primary ATS analysis uses the standard `-110` assumption.
date: 2026-04-11 15:30
summary: A real against-the-spread follow-up weakens the case for Spencer's theory and leaves, at most, a very noisy NFL subgroup hint.
---

After the first Spencer post went up, Spencer asked the natural follow-up:
fine, but does this hold up **against the spread**?

That is not just a betting-terminology cleanup. It changes the question.

On the moneyline, underdogs get paid more when they win. Against the spread,
most of that payout asymmetry disappears. So if the original theory was really
about market learning, and not just about moneyline payout geometry, some
version of it should survive when the bet becomes "take the points with the
dog" rather than "bet the dog to win outright."

So I ran that extension.

The cleanest public version turns out to split in two.

- **Primary ATS study**: NFL and NBA only, using closing spreads.
- **Handicap extension**: NHL puckline-style and MLB runline-style markets,
  reported separately because they are related to ATS, not identical to it.

There is one important seam in the public data. The archive I used stores NFL
and NBA closing spreads, but not the associated ATS juice. So for the primary
ATS analysis I used the standard market assumption of `-110` on both sides. For
NHL and MLB, the archive does store the handicap odds directly. I also had to
drop obviously malformed spread rows, which removed 264 NFL games and 936 NBA
games from the raw archive.

That matters, but it does not rescue the main result.

## The headline result

For the **primary ATS study** of NFL and NBA, betting every early-season
underdog against the spread still did not produce a clean positive pooled
result.

- first 2 weeks: ROI `-0.015`, `1338` bets
- first 3 weeks: ROI `-0.017`, `2000` bets
- first 3 weeks 95 percent bootstrap interval:
  `[-0.060, 0.034]`
- closest pooled primary window: first 5 games at ROI `0.002`,
  still with an interval that includes ordinary losses

That is a disciplined negative result. Under a standard `-110` assumption, the
early-underdog ATS story still looks more interesting than generic underdog
betting, but not clearly profitable.

The ROI figure below shows the early windows by league and market family.

![ATS ROI by window](/files/spencer-underdog-betting/fig_ats_roi_by_window.png)

## Better than generic ATS underdog betting, still short of a real edge

The comparison that matters is not whether early dogs sometimes look okay in a
small sample. It is whether they beat the relevant alternatives.

In the primary ATS sample:

- early 3-week underdogs: ROI `-0.017`
- all ATS underdogs over the season proxy: ROI `-0.036`

So early ATS dogs do look **less bad** than ATS underdogs in general. That is
weak directional evidence for a small early-season information story, not a
positive result. Both strategies still lose under the standard `-110`
assumption, and the primary sample does not use observed NFL/NBA spread juice.

For reference, the first 3-week pooled cover rate excluding pushes was
`0.515`. At `-110`, break-even is about
`0.524`. So the pooled ATS sample still falls short, though not by a wide
margin. That is another reason not to over-read the negative ROI as a precisely
measured market fact.

The threshold-comparison figure makes that visible.

![ATS threshold comparison](/files/spencer-underdog-betting/fig_ats_calibration.png)

## The league split

The primary ATS split is simpler than the original moneyline story:

- NFL, first 3 weeks: ROI `0.029`, 95 percent interval `[-0.036, 0.095]`
- NBA, first 3 weeks: ROI `-0.032`

So if there is an ATS version of Spencer's idea, it is much more plausible in
the NFL than in the NBA. But the NFL sample is also much smaller, and its
interval still comfortably includes no edge. This is exactly the kind of
league-specific positive point estimate that should be read carefully rather
than celebrated.

The forest plot below shows the raw and shrunk league estimates.

![ATS forest plot](/files/spencer-underdog-betting/fig_ats_forest_plot.png)

## What about MLB and NHL?

I did run the closest public analogue using archived `1.5` handicap markets,
but only on the moneyline-underdog side. Those should not be treated as
identical to true ATS, so I am labeling them as a companion extension rather
than folding them into the primary pooled claim.

In the first 3 weeks:

- MLB handicap underdogs: ROI `-0.004`
- NHL handicap underdogs: ROI `-0.046`

That is basically a flat-to-negative picture, not a second source of support.

## Bottom line

The against-the-spread follow-up weakens the broadest version of Spencer's
theory.

The most honest summary is:

1. the moneyline result was already only a weak hint, not a proven edge
2. the pooled ATS follow-up for NFL and NBA is still negative
3. NFL shows a directionally positive subgroup estimate, but it is too noisy to
   lean on
4. MLB and NHL handicap markets do not add much support

So if Spencer's idea contains something real, it looks less like a universal
"bet early underdogs" rule and more like a tentative hypothesis about a subset
of early NFL underdogs. Even that narrower reading is weak and uncertain rather
than established. That is a much smaller statement than the original theory,
and it is where I would stop unless better public spread-price data show
something stronger.
