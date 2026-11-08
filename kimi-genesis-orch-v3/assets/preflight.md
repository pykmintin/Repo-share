# Preflight — orchestrator-prompts skill load

This is the comprehension protocol. Run it once on first load in a session. It is one continuous exercise that threads three forces — dual-application, narrative anchoring, and articulation — through the same mental thread.

If you skip this, the skill becomes a list of words. With it, you have a stack of strategies you actually know how to deploy.

---

## Phase 0 — Read

Read these files, in order. You don't need to memorize. You need to know what's where so you can reach for it during use.

1. `SKILL.md` — framing, 4 forcing questions, 5 audit checks, catalog index.
2. `references/strategies.md` — full strategy catalog. Each entry has dual application (cognitive move + worker-prompt language) and a narrative case. Both pieces are load-bearing.
3. `references/failure-modes.md` — named failures, each tagged for own-work / worker-prompt / both.
4. `references/stacking.md` — archetypal situations and which strategies fire for each.
5. `references/slots.md` — the 8-slot structure (worker-prompt construction only).
6. `references/elicitation.md` — user-facing discipline.

When done, write one sentence: the single claim this skill makes that most changes how you would have approached the user's first message before reading. This is your Phase 0 marker.

Do not proceed to Phase 1 until that sentence is written.

---

## Phase 1 — Internalize (one exercise, three forces)

Three short questions sharing one mental thread. The strategies you pick in Q1 should be the ones you reference in Q2, and the same strategies reappear in Q3. One thread, three angles. The cost of doing all three is mostly the cost of doing one carefully.

### Q1 — Dual-application check (Force A)

Pick the 3 strategies you expect to be heaviest-weight in this session, given what the user has told you so far. For each, write:

- **As your own cognitive move:** what does it look like applied to your own thinking? (One line.)
- **As worker-prompt language:** what specific text does it produce in a prompt to a downstream worker? (One line.)

If you cannot write both, you don't yet know that strategy. Re-read its catalog entry in `references/strategies.md`. Do not proceed until both lines are written for all three strategies.

This question prevents *use-case forgetting* — the failure where an agent treats strategies as worker-only and never reaches for them while doing own-work.

### Q2 — Narrative-anchoring check (Force B)

For one of the 3 strategies you chose in Q1, write a short scenario (3-5 lines) showing how its failure-mode would show up in *this* session, given the project context the user has surfaced so far. Use the user's actual project nouns. Concrete, not abstract.

If you cannot ground the failure in this session, the principle isn't anchored — re-read the narrative case in the catalog entry. The catalog narratives are abstract by design; this question forces you to make them concrete to the project you're in.

This question prevents *list-decay* — abstract principles read as a checklist that doesn't survive contact with reality.

### Q3 — Articulation (Force C, project-specific plan)

Write a short articulation document, addressed to the user. Use the template at `assets/articulation.md`. It captures:

- The 3 strategies you'll lean on in this project (from Q1) and why each.
- The strategy you don't expect to need here, and why.
- Which use-case archetype (user-gives-info / user-requests-task / worker-returns / ambiguity-arrives / scope-creep-tempts / failure-surfaces) will most likely fire first this session.
- Which strategies you'd stack for that opening move.
- One thing in the catalog that shifted how you'd approach this project, compared to before reading the skill.

This question prevents *fluent ignorance* — the agent feeling they've understood without having tested it. Articulation is the test.

The articulation is the gate. The skill is "loaded" when you have written this document and shown it to the user — not before.

---

## Phase 2 — Surface

Show Q3 to the user. State that you've completed the preflight and the articulation is your operating brief for this project. The user can correct any of your project-specific picks before you start work. Common corrections:

- "Strategy X is more important here than you think because [project context you didn't have]."
- "The use-case archetype you picked isn't the most likely one — start with Y."
- "You misread the scope of this project — re-pick your 3 strategies."

If the user corrects you, re-do Q3 with the new context. Do not re-do Q1 or Q2 unless the correction was substantial enough to change which strategies are heaviest-weight.

---

## When to re-run preflight

Not every turn. The articulation produced at first load remains your operating brief.

Re-run only when the project's nature shifts enough that the heaviest-weight strategies might change:

- The user pivots to a substantially different task.
- A worker return reveals the project is structured very differently than you assumed.
- You're entering a new phase where the dominant use-case archetype changes (e.g., from ingestion-heavy to dispatch-heavy).

A heuristic: if you find yourself reaching for a strategy not in your top-3 from Q1, that's a signal the operating brief has drifted. Two responses: (a) update the brief explicitly with a one-paragraph addendum, or (b) re-run the preflight if the drift is large.

---

## Why this is one exercise, not three

The three forces guard against three different comprehension failures. If they were three sequential phases, the cost would be triple. They aren't — they share data.

- **Force A (dual-application)** prevents *use-case forgetting* — treating strategies as worker-only.
- **Force B (narrative anchoring)** prevents *list-decay* — abstract principles as a checklist.
- **Force C (articulation)** prevents *fluent ignorance* — feeling you understood without testing.

Each guards a different drift. Stacked, they reinforce. Skip any one and the comprehension is brittle.
