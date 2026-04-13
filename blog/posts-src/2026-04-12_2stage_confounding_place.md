---
title: Parallel confounding in identification of place effects
subtitle:
date: 2026-04-12 11:00
summary:
---

Suppose I want to know whether some characteristic of a place $X_p$ — say, racial context — affects an individual outcome $Y_i$, like vote choice. Two things can go wrong, and they are different problems.

First, people sort into places. If the kind of person who moves to a high-$X$ place would have had different outcomes regardless, then comparing across places confounds $X$ with individual selection. This is the standard worry in observational causal inference: place assignment is endogenous.

Second, places are bundles. A neighborhood with high $X$ also has particular schools, crime rates, pollution levels, social networks, and dozens of other attributes that co-vary with $X$ across places. Even if I solve the selection problem perfectly, I still cannot tell whether it is $X$ or something bundled with $X$ that drives the outcome.

The first problem is about who lives where. The second is about what places are. They require different solutions, and most identification strategies only solve one.

## The two paths

Call the first problem Path 1 (individual selection into place) and the second Path 2 (overlapping place characteristics). In DAG terms:

**Path 1:** $X_p \leftarrow P_i \leftarrow \mathbf{W}_i \rightarrow Y_i$

Individuals with pre-treatment characteristics $\mathbf{W}_i$ sort into places non-randomly, and $X_p$ inherits a spurious correlation with $Y_i$ through the sorting process.

**Path 2:** $X_p \leftarrow P_i \rightarrow \mathbf{Z}_p \rightarrow Y_i$

Place jointly determines $X_p$ and every other place characteristic $\mathbf{Z}_p$. Variation in $X$ across places is bundled with variation in $\mathbf{Z}$.

![Two-stage confounding DAG](/files/two_stage_confounding_dag.svg)

Two things worth noting. First, Path 1 can be innocuous for a specific $X$ even when place assignment is endogenous. If people sort on job opportunities but $X$ is annual rainfall, the selection path may not matter for $X$. Second, identifying the overall effect of place ($\tau^{\text{place}}$) only requires closing Path 1. Identifying the effect of a *specific characteristic* ($\tau^X$) requires closing both.

The typical case is that both paths are open, which makes causal claims about place characteristics doubly hard. Here is how four common identification strategies fare.

## Randomized relocation

The [Moving to Opportunity](https://www.cambridge.org/core/journals/american-political-science-review/article/longterm-effects-of-neighborhood-disadvantage-on-voting-behavior-the-moving-to-opportunity-experiment/4896C6743CF5D53DDD067D51D93A8CA7) experiment randomly assigned housing vouchers, inducing some families to move from high-poverty to lower-poverty neighborhoods. Randomization closes Path 1 completely — no functional form assumptions, no conditional independence, no parallel trends.

But the experiment randomizes access to a *bundle* of neighborhood characteristics, not to $X$ specifically. Families who used their voucher moved to places that differed from their origin neighborhoods in poverty, school quality, crime, pollution, and much else, all at once. The estimated treatment effect captures the composite:

$$\tau^{\text{LATE}} = f\big(\Delta X, \Delta \mathbf{Z}\big)$$

Path 2 remains wide open. The experiment tells us whether neighborhoods matter. It cannot tell us what about neighborhoods matters. This is worth emphasizing because people sometimes treat randomization as settling the question. It settles assignment; it does nothing to separate components within bundles.

![Randomized relocation DAG](/files/dag_a_mto_experiment.svg)

## Childhood mover design

The [childhood mover design](https://jacobrbrown.com/files/w31759.pdf) compares children who move between the same origin and destination at different ages. Those who move younger get a higher "dose" of the destination. The identifying assumption is that, conditional on origin-destination pair and family characteristics, the age at move is as-if randomly assigned. This is credible enough to identify $\mu_p$, the causal exposure effect of place $p$ per year of childhood.

The problem is that $\hat{\mu}_p$ captures the effect of everything about place $p$ — the full bundle. Researchers often regress $\hat{\mu}_p$ on $X_p$ in a second stage to isolate the role of a specific characteristic, but that regression is subject to Path 2 confounding: $\text{Cov}(X_p, \mathbf{Z}_p) \neq 0$ across places. I have used this design in my own work, so I am not criticizing it — I am saying that the second stage is where the hard problem lives.

![Childhood mover DAG](/files/dag_a_childhood_mover.svg)

## Difference-in-differences

[Difference-in-differences](https://link.springer.com/article/10.1007/s11109-020-09626-1) exploits within-place changes in $X$ over time, using individual or place fixed effects to absorb time-invariant confounders. Fixed effects absorb the time-invariant component of individual selection (Path 1) and the time-invariant component of overlapping place characteristics (Path 2). What remains is confounding from co-trending characteristics: if $\mathbf{Z}_p$ changes at the same time and in the same places as $X_p$, the backdoor path is open through those co-movements.

So DiD partially addresses both paths but fully closes neither. The parallel trends assumption has to do double duty, covering both selection on trends in potential outcomes and the possibility that other place characteristics co-move with $X$. Whether that is plausible depends on how much the researcher knows about what else changed in the treated places.

![Difference-in-differences DAG](/files/dag_b_difference_in_differences.svg)

## Spatial regression discontinuity

A [spatial RD](https://www.econometricsociety.org/publications/econometrica/2025/11/01/Gangs-Labor-Mobility-and-Development) exploits a boundary where $X$ changes discontinuously. Individuals just on either side of the boundary are comparable (Path 1 closed by the continuity assumption), and if $X$ jumps at the boundary but other place characteristics $\mathbf{Z}_p$ do not, then the local variation in $X$ is free of Path 2 confounding.

This is the strongest resolution of Path 2 among these four designs. But it depends entirely on the boundary being "clean" — only $X$ discontinuous, everything else smooth. If the boundary is a state border and multiple policies change at the same line, you are back to the bundling problem.

![Spatial regression discontinuity DAG](/files/dag_c_spatial_rd.svg)

## Path 2 as a construct validity problem

In many settings $X_p$ does not vary independently of $\mathbf{Z}_p$ even in principle, so the effect of a specific place characteristic may not be point-identified without functional form assumptions. In practice, Path 2 is a construct validity problem. A design gives you credible variation in something, and whether that something corresponds to the theoretical construct you care about is a separate claim — like a survey experiment that aims to prime one emotion but may prime others alongside it. When clean identification is not available, researchers fall back to [inference to the best explanation](https://arthurspirling.org/documents/whatgood.pdf), arguing for the characteristic-specific effect through abductive reasoning. That is not a failure of the research design. It is just a different kind of argument than the one that closes Path 1.
