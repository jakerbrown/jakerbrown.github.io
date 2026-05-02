---
title: Reflections on ~2 months with Claude Code/Codex
subtitle: Come on in, the water is warm and we have plenty of tokens.
date: 2026-05-02 10:51
publish_at: 2026-05-02 10:51
summary:
---

![](/files/xmen.png)

- Integrated essentially my entire research workflow, except for actual writing, with Claude Code and Codex: chatbots as sounding boards when developing ideas, methodological questions, data sources, background literature, Claude Code/Codex for data collection, coding, package design, code review, formatting, replication verification, and so forth.

- Truly autonomous research still feels far off, but not due to lack of intelligence, just lack of memory/sufficient context window for complex projects. But I have been optimizing for human-with-agents workflow, with autonomous stuff being more [experimental](https://jacobrbrown.com/blog/page/2/#belmont-coyote-clusters).

- Working with agents is quite *immersive* and *fun*.

- Moving back and forth with both models is pretty seamless, [scaffolding](https://jacobrbrown.com/blog/page/3/#forking-a-claude-workflow-into-codex) helps a lot, especially with Codex.

- Claude Code's autonomy is compelling, at its best when reorganizing an entire codebase, or working across multiple sessions on long data collection projects

- Rate limits on Claude are real, I hit the 5 hour one regularly. Good to have Codex as well. Been using Pro/Max 5x for both.

- Some of that rate limit hitting is due to being greedy and always wanting to use the best Claude model.

- General workflow is work on 1 important thing at a time with Claude to preserve tokens, fan out with Codex.

- Git was trending up in use on projects, but now is essential.

- Codex has essentially replaced Rstudio, Github Desktop, Pycharm.

- ChatGPT 5.5 is noticeably better at autonomous coding than 5.4 or 5.3 Codex and -- it admitted this to me when I asked -- more Claude-like by design.

- Adding tables and figures to (over-long) appendices used to be quite the chore, now either agent can directly throw these into .qmd or .tex files, even edit Overleaf.

- Both models work well with batch job cluster systems, with some friction for Codex since its shell default constantly fails there before it jumps local.

- This may be habit, but I am much more happy with the answers I get from ChatGPT Pro chatbot than Claude. But both good overall. Claude gets over-exuberant.

- Using the models to write prompts (sometimes for each other) is a major efficiency gain. So the input is my detailed but more scattered request, then a detailed prompt from the LLM, input the prompt, get a plan, modify plan, approve plan, execute. This is most important for more complex database maintenance or data collection. 

- Everything is cleaner, faster, easier to work with. Smarter and better.

- The design of the interface is well done. You feel like a conductor orchestrating the agents. Ironic but agentic automation feels involving.

- The productivity force multiplier when not just you but also your co-authors are embracing agentic capabilities is intense.

- It's interesting how much of the competitive advantage of different models, Claude specifically, is the design of how they deliver their intelligence, not just the actual intelligence they deliver.

- I had Claude write a prompt to ask ChatGPT to give it a run down on who I am and what I do and what I typically use ChatGPT for. That was a weird experience.

- Claude revised the Codex documents in all of my repos and made Codex run better in terms of memory, adversarial review, multiple agents, etc.

- Codex is a great pre-doc, Claude is a great post-doc.

- Some projects require restricted environments or locations where AI is not allowed. Makes for a nice respite from the rapid takeoff world. Slow research soothes the soul.

- This has been quite energizing. Ideas propagate faster. I can try things that would other wise have taken a very long time to learn. 
