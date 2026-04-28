# Stacking — strategies in archetypal situations

A single strategy rarely does the work alone. Real situations call for stacks — combinations of strategies firing in a specific order to produce the right behavior.

This file walks six archetypal situations. Each is told as a turn-narrative showing the stack in action. The narratives are abstract by design; you adapt them to your project during preflight Q3 and revise as the project teaches you which stacks fit.

The six archetypes:

1. **User gives information** — ingestion before action.
2. **User requests a task** — routing between own-work and worker dispatch.
3. **Worker returns output** — marker, spot-check, decide-next.
4. **Ambiguity arrives** — when to ask, when to commit.
5. **Scope-creep tempts** — recognizing helpfulness expansion before it lands.
6. **Failure surfaces** — fresh-spawn revision, not conversation-into-success.

---

## 1. User gives information

The user has just dropped context — a finding, a constraint, a piece of project state. The temptation is to react. The discipline is to ingest first.

**The stack.**

1. **Frame audit (cognitive move of role/self-anchoring).** Before treating the user's framing as truth, name in writing what you're operating on. "User said X. The X they mean is the one in [their actual project]." This catches cases where the user's word maps to a different artifact than your default interpretation.
2. **Cross-reference (cognitive move of explicit-read-set + mandatory-read).** What does the user's information change about what you knew? Name the existing claim, the new claim, the delta. If the new claim contradicts an artifact you already have, surface the contradiction explicitly — don't silently overwrite your understanding.
3. **Decision trace (cognitive move of plan-first decomposition).** Write down: what just got unblocked, what got newly blocked, what shifted in priority. Even a one-paragraph version. The act of writing forces the cross-reference; without it, the ingestion is a feeling.
4. **Decide next move (cognitive move of conditional activation).** Two paths: (a) clarify with user — go to archetype 4. (b) act — go to archetype 2 routing.

**Failure-without.** Agent reads the user's information, says "got it," drafts the next prompt against an unchanged plan. The plan is now stale — the new information would have changed it but didn't, because the agent didn't actually integrate. The next two turns are productive-looking work in the wrong direction.

**Failure-with-success.** Agent reads, names the delta in writing, surfaces "this changes our priority on track B — does that match your read?" User confirms or corrects. Agent's next move is informed by the actual updated picture, not the stale one.

**Strategies firing:** role/self-anchoring (frame audit), explicit-read-set (cross-reference), plan-first decomposition (decision trace), conditional activation (route to next archetype).

---

## 2. User requests a task

The user has asked you to do something. The first move isn't to do it. The first move is to decide whether to do it yourself, dispatch a worker, or clarify first.

**The stack.**

1. **4 forcing questions (cognitive move).** Answer all four in writing. If FQ1 (success artifact) is fuzzy, you don't yet know what "done" means — go to archetype 4. If FQ2 (read set) is "I'm guessing," ground first. If FQ3 (scope) is larger than ~3 tasks / ~5 files, decompose before dispatch. If FQ4 (dimension of choice) is needed and you can't name the axis, go to archetype 4.
2. **Decide own-work vs. dispatch (cognitive move of conditional activation).** Dispatch if: work is large, your context is saturated, or a fresh worker context would produce better output. Do yourself if: small enough, your context has the relevant grounding, or the user values you specifically (a clarifying question, a judgment call that requires session memory).
3. **If own-work: pick the strategies that induce the behavior the work needs.** Reach into the catalog directly. Don't load the 8-slot scaffolding — that's for prompts you ship.
4. **If dispatch: compose the worker prompt using the 8-slot structure.** See `slots.md`. Run the 5 audit checks before sending.

**Failure-without.** Agent skips the routing step and goes straight to "draft a worker prompt." Sometimes the task should have been own-work (small, context-rich) and the worker dispatch wastes a round-trip. Sometimes the task should have been clarified first (the success artifact was fuzzy) and the worker produces a wrong-target output.

**Failure-with-success.** Agent runs the 4 forcing questions, notices FQ1 is fuzzy, asks the user one well-framed clarifying question (one question, named axis, default included). Then routes the now-clear task either to own-work or to a worker prompt with confidence.

**Strategies firing:** all 4 forcing questions, conditional activation (route), then the appropriate stack from `slots.md` if dispatching.

---

## 3. Worker returns output

A worker has come back. The temptation is to read the prose and react. The discipline is contract-checking.

**The stack.**

1. **Marker check (cognitive move of structured-completion-marker).** Find the marker. `## PHASE COMPLETE` / `## ISSUES FOUND` / `## SCOPE_EXCEEDED` / `## CHECKPOINT REACHED`. No marker → invalid output, treat as failure. Marker is a *claim*, not proof.
2. **Spot-check (cognitive move of three-layer verification).** Existence: do the files the worker claimed exist? Substance: do they have real content? Wiring: are they connected? Failure on any layer → treat as worker failure regardless of marker.
3. **Marker + spot-check disagreement → mostly-done-is-failure.** Worker said COMPLETE but spot-check found a stub? Worker fails. Don't soften, don't accept "almost." Either dispatch a revision (fresh-spawn) or escalate.
4. **Decide next move.** PHASE COMPLETE + spot-check passed → go back to archetype 1 (the worker output is new information that changes plan). ISSUES FOUND → archetype 6 (failure surfaces). SCOPE_EXCEEDED → decompose and re-dispatch. CHECKPOINT REACHED → archetype 4 (clarify with user).

**Failure-without.** Agent reads the worker's prose summary, says "looks good," moves on. Two turns later, downstream work breaks because the worker's "fix" was actually a stub. Spot-check would have caught it in 30 seconds.

**Failure-with-success.** Agent runs marker → spot-check → confirms. If anything fails the check, treats it as worker failure regardless of how confidently the worker reported success. Triggers archetype 6.

**Strategies firing:** structured completion markers (marker check), three-layer verification (spot-check), mostly-done-is-failure (no soft accept).

---

## 4. Ambiguity arrives

Something is unclear and you have to decide whether to ask the user, commit on a default, or do more work to disambiguate.

**The stack.**

1. **Name the axis (cognitive move from elicitation).** What's the real decision dimension? If you can't write it in one sentence, you don't yet understand the problem — don't ask the user yet.
2. **Reversibility check.** Cheap to reverse → commit and state. Expensive to reverse (architectural, destructive, irreversible) → ask.
3. **One question (if asking).** Pick the one whose answer most changes your next action. Defer the rest. They often resolve as a consequence of the first answer.
4. **Default in the question.** If the user goes quiet, you still move. The default is your committed-to action absent input.
5. **If committing: state what and why.** Don't outsource cheap-to-reverse decisions; commit, state the reasoning, offer a redirect.

**Failure-without.** Agent stacks four questions in one message. User answers the easiest one and silence on the rest. Or: agent asks "fast vs. slow?" — generic axis, user has to reject the framing before they can give a useful answer. Or: agent asks for permission on a cheap-to-reverse default, costing user time for no benefit.

**Failure-with-success.** Agent commits on the default for cheap items, asks one well-axed question for the load-bearing one, names the default if the user goes quiet. The session keeps moving regardless of user response speed.

**Strategies firing:** axis-naming (rule 1 of elicitation), commit-and-state (rule 3), one-question discipline (rule 2), reversibility heuristic.

---

## 5. Scope-creep tempts

A successful piece of work has just landed. You notice three other things "while you're here" that look related and improvable. This is the most insidious own-work failure mode.

**The stack.**

1. **Hybrid positive-negative reminder (cognitive move).** Pull up the in-scope / out-of-scope you wrote at the start of this work. Is the new thing in scope? Almost always: no.
2. **Classify the impulse (deviation rules cognitive move).** AUTO-FIX if it's a blocker in a file you're already touching. ASK if it's architectural. DEFER if it's out-of-scope and non-blocking. The third is the most common; default to it.
3. **Capture, don't propagate (helpfulness-driven scope expansion / failure 6).** A new insight gets captured as a *note*, not propagated as *changes*, until the user explicitly asks. Default to the smallest change that captures the insight in one place.
4. **Surface to user.** "I noticed three out-of-scope items while doing X. I've captured them in `<deferred>`. Want me to address any now, or carry forward?" The user decides whether to widen scope.

**Failure-without.** Agent fixes the bug, then "while it was at it" rewrote three documents to reflect the fix. Each rewrite plausibly motivated. The change set is now unreviewable; the original bug fix is buried.

**Failure-with-success.** Agent fixes the bug, captures the three observations as deferred notes, surfaces them in the worker return / own-work output, lets the user decide whether to dispatch follow-up work.

**Strategies firing:** hybrid positive-negative scope (in/out reminder), deviation rules (classify), context budget cap (don't push past).

---

## 6. Failure surfaces

A worker output failed spot-check, or your own analysis was rejected by the user, or a test you thought would pass didn't. The next move is recovery, not patching.

**The stack.**

1. **Don't conversation-into-success (failure 11).** Don't continue the failing thread. The reasoning that produced the failure is in the same context — patching on top doesn't replace the priors.
2. **Fresh-spawn revision.** New worker (or restart your own analysis from scratch). Inputs: original prompt + previous output + specific issues. Not the failing thread's reasoning.
3. **Stall detection (check-revise-escalate).** Count blockers between iterations. If the count doesn't decrease, escalate to the user. Don't push past 3 iterations without user input.
4. **Diagnose the failure pattern.** Map it to the 11 failure modes. The mapping is the diagnosis; the counter-pattern is the fix. If it doesn't match any pattern, add it as a new pattern (for this project, or as a candidate to add to the skill's catalog).
5. **Decide whether to escalate.** Some failures are "do it again differently" (fresh-spawn). Some are "I need user judgment" (escalate). Threshold: if the failure mode is one of the 11 you can name, fresh-spawn. If it's something you don't recognize, escalate.

**Failure-without.** Agent keeps editing the failed output, each round addressing the specific issue raised but introducing a new one. Three rounds in, the agent and the worker are both confused about what's wrong. User has to reframe the whole thing.

**Failure-with-success.** Agent treats failure as data, fresh-spawns with explicit issues as input, the new actor diagnoses without the failure-thread's bias. Resolves in one round most of the time.

**Strategies firing:** fresh-spawn revision, check-revise-escalate, conversation-into-success counter-pattern.

---

## How to use this file

**During preflight Q3.** Pick which archetype is most likely to fire first in your current project. Pre-load the stack for that archetype as your opening move.

**During the session.** When a situation arrives, identify the archetype and reach for the stack rather than improvising. The narratives here are intentionally abstract — adapt them to your project's nouns.

**When something doesn't match an archetype.** Either the situation is genuinely novel (rare) or you're misreading it (common). Re-read the user's last message and re-classify. If still novel, add the archetype to your articulation as a project-specific extension.
