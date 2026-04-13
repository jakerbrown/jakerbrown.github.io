---
title: How the claude/codex diary works
subtitle:
date: 2026-04-13 10:00
summary:
---

A year ago, the main limitation of these models seemed to be memory. It was
like working with a brilliant computer scientist who, for the life of them,
could not remember what I was working on. This has gotten much better by
default in the most expensive models, to the point where ChatGPT Pro will
bring up conversations about other projects when discussing completely
different projects, drawing connections and helping me place a question in the
broader context of my research agenda. But as before, the infrastructure around
these models is the real key to getting the most out of the intelligence
embedded in them. There is a great deal that can be done with scaffolding,
particularly having Claude or Codex keep detailed notes on what you are doing
and cataloguing decisions and preferences, to make memory better and help the
models stay on track.

So we do not have to rely on conversational recall to make Codex productive,
and we can preserve memory across sessions and different computing environments
by keeping track of what we do in durable files. In practice, that means
storing context in repository files that Codex is told to read at the start of
work, especially `AGENTS.md`, `KNOWLEDGE_BASE.md`, and `MEMORY.md`.
`KNOWLEDGE_BASE.md` is for domain truth that should remain true across
sessions: project definitions, architecture, naming rules, and recurring domain
facts. In my repos, `MEMORY.md` is usually read near the start of any
non-trivial task because the local `AGENTS.md` files explicitly tell Codex to
read it before proceeding. So the file is not magical application memory; it
works because the repo instructions repeatedly promote it into the model
context at the beginning of work. Claude's design anticipates all this, and it's memory is much better and more automatic than Codex.

As I was thinking about this, I decided that Claude Codex should keep even more
detailed notes on what I ask it to do, so I can refer back to them, since my
own memory is also not perfect. So I set up instructions in each repo to take
more copious notes, storing them in run logs. I then asked Codex to help me
set up functionality where it does a regular sweep of each repo's logs, drafts
a bulleted list of a sample of things it helped me do over the last few days,
and turns that list into a Codex diary blog post.

It strikes me as an interesting example of both the high-level possibilities
here, using better memory retention to increase operational capacity, and the
low-level ones, like using the same system to write a blog post that explains
what these tools can do. In all this I am basically an amateur, and more
efficient or more elegant ways of structuring these models surely exist, or
will soon. Mostly I just ask Claude/Codex whether something is possible and then have
it help me design it.


