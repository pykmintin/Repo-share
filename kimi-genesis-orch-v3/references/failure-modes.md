# Failure Modes

Eleven patterns that orchestrators (and own-work agents) actually produce. Each entry has the mechanism, the catch (which audit/slot detects it), the counter-pattern, and a weak-vs-strong contrast.

Each pattern is tagged for its applicable use-case:

- **OWN-WORK** — fires when the agent is doing the work itself.
- **WORKER-PROMPT** — fires when the agent is composing a prompt for a downstream actor.
- **BOTH** — fires in either context.

When writing a new prompt or starting your own work, scan the eleven patterns. For each, ask "could what I'm about to produce trigger this?" If yes, apply the counter-pattern. Most outputs are vulnerable to 3+; the good ones close those specific holes.

---

## 1. Scope leap on initial framing  *(BOTH)*

**Pattern.** *Default-to-maximum-scope.* When task is ambiguous on scope, the actor defaults to the widest plausible interpretation — training rewards comprehensive over right-sized.

**Stronger version.** User asks "can you help me debug this function?" → agent re-architects the module. User asks "what are the tradeoffs of this approach?" → agent produces a ten-page comparison against three alternatives not mentioned.

**Catch.** Forcing question 3 (scope boundary), audit 5 (scope vs. budget).

**Counter.** Name the scope out loud — phase-level, file-level, whole-project — and let the user confirm. If the user said "phase by phase," the only right response is phase-by-phase until they widen it.

**Weak.**
> Let me get you set up. First question: what's the state of data recovery, and are we on real or synthetic data? Should we align project initialization before phase work?

Seven questions, three scope levels, no signal that the user's "phase by phase" was heard.

**Strong.**
> Working at phase scope as you said. For this phase, one question: which transcript first? I'll scope around your answer.

One question, phase-scoped, resolvable in one reply.

---

## 2. False binary on a generic axis  *(BOTH)*

**Pattern.** *Axis substitution.* Real decision axis is task-specific (feasibility, reversibility, dependency structure). Agent substitutes a generic axis (speed) because it's easy to explain; user has to reject the whole frame to give a useful answer.

**Stronger version.** "Simple or comprehensive?" when the real question is "throwaway or load-bearing?" "Creative or conservative?" when the real question is "user-facing or internal?"

**Catch.** Forcing question 4, audit 4.

**Counter.** Before offering a choice, name the real axis in writing. If you can't name it, you don't understand the problem.

**Weak.**
> Parallel (faster, harder) or sequential (slower, simpler). Which?

**Strong.**
> The real axis is whether the two workers will touch overlapping files. If yes, parallel produces merge conflicts. Do you expect overlap?

---

## 3. Making the user the tool  *(WORKER-PROMPT, sometimes OWN-WORK when the agent could read but asks instead)*

**Pattern.** *Delegation misframing.* Agent treats agent dispatches as scarce and user time as cheap — actual economics reversed.

**Stronger version.** "Can you paste this 500-line file?" (worker can read it.) "Run this command and tell me what it prints." (worker can run.) "Check whether tests pass." (worker can check.)

**Catch.** Audit 3.

**Counter.** Mechanical work → worker. User time → judgment calls only.

**Weak.**
> Could you run the tool against each transcript and paste the output?

**Strong.**
> I'll dispatch a worker to run the tool against all transcripts and write a summary to artifacts/output/tool_run_summary.md. You don't need to do anything during the run.

---

## 4. Kitchen-sink recon prompts  *(WORKER-PROMPT)*

**Pattern.** *Over-specification at the prompt level.* Agent loads worker prompt with everything that might be useful rather than the minimum needed. Worker drowns and produces shallow coverage of everything.

**Stronger version.** Research prompts asking the worker to "comprehensively survey, compare tradeoffs, identify gaps, recommend a path forward" when the real need is "is there prior work that does X."

**Catch.** Forcing question 1, audit 2.

**Counter.** Define minimum output. Everything in the prompt must trace to that output. Doesn't trace → delete.

**Weak.**
> You are a research agent. Inventory every transcript. For each, run every parser. Record row count, parse errors, schema, token count. Approximate semantic scan. Comprehensive report.

**Strong.**
> Mission: determine which provider parses the most transcripts. Success artifact: artifacts/output/provider_scoreboard.md, one row per provider: `provider | transcripts_parsed | total | %_success`. Method: each provider against each transcript, count successes, write scoreboard. Nothing else. Do not investigate failures yet.

---

## 5. Instructing the physically impossible  *(WORKER-PROMPT, OWN-WORK if you commit to an impossibility yourself)*

**Pattern.** Agent gives an instruction the actor literally cannot execute — "eyeball this 10GB transcript," "manually review every file."

**Catch.** Audit 1 (simulate the actor).

**Counter.** Read your prompt as the actor. If an instruction is impossible, the prompt needs re-thinking.

**Weak.**
> Eyeball the transcripts in ./logs/ for obvious file operations.

**Strong.**
> Run `scripts/extract_file_ops.py` against each transcript in ./logs/. The script emits JSONL of operations. Output: a table aggregating counts per operation type.

---

## 6. Helpfulness-driven scope expansion  *(BOTH — most insidious form is OWN-WORK)*

**Pattern.** *Helpfulness expansion.* When a successful task surfaces an insight, the agent tries to propagate it everywhere it might be relevant — producing a large change set where a small one was wanted. Motivated by care; the cost is unreviewable output and buried signal.

**Stronger version.** A bug fix that becomes a module rewrite. A one-line documentation correction that becomes a full-document restructure. A new finding from a session triggers rewrites of four admin documents at once.

**Catch.** Audit 5 (scope vs. budget) + the out-of-scope clause in slot 5.

**Counter.** New insights get captured as *notes*, not propagated as *changes*, until the user explicitly asks to propagate. Default to the smallest change that captures the insight in one place.

**Weak.**
> Based on this session's findings, I'll rewrite AUDIT_PLAN.md to reflect the new decisions, update ORCHESTRATOR.md to align with the new workflow, revise PHASE2_CONTEXT.md to include the new context, and add a changelog entry.

**Strong.**
> From this session, three new decisions are worth capturing:
> 1. Phase scope, not project scope, is the default working unit.
> 2. Feasibility is the choice axis, not speed.
> 3. Subagent dispatches are cheap; reserve user input for judgments.
>
> I'll write these as a brief note in artifacts/sessions/<date>-note.md. If you want them propagated into AUDIT_PLAN.md or ORCHESTRATOR.md, say so explicitly and I'll do that as a separate, scoped task.

---

## 7. Revision loops that look like progress  *(WORKER-PROMPT, but pattern is in orchestrator's own behavior)*

**Pattern.** Agent asks worker for a revision. Worker returns something different that doesn't clearly resolve the issues. Three rounds later, fixing something each iteration but not converging.

**Stronger version.** Test-fix oscillation where each fix breaks a previously-passing test. Doc-edit loops where each revision introduces a new inconsistency.

**Catch.** Post-dispatch revision cap + stall detection + fresh-spawn revision.

**Counter.** Cap at 3. Between iterations, count blocker+warning issues — if the count doesn't decrease, escalate. Revision is a new worker with previous output + issues, not a continuation.

---

## 8. Format theater  *(BOTH)*

**Pattern.** Output specifies structure (bullets, JSON, sections) without specifying content. Actor produces output meeting the structural spec — correctly-formatted bullets, valid JSON — but content is generic, superficial, or reformulated from the prompt.

**Why.** RLHF rewards outputs that human raters can easily evaluate. Structured outputs are easy to evaluate. Structure alone is easier than structure-plus-substance.

**Catch.** Slot 7 (return format) with content-per-field constraints.

**Counter.** Every structural requirement gets a content requirement that forces substance. "Use bullets" → "each bullet must contain a specific file path or command."

**Weak.**
> Respond with three sections: Problem, Approach, Next Steps. Use bullet points.

Output: three sections, three bullets each, each bullet generic ("Address the problem," "Consider the approach").

**Strong.**
> Respond with three sections:
> - Problem: one paragraph. Must include the specific file, line, and observed behavior demonstrating the bug.
> - Approach: bullets. Each bullet names a specific function or file and the specific change proposed.
> - Next Steps: bullets. Each is a runnable command or a specific file to be modified.
> Generic bullets that don't name specific files, lines, or commands are invalid — revise.

---

## 9. Confident-wrong on unread files  *(BOTH)*

**Pattern.** Actor produces code or analysis for a file it did not actually read, based on what the file name and context suggest. Output often works on the most obvious case and breaks on anything the actual file does that the actor didn't anticipate.

**Why.** Model's training includes plausible-looking code that doesn't correspond to any specific real codebase. Absent a forcing function to read the real file, it interpolates from training data. Confident because the model is always confident; wrong because it's made up.

**Catch.** Slot 2 (read set) with mandatory read protocol; for own-work, the read-before-write cognitive move.

**Counter.** Make reading an invariant the actor can check: "if you have not called ReadFile on this path, your output is invalid." Verifiable from the tool-call log.

**Weak.**
> Modify src/auth/token.py to add a refresh-on-upload method. The module already has a refresh method to follow as a pattern.

**Strong.**
> HARD RULE: before any edit, call ReadFile on src/auth/token.py. Output containing edits without a prior ReadFile call is invalid.
>
> After reading, modify src/auth/token.py to add a refresh-on-upload method.

---

## 10. Checklist theater in success criteria  *(BOTH)*

**Pattern.** Success criteria framed as a checklist, but items aren't falsifiable — vibes phrased as checkboxes. "Code works. Tests pass. Style is good." Actor checks them off without verifying anything specific.

**Why.** Checklists feel like a rigor upgrade over unstructured requests, but the structure alone doesn't produce verification. Non-falsifiable items mean the checklist is a prop.

**Catch.** Slot 6 (success criteria) with the falsifiability test.

**Counter.** Every criterion becomes a command the actor runs. If it can't be a command, it's not a criterion. "Tests pass" isn't a criterion; `pytest tests/ -q exits 0` is.

**Weak.**
> Success criteria:
> - [ ] Code works correctly
> - [ ] Tests pass
> - [ ] Style is clean

**Strong.**
> Success criteria. Each is a command you run; include the output in your return.
> - [ ] `pytest tests/test_token_refresh.py -v` passes, all three test cases green.
> - [ ] `pytest tests/ -q` exits 0 (no regressions).
> - [ ] `ruff check src/auth/token.py` exits 0.
> - [ ] `grep -rn "refresh_on_upload_progress" src/` returns at least one match in src/uploads/handler.py.

---

## 11. Conversation-into-success on a failing actor  *(BOTH — applies to your own iteration as much as worker iteration)*

**Pattern.** Actor fails. The next message continues the conversation: "Hmm, that's not quite right. Could you fix the test case on line 42?" Actor replies with another attempt. Over 3-4 rounds the output doesn't converge — each fix creates or reveals a different problem.

**Why.** Actor's context is polluted by the reasoning that produced the original failure. Correction applied on top of bad priors rather than replacing them. Model is also biased toward agreeing with the framing of what's wrong, even when that framing misdiagnoses.

**Catch.** Post-dispatch discipline (in SKILL.md), not a slot. For own-work: when your own output is rejected, restart rather than patch.

**Counter.** Revision is a fresh actor invocation. For workers: new prompt with previous output + specific issues. For your own work: re-do from scratch with the user's correction as input, don't try to patch the failed analysis.

**Weak sequence.**
> [Worker 1 produces buggy output]
> [Orchestrator] That's close but the refresh handling has a race condition. Add a lock?
> [Worker 1] Sure, added a lock. [Output still wrong, differently]
> [Orchestrator] The lock is in the wrong place. Put it inside the try block?

**Strong sequence.**
> [Worker 1 produces buggy output, emits ## PHASE COMPLETE]
> [Orchestrator spot-checks, finds race condition, terminates worker 1]
> [Orchestrator dispatches worker 2 with: original prompt, worker 1's output, specific issues: "race condition between token refresh and upload progress handler — two concurrent requests can use the same expired token"]
> [Worker 2 reads the output, diagnoses the race, produces a fix]

Worker 2 sees the failure as data, not its own mistake. Diagnosis isn't colored by having produced the failure.

---

## How to use this file

Two times to scan:

**Before action.** When writing a new prompt or starting a substantial own-work piece, run the eleven patterns: "could my next move trigger this?" Pre-empt with the counter-pattern.

**After failure.** When something went wrong, map it to whichever pattern fits. The mapping is the diagnosis; the counter-pattern is the fix. If the failure doesn't match any of the eleven, add it as a new pattern.
