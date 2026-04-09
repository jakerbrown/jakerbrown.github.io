---
title: Claude v Codex I
subtitle: Porting Claude workflow to Codex
date: 2026-04-08 22:15
summary: A plain-language explanation of how I adapted Pedro Sant'Anna's Claude workflow repo into a Codex-first workflow while preserving the core process.
---

It is increasingly clear that the infrastructure *around* the model is a force
multiplier for what the model can achieve. I am still skeptical that I can
always tell with 100% confidence when one top model is obviously better than a
competitor. But I am curious and ready to be proven wrong. Partly as an
educational exercise, and partly to expand Codex's capacity in my workflow to
do more autonomous work, I worked with ChatGPT and Codex to translate Pedro
Sant'Anna's
[`claude-code-my-workflow`](https://github.com/pedrohcgs/claude-code-my-workflow)
repo so that as much of the same functionality as possible could be emulated in
Codex. I was particularly interested in the specialist agent capabilities (R
reviewer, proofreader, writer, etc.) and the adversarial agent that critiques
presentational work and code so the model iterates on itself to make the final
product and pipeline stronger. So far, Codex seems great for building out
codebases in fairly frequent contact with the human researcher, which I mostly
prefer as a workflow because it is easier to keep track of the project. But it
was not immediately clear how to get it to fully run away and write a paper on
its own.

So this port was an attempt to learn more about how Codex and Claude work while
also expanding what I can do with the models. Specifically: how much of the
Claude workflow from Sant'Anna's repo can be preserved when the assistant
changes from Claude to Codex?

You can find the repo for this project here:
[codex-my-workflow](https://github.com/jakerbrown/codex-my-workflow)

As Codex explains it to me:

> The simplest way to think about a workflow repo is as a toolbox plus a rulebook for working with an AI assistant.

- instructions about how to behave
- templates for plans and reports
- reusable specialist roles
- project memory that survives past one conversation
- verification steps so "done" means something real

That structure turns an AI assistant from "a smart autocomplete window" into
something closer to a junior contractor with a clipboard, a checklist, and a
filing cabinet.

The Claude Code setup was appealing because it treated reliability as a
workflow problem. It had several appealing features:

- Plan first. This is pretty standard operating procedure with Codex or
  Claude ("enter plan mode" or "make a plan").
- Keep durable notes on disk so context is not trapped in one chat window.
- Use specialists when one general reviewer is not enough.
- Verify outputs instead of trusting fluent prose.
- Gate completion with explicit quality thresholds.
- Use an adversarial critic/fixer loop instead of a single pass.

So I forked the repo, then asked ChatGPT 5.4 Pro in the browser how I could
work with Codex to port it into a Codex-focused version with as much of the
same functionality as possible. ChatGPT helped draft initial `AGENTS.md` and
plan documents to guide the Codex rewrite, and it also helped draft the prompt
that got Codex started on the translation. Codex then evaluated the Claude repo
and decided which documents could generally be preserved, what had to be
adapted, and what could not be recreated one-for-one.

The first lesson is that, at a high level, Claude and Codex are similar enough
that a port is genuinely possible. They can both read repository content, edit
files, follow detailed instructions, run shell commands, work iteratively, and
use role-like specializations. They also both benefit greatly from foundational
project guidance rather than one-off prompts. But the interesting part of
porting this workflow was where they differ.

As Codex put it:

> Claude and Codex are similar in the way two kitchens are similar: both have heat, knives, and counters, but the appliances are in different places and some of them work differently. A recipe can survive that move, but not by copying the layout blindly.

There are some important differences. The syntax of guiding documents varies,
so the repo structure through which Claude and Codex receive guidance differs.
Codex translated Claude project guidance into root and nested `AGENTS.md`
files. Claude settings became Codex config, hooks, and rules. Claude agent
definitions became `.codex/agents/*.toml`. Claude skills became repo-local
skills under `.agents/skills/`.

Another difference is that Codex makes explicitness more important. Codex is
less likely to automatically spawn agents such as the adversarial reviewer or
specialist agents. This functionality can still be achieved, but prompts need
to ask for it explicitly to better ensure those agents get deployed. That
changes how the workflow has to be written.

One takeaway is that in the original Claude-centered workflow, Claude can feel
more anticipatory of likely researcher desires, and therefore more autonomous.
In Codex, the safer pattern is to be more explicit. Prompts generally should
name the specialists to be spun up, tell Codex what to do with them, and state
verification expectations directly. Codex thus feels a little less magical and
in need of a bit more handholding from the researcher and the workflow
structure around it. But this is one of the most useful lessons from the port.
When platforms differ, a good fallback is often not "invent more automation."
It is "store the important files so the model can read them and stay on
target."
