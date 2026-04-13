---
title: Parallel confounding in identification of place effects
subtitle:
date: 2026-04-12 11:00
summary:
---

Suppose I have some characteristic of place $X_p$ that I think causes an outcome $Y_i$, such as the effect of racial context on vote choice. There are two distinct sources of confounding to worry about:

1. Place assignment itself may be non-random. Place, or time spent in place if the treatment is duration of exposure, needs to be as-if randomly assigned conditional on observables.
2. Other place characteristics may move together with $X$. Everything about places with higher $X$ besides $X$ itself can confound the relationship if it also affects $Y_i$.

**Notation:**
- $P_i \in \{1, \dots, J\}$: place assignment for individual $i$ (or exposure duration $D_i$ if treatment is length of exposure)
- $X_p \in \mathbb{R}$: focal characteristic of place $p$
- $\mathbf{Z}_p \in \mathbb{R}^K$: all other characteristics of place $p$ (the "overlapping" attributes)
- $\mathbf{W}_i$: pre-treatment individual covariates
- $Y_i(p)$: potential outcome for $i$ under assignment to place $p$
- $Y_i(x)$: potential outcome for $i$ under intervention setting the focal characteristic to $x$
- $Y_i = Y_i(P_i)$ is the observed outcome

## Estimands

The **overall place effect** is:

$$\tau^{\text{place}}(p, p') = \mathbb{E}[Y_i(p) - Y_i(p')]$$

The **characteristic effect** is:

$$\tau^{X}(x, x') = \mathbb{E}[Y_i(x) - Y_i(x')]$$

## Two Threats to Identification of $\tau^X$

Identifying the causal effect of a specific place characteristic $X_p$ on outcomes requires closing two distinct backdoor paths from $X_p$ to $Y_i$. These paths operate through different mechanisms and can be open or closed independently.

### Path 1: Individual Selection into Place

$$X_p \leftarrow P_i \leftarrow \mathbf{W}_i \rightarrow Y_i$$

Individuals sort into places non-randomly. If pre-treatment characteristics $\mathbf{W}_i$ both drive place choice and directly affect outcomes, then any place characteristic — including $X_p$ — inherits a spurious correlation with $Y_i$ through the sorting process. Closing this path requires:

$$P_i \perp\!\!\!\perp Y_i(p) \mid \mathbf{W}_i \quad \forall \, p$$

This is the standard place-ignorability assumption. Under overlap ($0 < \Pr(P_i = p \mid \mathbf{W}_i) < 1$), it is sufficient to identify $\tau^{\text{place}}$ — the overall effect of place — because the entire bundle of place characteristics is rendered uncorrelated with potential outcomes conditional on $\mathbf{W}_i$.

Note, however, that Path 1 may be innocuous for a *specific* characteristic $X$ even when place assignment is endogenous. If $X_p \perp\!\!\!\perp Y_i(p)| \mathbf{W}_i$ — that is, $X$ is orthogonal to the dimensions along which individuals sort — then the individual selection path does not confound the $X \to Y$ relationship. For instance, if people sort into cities based on job opportunities but $X$ is average annual rainfall, Path 1 may be irrelevant for $\tau^X$ even though $\tau^{\text{place}}$ is confounded.

### Path 2: Overlapping Place Characteristics

$$X_p \leftarrow P_i \rightarrow \mathbf{Z}_p \rightarrow Y_i$$

Place jointly determines $X_p$ and all other place characteristics $\mathbf{Z}_p$. Even if individual selection is resolved, variation in $X$ across places is bundled with variation in $\mathbf{Z}$. Closing this path requires:

$$X_p \perp\!\!\!\perp Y_i(x) \mid \mathbf{W}_i, \mathbf{Z}_p$$

This is a distinct identification challenge from Path 1. It concerns the internal structure of places — how to separate the contribution of one characteristic from the contributions of all others — rather than the selection of individuals into places. Identifying $\tau^X$ requires imagining interventions that vary $X$ independently of $\mathbf{Z}$—which is not how places vary in the data.

![Two-stage confounding DAG](/files/two_stage_confounding_dag.svg)



$\tau^{\text{place}}$ requires closing only Path 1. $\tau^{X}$ requires closing both, or establishing that one is innocuous. If people sort into places non-randomly, but $X$ happens to be the only place characteristic that affects $Y$ (or the only one correlated with $\mathbf{W}_i$), then solving selection is sufficient.  The typical case is that both paths are open, making identification of causal place *characteristic* effects doubly hard. 

## How this applies to four place effects identification strategies

### [Randomized relocation](https://www.cambridge.org/core/journals/american-political-science-review/article/longterm-effects-of-neighborhood-disadvantage-on-voting-behavior-the-moving-to-opportunity-experiment/4896C6743CF5D53DDD067D51D93A8CA7)

**Additional notation.** Let $Z_i \in \{0, 1\}$ denote a randomly assigned voucher offer (or other experimentally assigned inducement to move). Let $D_i \in \{0, 1\}$ indicate whether individual $i$ actually moves in response to the offer. Among movers, let $P_i^1$ denote the destination neighborhood and $P_i^0$ the origin. The voucher shifts families from neighborhoods with characteristics $(X_{P_i^0}, \mathbf{Z}_{P_i^0})$ to neighborhoods with characteristics $(X_{P_i^1}, \mathbf{Z}_{P_i^1})$.

**Identifying variation.** Random assignment of $Z_i$ provides an unconfounded source of variation in neighborhood exposure. The intention-to-treat effect is:

$$\tau^{\text{ITT}} = \mathbb{E}[Y_i \mid Z_i = 1] - \mathbb{E}[Y_i \mid Z_i = 0]$$

With one-sided noncompliance (not all voucher recipients move), one can estimate the local average treatment effect on compliers by instrumenting actual move status $D_i$ with $Z_i$:

$$\tau^{\text{LATE}} = \frac{\mathbb{E}[Y_i \mid Z_i = 1] - \mathbb{E}[Y_i \mid Z_i = 0]}{\mathbb{E}[D_i \mid Z_i = 1] - \mathbb{E}[D_i \mid Z_i = 0]}$$

**Path 1 (individual selection) — Closed by design.** Randomization eliminates Path 1 entirely:

$$Z_i \perp\!\!\!\perp \big(Y_i(z), D_i(z), \mathbf{W}_i\big) \quad \forall \, z$$

Pre-treatment characteristics $\mathbf{W}_i$ are balanced across treatment and control by construction. There is no selection into place to worry about — the experiment *is* the assignment mechanism. This is the strongest possible resolution of Path 1: no functional form assumptions, no conditional independence, no parallel trends. Randomization handles it.

**Path 2 (overlapping characteristics) — Open.** Despite the experimental gold standard for Path 1, the experiment randomizes access to a *bundle* of neighborhood characteristics, not to $X$ specifically. Families who use their voucher move from high-poverty neighborhoods to lower-poverty neighborhoods — but these destination neighborhoods also differ from origin neighborhoods in school quality, crime rates, social networks, environmental exposures, and innumerable other attributes. The estimand $\tau^{\text{ITT}}$ (or $\tau^{\text{LATE}}$) captures the composite effect of the entire neighborhood change:

$$\tau^{\text{LATE}} = f\big(\Delta X, \Delta \mathbf{Z}\big)$$

where $\Delta X = X_{P^1} - X_{P^0}$ and $\Delta \mathbf{Z} = \mathbf{Z}_{P^1} - \mathbf{Z}_{P^0}$ change simultaneously. The backdoor path $X_p \leftarrow P_i \rightarrow \mathbf{Z}_p \rightarrow Y_i$ remains fully open. One cannot determine from the experiment alone whether the effects on mental health, for instance, are driven by lower poverty, safer streets, better schools, or reduced pollution — all of which changed together when families moved.

This is a central lesson: **even a randomized experiment does not identify the effect of a specific place characteristic.** The experiment tells us whether *neighborhoods matter*; it cannot tell us *what about neighborhoods* matters. Randomization solves assignment to bundles, it does nothing to separate components within bundles. 

![Randomized relocation DAG](/files/dag_a_mto_experiment.svg)

### [Childhood mover design](https://jacobrbrown.com/files/w31759.pdf)

**Additional notation.** Let $o(i)$ and $d(i)$ denote the origin and destination places for mover $i$. Let $a_i$ denote the age at move, so that exposure to the destination is $E_i = \bar{a} - a_i$ years, where $\bar{a}$ is the age at which outcomes are measured (e.g., age 26 for income). Define the place-level causal exposure effect $\mu_p$ as the causal effect of an additional year of childhood spent in place $p$.

**Identifying variation.** Among children who move from the same origin to the same destination, those who move at younger ages receive a higher "dose" of the destination. The key regression takes the form:

$$Y_i = \delta_{o(i)} + \delta_{d(i)} + \mu_{d(i)} \cdot E_i + \mathbf{W}_i'\gamma + \varepsilon_i$$

where $\delta_{o(i)}$ and $\delta_{d(i)}$ are origin and destination fixed effects.

**Path 1 — Solved.** The identifying assumption is:

$$a_i \perp\!\!\!\perp Y_i(a) \mid o(i), d(i), \mathbf{W}_i$$

That is, conditional on origin-destination pair and family characteristics, the age at move is as-if randomly assigned. This is a selection-on-observables assumption, but it is strengthened considerably by the within-origin-destination comparison: families that move from the same place to the same place but at different times are arguably similar. The design identifies $\mu_p$, the causal exposure effect of place $p$.

**Path 2 — Not solved.** The estimated $\hat{\mu}_p$ captures the total causal effect of an additional year of exposure to everything about place $p$ — the full bundle $(X_p, \mathbf{Z}_p)$. The design identifies $\tau^{\text{place}}$ (in its exposure-effect form) but not $\tau^X$. One can regress $\hat{\mu}_p$ on $X_p$ across places in a second stage:

$$\hat{\mu}_p = \alpha + \beta X_p + \eta_p$$

but $\beta$ is subject to Path 2 confounding: $\text{Cov}(X_p, \mathbf{Z}_p) \neq 0$ across places, so $\hat{\beta}$ conflates the effect of $X$ with the effects of correlated place characteristics. The backdoor path $X_p \leftarrow P_i \rightarrow \mathbf{Z}_p \rightarrow Y_i$ remains open.

![Childhood mover DAG](/files/dag_a_childhood_mover.svg)

### [Difference-in-differences](https://link.springer.com/article/10.1007/s11109-020-09626-1)

**Additional notation.** Suppose individuals remain in their places and we observe panel data over periods $t \in \{0, 1\}$. The focal characteristic $X_{pt}$ varies over time within places (e.g., a new policy is adopted in some places but not others). Other place characteristics may also change: $\mathbf{Z}_{pt}$. Let $\alpha_i$ denote a time-invariant individual (or place) fixed effect and $\lambda_t$ a common time effect.

**Identifying variation.** The change in $X_{pt}$ within a place over time, net of common trends, provides identifying variation. The estimating equation is:

$$Y_{it} = \alpha_i + \lambda_t + \beta X_{p(i),t} + \mathbf{Z}_{p(i),t}'\gamma + \varepsilon_{it}$$

or equivalently in first differences:

$$\Delta Y_{it} = \Delta \lambda + \beta \, \Delta X_{p(i),t} + \Delta \mathbf{Z}_{p(i),t}'\gamma + \Delta \varepsilon_{it}$$

**Path 1 — Partially solved.** Individual fixed effects $\alpha_i$ absorb all *time-invariant* determinants of both place selection and outcomes — including the level of $\mathbf{W}_i$ that drives sorting into places. This eliminates the most obvious form of Path 1 confounding: individuals with higher baseline potential outcomes selecting into particular places.

However, fixed effects do not rule out *selection on trends in potential outcomes*. The residual Path 1 assumption is:

$$\mathbb{E}[\Delta Y_{it}(0) \mid P_i, \Delta X_{pt}] = \mathbb{E}[\Delta Y_{it}(0) \mid \Delta X_{pt}]$$

That is, conditional on the change in $X$, the trend in untreated potential outcomes must be uncorrelated with place membership. This fails if individuals sort into places based on anticipated trajectories of $Y$ — for example, if workers move to cities where wages are already rising for reasons unrelated to $X$ — or if the places where $X$ changes are on systematically different outcome trends from places where $X$ does not change. The parallel trends assumption thus represents a *residual* Path 1 requirement: weaker than cross-sectional ignorability of place assignment, but not trivially satisfied by the panel structure alone.

**Path 2 — Partially addressed.** The parallel trends assumption for $\tau^X$ is:

$$\mathbb{E}[\Delta Y_{it}(0) \mid \Delta X_{pt}, \Delta \mathbf{Z}_{pt}] = \mathbb{E}[\Delta Y_{it}(0) \mid \Delta \mathbf{Z}_{pt}]$$

That is, conditional on changes in other place characteristics, changes in $X$ are uncorrelated with changes in untreated potential outcomes. Including time-varying controls $\Delta \mathbf{Z}_{pt}$ blocks the backdoor path through observed overlapping characteristics that co-move with $X$. This *partially* addresses Path 2: the path $\Delta X_{pt} \leftarrow \text{co-trend} \rightarrow \Delta \mathbf{Z}_{pt} \rightarrow \Delta Y_{it}$ is blocked for observed $\mathbf{Z}$, but unobserved co-trending place characteristics remain a threat.

![Difference-in-differences DAG](/files/dag_b_difference_in_differences.svg)

### [Spatial regression discontinuity](https://www.econometricsociety.org/publications/econometrica/2025/11/01/Gangs-Labor-Mobility-and-Development)

**Additional notation.** Let $\mathcal{B}$ denote a spatial boundary (e.g., a state or policy border) across which $X$ changes discontinuously. Define the running variable $r_i$ as the signed distance from individual $i$ to $\mathcal{B}$, with $r_i > 0$ on the "high-$X$" side. Let $\Delta_X = \lim_{r \to 0^+} X_p(r) - \lim_{r \to 0^-} X_p(r)$ denote the jump in $X$ at the boundary.

**Identifying variation.** The discontinuity in $X$ at $\mathcal{B}$ provides a local experiment: individuals just on either side of the boundary live in places that differ sharply in $X$ but (under the identifying assumptions) are otherwise comparable. The estimand is a local average treatment effect at the boundary:

$$\tau^{\text{RD}} = \frac{\lim_{r \to 0^+} \mathbb{E}[Y_i \mid r_i = r] - \lim_{r \to 0^-} \mathbb{E}[Y_i \mid r_i = r]}{\Delta_X}$$

**Path 1 — Solved.** The continuity assumption on individual characteristics at the boundary is:

$$\lim_{r \to 0^+} \mathbb{E}[\mathbf{W}_i \mid r_i = r] = \lim_{r \to 0^-} \mathbb{E}[\mathbf{W}_i \mid r_i = r]$$

Individuals cannot precisely sort across the boundary, so those just on either side are comparable in pre-treatment characteristics. Place assignment (which side of the boundary) is as-if randomly assigned in a neighborhood of $\mathcal{B}$.

**Path 2 — Solved (conditionally).** The key additional assumption is that overlapping place characteristics are continuous at $\mathcal{B}$:

$$\lim_{r \to 0^+} \mathbf{Z}_p(r) = \lim_{r \to 0^-} \mathbf{Z}_p(r) \quad \text{while} \quad \lim_{r \to 0^+} X_p(r) \neq \lim_{r \to 0^-} X_p(r)$$

If $X$ jumps at the boundary but $\mathbf{Z}$ does not, then the variation in $X$ at $\mathcal{B}$ is free of Path 2 confounding: the backdoor path $X_p \leftarrow \mathbf{Z}_p \rightarrow Y_i$ is closed because $\mathbf{Z}_p$ is locally constant across the discontinuity. This is the strongest resolution of Path 2 among the three designs.

**Caveat: compound treatments.** If other place characteristics also jump at $\mathcal{B}$ — for instance, if the boundary is a state border and multiple policies change at the same line — then Path 2 is not fully solved. The identifying discontinuity bundles $X$ with whichever elements of $\mathbf{Z}$ also change at the boundary, and we are back to a version of the overlapping-characteristics problem.

![Spatial regression discontinuity DAG](/files/dag_c_spatial_rd.svg)

## Last thoughts: Path 2 is a construct validity problem

In many settings, $X_p$ does not vary independently of $\mathbf{Z}_p$ even in principle, so $\tau^X$ may not be well-identified without additional structure or functional form assumptions. In practice, then, Path 2 is a construct validity problem. Does assignment to place measure what we think it measures? If so, as-if random assumptions about place may lead us to convincing arguments about the effect of $X_i$ on $Y_i$. This is akin to a survey experiment that aims to prime one emotion but perhaps primes other feeling as well. A design gives us credible variation in something, and whether that something corresponds to the theoretical construct we care about is a separate claim. In absence of clean identification closing Path 2, researchers fall back to [inference to the best explanation](https://arthurspirling.org/documents/whatgood.pdf), arguing for $\tau^{X}$ through abductive reasoning.
 
