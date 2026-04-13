# Codex Diary And Memory Notes

## How the codex diary was made to work

- Start with a durable rule in each participating repo that every non-trivial Codex session leaves a short breadcrumb on disk before wrap-up.
- Standardize where those breadcrumbs live so the collector has predictable places to look: `memos/codex_activity/`, `quality_reports/codex_activity/`, or `logs/codex_activity/`.
- Standardize the breadcrumb filename pattern as `YYYY-MM-DD_slug.md` so the diary pass can find recent work quickly.
- Keep the breadcrumb itself very small and very plain: what was worked on, what changed, why it mattered, and what was verified or still unresolved.
- Put the central diary machinery in this website repo so one place owns the cross-repo summary workflow.
- Create a repo list in `files/codex-diary/config/repos.txt` so the collector knows exactly which local repositories count as part of the diary.
- Add `scripts/codex_diary_report.py` to scan each configured repo for recent breadcrumbs and git commits across the selected diary window.
- Make the script tolerant of imperfect repo state by checking a few candidate breadcrumb directories and skipping repos that are missing or inactive.
- Have the script write a dated digest into `files/codex-diary/daily_digest/` so each diary window has a durable source document instead of depending on chat history.
- Treat git history as a backup signal, not the main narrative source, so the diary still captures why the work mattered and what was verified.
- Add shared style rules in `files/codex-diary/config/style_preferences.md` so the final diary reads like a public-facing note rather than an internal technical log.
- Add a breadcrumb template and README in `files/codex-diary/` so the workflow is explainable and repeatable rather than living only in prompts.
- Add a lightweight checker in `scripts/check_codex_diary_style.py` so the final diary can be quickly sanity-checked for tone and structure.
- Keep a running diary file at `files/codex-diary/diary.md`, with one dated section per diary window, so the public artifact is stable and append-only.
- Use a Codex automation to generate a digest for the current window and then turn that digest into a short set of polished bullets for that span.
- Delay publication until late evening so the diary does not appear on the blog as a premature placeholder before the day is actually over.
- Wire the site generator to treat dated sections from `files/codex-diary/diary.md` as blog posts automatically, so the diary becomes part of the regular publishing flow instead of a separate manual site process.
- Tighten the style over time by revising both the rules and the actual diary entries after reading how they landed in the blog.
- Require breadcrumb entries in repo-level `AGENTS.md` files so the diary system is enforced where the work happens, not just documented centrally.
- The core design choice is to move the important memory from ephemeral chat into small on-disk artifacts at two levels: local breadcrumbs during the day, and a central digest plus diary entry at night.

## Memory more generally in Codex

- The main memory idea in your setup is that Codex should not rely on conversational recall for anything important that needs to survive across sessions.
- In practice, that means storing durable context in repository files that Codex is told to read at the start of work, especially `AGENTS.md`, `KNOWLEDGE_BASE.md`, and `MEMORY.md`.
- `KNOWLEDGE_BASE.md` is for domain truth that should remain true across sessions: project definitions, architecture, naming rules, and recurring domain facts.
- `MEMORY.md` is for workflow truth: what Codex learned about how to operate safely and effectively in that particular repo.
- The reusable workflow docs in `codex-my-workflow` make this distinction explicit: domain truth goes in `KNOWLEDGE_BASE.md`; workflow truth goes in `MEMORY.md`.
- The standard `MEMORY.md` format across several repos is a sequence of `[LEARN]` blocks with `Context`, `Lesson`, and `Action`.
- That format matters because it turns vague “remember this next time” advice into a concrete rule with a reason and an expected behavior.
- In your repos, `MEMORY.md` is usually read near the start of any non-trivial task because the local `AGENTS.md` files explicitly tell Codex to read it before proceeding.
- So the file is not magical application memory; it works because the repo instructions repeatedly promote it into the model context at the beginning of work.
- In `referenda`, `MEMORY.md` stores lessons about preserving memo-style ExecPlans, separating workflow notes from runbooks, and making uncertainty explicit instead of overclaiming coverage.
- In `ward_sim`, `MEMORY.md` stores lessons about preserving the repo’s existing planning surface, keeping workflow logs out of runtime logs, staying additive in dirty worktrees, and escalating review only when the stakes justify it.
- In `twitter`, `MEMORY.md` stores lessons about respecting existing safety boundaries, using syntax-level validation when private data block full runs, and naming specialist review lenses explicitly before inventing more machinery.
- In `aggregate_causal`, `MEMORY.md` is a little more compact and functions as a short operating manual: what to read first, common failure modes, how to verify, when to escalate review, and how much workflow infrastructure is appropriate.
- Across repos, the file works less like a diary and more like a durable list of “hard-won operating lessons” for future Codex sessions.
- The point is not to save everything. The point is to save the recurring things that are easy for a model to forget but expensive to relearn.
- That includes repo-specific planning surfaces, validation norms, review expectations, path safety rules, naming conventions, and known failure modes.
- It also helps preserve the user’s house style, because preferences like “be additive,” “record uncertainty,” or “treat verification as part of done” can be written once and reused many times.
- In your broader workflow, memory is layered rather than centralized: `AGENTS.md` gives instructions, `KNOWLEDGE_BASE.md` gives durable project facts, `MEMORY.md` gives workflow lessons, plans track current task intent, and session logs preserve what happened during a specific stretch of work.
- That layered approach is why the system is more robust than chat memory alone: each file has a narrower job, so the important context is easier to reload and maintain.
- A useful blog framing is that `MEMORY.md` is not an autonomous memory system built into Codex. It is a deliberate repo-local prompt surface that becomes effective because your workflow teaches Codex to consult it every time.

## Possible framing for the post

- The diary works because you reduced “memory” into a set of small durable files with different jobs, rather than asking the model to remember everything itself.
- Breadcrumbs capture what happened locally.
- The digest script gathers the day across repos.
- The diary style rules turn raw notes into something readable by outsiders.
- `MEMORY.md` does the same kind of work at the repo level: it preserves the recurring lessons that shape future sessions.
