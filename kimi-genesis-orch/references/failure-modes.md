# Failure Modes

Patterns that orchestrators (and own-work agents) actually produce. Each entry has the mechanism, the catch (which audit/slot detects it), the counter-pattern, and a weak-vs-strong contrast.

Each pattern is tagged for its applicable use-case:

- **OWN-WORK** — fires when the agent is doing the work itself.
- **WORKER-PROMPT** — fires when the agent is composing a prompt for a downstream actor.
- **BOTH** — fires in either context.

When writing a new prompt or starting your own work, scan the patterns. For each, ask "could what I'm about to produce trigger this?" If yes, apply the counter-pattern. Most outputs are vulnerable to 3+; the good ones close those specific holes.

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

**Before action.** When writing a new prompt or starting a substantial own-work piece, run the patterns: "could my next move trigger this?" Pre-empt with the counter-pattern.

**After failure.** When something went wrong, map it to whichever pattern fits. The mapping is the diagnosis; the counter-pattern is the fix. If the failure doesn't match any of the patterns, add it as a new pattern.
