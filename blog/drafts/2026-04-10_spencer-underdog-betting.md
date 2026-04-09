---
title: Automation experiment III: Did Spencer's early-season underdog strategy ever work?
subtitle: Jacob: This research was conducted entirely, in both coding, methods decisions, and writeup, by Codex. This was not a complete one-shot. I pushed Codex to tighten the claims, add benchmark comparisons, build a replication package, and survive specialist plus adversarial review. You can find the original prompt here: [CODEX_PROMPT.md](https://github.com/jakerbrown/codex-my-workflow/blob/main/explorations/spencer-underdog-betting/CODEX_PROMPT.md)
date: 2026-04-10 12:00
summary: 
---

Spencer's theory has the virtue of sounding plausible before it sounds profitable. Early in a season, sportsbooks and bettors are still leaning on priors: last year's record, offseason narratives, roster headlines, vague expectations of continuity or collapse. If the market has not learned enough yet, some teams priced as underdogs should really be closer to coin flips. And when underdogs win, they pay more. A small probability mistake can matter a lot.

That logic is clean. The question is whether it actually worked in real historical betting data once bookmaker hold, league differences, and ordinary variance are taken seriously.

So Codex built a public-data test.

The project assembled a game-level closing-moneyline archive for the NFL, NBA, NHL, and MLB from 2011 through 2021 using a documented public GitHub archive of sportsbook data. The final cleaned panel contains 53,453 games across 44 league-seasons. The goal was not to find the single best backtested rule after the fact. The goal was to ask a narrower question honestly: if you had simply bet early-season underdogs, would that have made money often enough to deserve belief as a real edge?

The bottom line is careful but fairly clear. Spencer's rule looks better than generic underdog betting, and it may contain a small early informational effect, especially in MLB and maybe NFL. But the observed data do not support a strong claim that early-season underdogs were a robust cross-league money machine.

If you want the replication materials, code, intermediate outputs, and notes, they live here: [replication folder for this analysis](https://github.com/jakerbrown/codex-my-workflow/tree/main/explorations/spencer-underdog-betting). The main executable pipeline is [`src/run_analysis.py`](https://github.com/jakerbrown/codex-my-workflow/blob/main/explorations/spencer-underdog-betting/src/run_analysis.py), with an R-side robustness check in [`src/robustness_meta_analysis.R`](https://github.com/jakerbrown/codex-my-workflow/blob/main/explorations/spencer-underdog-betting/src/robustness_meta_analysis.R).

## The method, in plain English

Codex started with the cleanest common public historical source it could find across all four leagues: the `flancast90/sportsbookreview-scraper` archive on GitHub. That source is imperfect. The strongest cross-league public window it supports consistently is 2011 through 2021, and it does not provide a perfect official season-type flag across leagues. But it does give dates, final scores, and closing moneylines for both sides of each game, which is enough to run a serious first-pass historical test.

The strategy definitions were fixed early in the workflow before reading the output tables. Codex compared several natural versions of "early season":

1. First 2 calendar weeks.
2. First 3 calendar weeks.
3. First 5 games played by the betting team.
4. First 10 percent of the team-season proxy.

The main strategy was as transparent as possible:

- bet $100 on every qualifying underdog
- settle the bet at the closing moneyline
- compare the realized profit with sensible alternatives

Those alternatives mattered. Codex did not just report one ROI number and declare victory or failure. It compared Spencer's idea with:

- all underdogs over the likely-regular-season proxy
- favorites in the same early windows
- random teams in the same early windows
- later-season underdogs
- a timing-placebo benchmark that permutes when underdog bets occur within season

It also did the more important thing that betting arguments often skip: check calibration. Underdogs can sometimes look good in realized ROI just because payouts are asymmetric. The sharper question is whether they actually won more often than the no-vig market implied.

## The headline result

The strongest naive pooled rule in this run was "bet every underdog in the first 3 calendar weeks." That rule still did not deliver a clean positive result.

- ROI: -0.4%
- bets: 5,901
- 95% bootstrap interval: [-4.0%, 3.4%]

That is the kind of estimate that should slow down anyone who wants a triumphalist answer. It is close to breakeven. The interval still includes modest gains, but it also includes ordinary losses. There is no disciplined way to call that a proven positive edge.

The pooled ROI figure below shows the main windows side by side.

![ROI by league and early-season window](/files/spencer-underdog-betting/fig_roi_by_window.png)

## Better than generic underdog betting, but still not a gold mine

Where Spencer's idea does look interesting is in relative rather than absolute terms.

Compared with the early 3-week underdog rule:

- all underdogs over the likely-regular-season proxy lost 1.8%
- early favorites lost 4.1%
- a random team in the same early window also did worse on average
- permuted underdog timing also looked worse than the actual early window

That pattern is consistent with a small early informational story. Early underdogs seem to be less overpriced than underdogs in general. But that is not the same thing as showing a durable positive betting edge after vig.

So the right reading is not "this made money." It is closer to: "this lost less than the obvious alternatives, and maybe for a real reason."

## The league split

The four-league breakdown is where the story gets more interesting and more dangerous.

Early 3-week underdog ROI by league:

- MLB: +3.9%
- NFL: +1.8%
- NBA: -0.4%
- NHL: -8.2%

On a casual read, that looks like a simple story: maybe the edge is in MLB and NFL, maybe not in NBA, definitely not in NHL. But the project did not stop at casual reads. Codex fit a partial-pooling summary that shrinks league-specific results back toward the pooled mean, because these league-by-league splits are noisy and should not be treated as four isolated truths.

That shrinkage matters. It means the right interpretation is:

- MLB is the strongest positive hint.
- NFL is also directionally positive, but on a much smaller sample.
- NBA is basically flat.
- NHL is the clearest negative case.

The forest plot below shows the raw league estimates and the shrunk versions together.

![League-specific early-underdog estimates](/files/spencer-underdog-betting/fig_forest_plot.png)

This is also where a broader domain story starts to wobble. If the mechanism were something simple like "short seasons create more mispricing" or "continuity helps market learning," the league pattern would likely line up more cleanly than this. It does not. That is another reason to stay modest.

## The key evidence is calibration, not just ROI

The most useful part of the analysis is probably the calibration check.

For pooled early 3-week underdogs:

- realized win rate: 40.45%
- no-vig implied win probability: 39.70%
- calibration gap: +0.75 percentage points

That is a favorable sign. Early underdogs did win slightly more often than the de-vigged market implied. But the gap is small.

The calibration plot below makes the point visually.

![Calibration of early underdogs versus the rest of the season](/files/spencer-underdog-betting/fig_calibration.png)

League-level calibration gaps follow the same basic pattern as the ROI splits:

- MLB: +2.14 points
- NFL: +2.69 points
- NBA: +0.65 points
- NHL: -2.15 points

This is why the most defensible conclusion is not "the strategy failed completely." It is "the market may have been mildly too low on some early underdogs, but not by enough to create a strong cross-league historical profit claim."

## The one refined variant that looks tempting

There was one result in the package that could easily tempt someone into overclaiming: bigger underdogs in the first 3 weeks.

- `big_dog_3w`: ROI +4.2%

This is exactly the sort of result that deserves suspicion rather than celebration. It appears after testing multiple plausible windows and variants. Its confidence interval is still wide. NHL moves sharply against it. The whole thing is vulnerable to the usual p-hacking problem of selecting the tail bucket that happens to look best.

So Codex treated that result as exploratory. Interesting, yes. Bankable, no.

## Kelly sizing does not rescue the story

Codex also ran a leave-one-season-out half-Kelly exercise using out-of-sample predicted win probabilities. If there were a meaningful exploitable edge, a more disciplined stake size should help.

It barely did:

- half-Kelly, 2 weeks: +0.1%
- half-Kelly, 3 weeks: +0.2%

That is basically breakeven. It reinforces the broader conclusion: whatever signal may exist here is small.

## What the simulation adds

Because the underlying theory is about learning, Codex added a stylized market-learning simulation with:

- preseason strength priors
- slow or fast market updating
- a possible public premium on favorites

The simulation shows that early underdogs *can* become profitable in a world where the market updates slowly and favorites are slightly overpriced. That makes Spencer's idea coherent in theory.

But the simulation is a mechanism illustration, not calibrated proof. The historical data are directionally compatible with a small version of that story, not enough to claim that the simulation quantitatively explains observed betting outcomes.

## What this does and does not show

It does **not** show that betting early underdogs was a reliable profit strategy across the major U.S. leagues.

It *does* show three more limited things:

1. Early underdogs performed better than generic underdog betting.
2. They may have benefited from a small early informational effect in some leagues.
3. That effect was not large or stable enough to produce a convincing historical edge once vig and uncertainty are taken seriously.

That is a more interesting answer than either extreme. The strategy was not obviously silly. It just was not a clean money printer.

## The takeaway

If you want the shortest version:

- Spencer's idea was plausible.
- The data weakly support a mild early-season underpricing story.
- The strongest hints are in MLB and maybe NFL.
- The pooled evidence does not support a robust cross-league claim that early-season underdog betting made money.

That is where I would land after looking at the tables, the calibration evidence, the benchmarks, the shrinkage, the Kelly exercise, and the adversarial review: probably no durable all-league edge, but a real enough hint to make the theory worth taking seriously as a research question.
