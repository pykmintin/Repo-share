# The 8 Slots — for worker-prompt construction

**Scope of this file:** worker-prompt construction only. The 8-slot structure is the canonical layout for a prompt sent to a downstream agent. For own-work, you reach into `strategies.md` directly — the slots are scaffolding for prompts you ship, not for thinking you do.

Each slot induces one class of behavior in the worker. Weak-vs-strong contrasts are the teaching — a slot you can describe abstractly is a slot you'll fill abstractly, which is a slot that doesn't induce anything.

---

## Slot 1: Role

**Behavior needed.** Domain vocabulary activation + methodology adoption. The worker thinks the way someone with the right expertise would, reaching for the idioms and cautions of that field rather than generic helpful-assistant ones.

**Why first.** Role tokens at the start of the prompt receive attention from every later position. Setting role after the fact is much weaker.

**Strategies that fit.** Role anchoring (specific credentials), functional role with process pipeline, conditional mode switching.

**Weak.**
> You are an expert.

Activates nothing specific. Model is in "helpful assistant" mode with slightly elevated confidence.

**Strong.**
> You are a debugging agent. You are a senior backend engineer with distributed-systems experience. Your process is: reproduce → observe → hypothesize → test → localize → propose fix. You do not skip steps. You do not propose a fix before localizing the cause.

Activates distributed-systems vocabulary, methodology (reproduce-first), sequence adherence, caution about premature fixes.

**Break mode.** Worker defaults to "friendly general helper" register and picks its own methodology, usually the one that looks most helpful short-term. Outputs are plausible but don't reflect the field's actual norms.

---

## Slot 2: Read set

**Behavior needed.** Grounding in actual state. The worker looks at real files before acting, not at what it imagines they contain.

**Why load-bearing.** Single highest-leverage grounding mechanism. Workers that skip real reads write plausible-but-wrong code and the orchestrator often can't catch it without running the code.

**Strategies that fit.** Mandatory read-before-write protocol, explicit read set with exact paths.

**Weak.**
> Familiarize yourself with the relevant code.

"Relevant" and "familiarize" are both up to the worker's interpretation, which is wrong.

**Strong.**
> HARD RULE: before modifying any file, call ReadFile on that file. Files to read first, in order:
> - src/auth/token.py
> - src/auth/test_token.py
> - docs/auth_contract.md
> You are forbidden from writing based on assumptions about file contents. Output that violates this rule is invalid.

Exact paths (auditable), invariant phrased as an invalidation condition (self-checkable), ordering.

**Break mode.** Worker fabricates file contents from the prompt and its training priors. Clobbers existing code. "Improvements" remove working features.

---

## Slot 3: Project context

**Behavior needed.** Convention adherence. Code fits the codebase's naming, style, error-handling, and test patterns rather than generic "best practices."

**Why it matters.** Conventions live in project files (CLAUDE.md, AGENTS.md, style guides). Without pointing, the worker uses training-data defaults — a random sample of internet code.

**Strategies that fit.** Project context discovery.

**Weak.**
> Follow the project's conventions.

Worker has no idea what they are and won't ask.

**Strong.**
> Before drafting any code: read CLAUDE.md and scan .claude/skills/ for applicable skills. Apply whatever conventions they document. If CLAUDE.md specifies a testing framework, naming convention, or style rule, follow it rather than a generic default.

Mandates reading, names downstream use, names the override rule.

**Skip when.** Task doesn't touch project code, or no documented conventions exist.

---

## Slot 4: Mission

**Behavior needed.** Understanding what "done" means, including who consumes the output and what they need it to look like. The densest slot — carries task + downstream expectations + mission-specific constraints.

**Why here.** Missions without downstream-consumer info produce outputs that are complete-by-spec but wrong-by-need. Consumers are often another worker or an automated check.

**Strategies that fit.** Specific mission statement, audience specification, plan-first decomposition, simulate-before-execute.

**Weak.**
> Implement the token refresh feature.

Ambiguous on scope, trigger, test requirements, consumer.

**Strong.**
> Mission: fix the bug where auth tokens expire during uploads longer than 5 minutes.
>
> Root cause (confirmed): session refresh is gated on user activity events, which do not fire during a single long upload. Fix: add refresh on upload progress events (fired every 1MB by src/uploads/handler.py).
>
> Downstream: the verification worker will check (a) tests/test_token_refresh.py exists and passes, (b) the fix is called from src/uploads/handler.py, and (c) no other tests regress. Your output will be rejected if any of these fail.
>
> Before implementing: describe in one paragraph what the change will be, then implement.

Names the bug precisely, the confirmed root cause (worker doesn't re-diagnose), the downstream checks (worker knows the grade), requires simulate-before-execute.

**Break mode.** Worker produces a solution that "implements token refresh" abstractly but doesn't connect to the upload handler.

---

## Slot 5: Constraints

**Behavior needed.** Scope adherence and failure-mode suppression. Worker stays inside the boundary, no drift into "while I'm here."

**Why here.** Where scope creep and warmth drift are prevented. Most negative-prompting-heavy slot — mostly a list of things not to do.

**Strategies that fit.** Context budget cap, hybrid positive-negative scope, deviation rules, dehumanization, conditional activation.

**Weak.**
> Don't go out of scope.

Means nothing. Worker's notion of "scope" is its prior.

**Strong.**
> In scope: src/auth/token.py, src/uploads/handler.py, new file tests/test_token_refresh.py.
>
> Out of scope: refactoring unrelated code; adding features beyond the fix; updating documentation outside of inline comments on the changed lines; improving error messages in surrounding code.
>
> Budget: at most 5 files touched, at most 3 distinct logical tasks. If exceeded, emit `## SCOPE_EXCEEDED` with a decomposition plan.
>
> Deviation rules:
> - AUTO-FIX: bugs, missing critical functionality, or blocking errors in files you're already modifying.
> - ASK: architectural changes, new dependencies, refactors touching files outside scope.
> - DEFER: out-of-scope non-blocking issues. Add to `<deferred_work>`.
>
> Tone. No preamble. Do not hedge with "as an AI" or "this may or may not." State the change, support with evidence, stop.

Names exact in-scope files; names specific drift patterns; gives decision procedure for discovered work; caps tone.

**Break mode.** Worker produces a 40-file diff that "improves the module while fixing the bug." Reviewer has to find the fix inside unrelated refactoring.

---

## Slot 6: Success criteria

**Behavior needed.** Pre-handoff self-checking against falsifiable conditions. Worker verifies its own work before emitting the completion marker.

**Why critical.** Without falsifiable criteria, every worker output requires full orchestrator re-verification. With them, the worker does first-line verification; the orchestrator's job drops to spot-check.

**Strategies that fit.** Falsifiable success criteria, three-layer verification, "mostly done is failure" framing.

**Weak.**
> Make sure the feature works.

"Works" is a vibe.

**Strong.**
> Success criteria. You may not emit `## PHASE COMPLETE` until you have verified each. Run the commands; include results in your return.
>
> - [ ] `pytest tests/test_token_refresh.py -v` passes, all three cases green.
> - [ ] `grep -n "def refresh" src/auth/token.py` returns a new function.
> - [ ] `grep -n "refresh" src/uploads/handler.py` shows the new function is called.
> - [ ] `pytest tests/ -q` exits 0 (no regressions).
>
> Three-layer verification for every file you modified:
> - Existence: file on disk.
> - Substance: non-trivial content, not a stub.
> - Wiring: imports, exports, and call sites connect.
>
> Binary gate. "Mostly done" is failure. "Tests will pass after the reviewer adjusts them" is failure.

Every criterion is a runnable command. Worker can't claim done without having run them.

**Break mode.** Worker emits completion markers for 70%-done work. Orchestrator wastes an iteration catching gaps that structured criteria would have prevented.

---

## Slot 7: Return format

**Behavior needed.** Orchestrator-parseable output. Orchestrator extracts what it needs without interpreting prose; worker can't accidentally hide failure inside rambling.

**Why here.** Contract between worker output and orchestrator's next step. If the orchestrator has to read prose to figure out success, you have no contract.

**Strategies that fit.** Structured completion markers, content-per-field constraint, progressive disclosure, length control.

**Weak.**
> Summarize what you did.

Worker writes 500 words of prose. Orchestrator has to read it.

**Strong.**
> Return format:
>
> ```
> ## TL;DR
> One sentence: what you did. One sentence: key verification result.
>
> ## Changes
> - file: src/auth/token.py — added function `refresh_on_upload_progress`
> - file: src/uploads/handler.py — added call to `refresh_on_upload_progress` in progress-event handler
> - file: tests/test_token_refresh.py — new test file, 3 cases
>
> ## Verification
> - pytest tests/test_token_refresh.py -v: [output]
> - pytest tests/ -q: [exit code, output]
> - grep results for wiring checks: [output]
>
> ## Deferred
> [anything discovered but not fixed; empty if none]
>
> ## Marker
> ## PHASE COMPLETE
> ```
>
> Each Changes bullet must name a specific file and specific action. "Improved the module" is invalid — replace with the specific function or change.

Headers are machine-extractable. Content-per-field constraint prevents "improved the module" non-answers. Marker is standalone, not buried in prose.

**Break mode.** Orchestrator has to interpret free-form prose. Missing data discovered later, during a spot-check that doesn't find what it needs.

---

## Slot 8: Self-reflection (hidden)

**Behavior needed.** Pre-output quality gate with iteration. Worker evaluates its own draft against a rubric before emitting, iterating if below threshold. Hidden from final output.

**Why asymmetric.** Present → catches surface failures cheaply. Absent → those become orchestrator problems. Not needed for every task, but high-leverage when output quality is graded rather than binary.

**Strategies that fit.** Rubric-based self-reflection (hidden), simulate-before-execute.

**Weak.**
> Check your work before submitting.

Worker glances and moves on.

**Strong.**
> Self-reflection (hidden — do not include in final output).
>
> Before emitting, internally score your draft against this rubric. Any row below 4/5 means iterate; emit only when all rows ≥ 4.
>
> - [ ] Addresses every success criterion: 1–5
> - [ ] Claims supported by specific evidence (commands run, file contents verified): 1–5
> - [ ] Contains no hedges where definite claims are possible: 1–5
> - [ ] Return format matches the specified structure exactly: 1–5

Explicit rubric, iteration rule, gating condition, hidden-from-user.

**Skip when.** Task is pass/fail (test passed or didn't), not graded. Overhead doesn't earn its keep on binary tasks.

---

## Composition: how slots interact

- **Slot 1 bleeds into slot 4.** A role with a process pipeline pre-loads half the mission discipline. You can sometimes shorten slot 4 — but only if coherent (debugging-agent role and build-new-feature mission fight each other).
- **Slot 2 is useless without slot 5's read-before-write rule.** Listing files without mandating the read allows skimming.
- **Slot 6 is useless without slot 7.** Success criteria not reflected in return format get evaluated mentally by the worker and not reported.
- **Slot 5's dehumanization affects slot 7's output.** Kill warmth + ask for progressive disclosure → stark TL;DRs followed by spare bodies (usually what you want). Don't kill warmth → "Great question! Here's a TL;DR…"
- **Slot 8 depends on slot 6.** Reflection rubric should reference success criteria. Different quality dimensions → two competing graders; worker optimizes for whichever is louder.

## Skip discipline

You don't fill every slot every time. Skip ones the task doesn't need — but skip *deliberately*, not by forgetting.

Before dispatching, scan the 8 slots: "Which behavior does this slot induce, and does my task need it?" If "no," skip. If "I don't know," the slot goes in — cost of the unneeded slot is small vs. cost of drift into the behavior that slot would have prevented.

Under-fill failure: scope creep, hallucinated contents, non-falsifiable success. Over-fill failure: slot 5 becomes a wall of rules competing with mission. Under-fill is more destructive.

## When you don't need slots at all

If the work is your own (not a worker dispatch), reach for `strategies.md` directly. The slot structure is a template for a *prompt that ships*. Your own thinking doesn't need to be templated — it needs the right strategies applied at the right moments. Slots without dispatch is ceremony.
