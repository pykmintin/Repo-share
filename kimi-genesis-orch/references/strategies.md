# Strategy Catalog

Each strategy is a piece of cognitive language with a known mechanism and a known effect. Every entry has two grips:

- **As your own cognitive move** — what the strategy looks like applied to your own thinking when you ingest, plan, or do work yourself.
- **As worker-prompt language** — the specific text you put in a prompt to a downstream worker.

Same strategy. Two grips. Pick the grip the situation calls for.

You work backwards from behavior to strategy, never forwards. If you find yourself thinking "I should add chain-of-thought here," stop and ask what behavior you actually need. If the behavior is "externalize reasoning on a multi-step task," CoT is right. If the behavior is "produce correct output," CoT isn't automatically the answer.

## Contents

- [Grounding](#grounding) — Role/self-anchoring · Functional pipeline · Mandatory read-before-write · Explicit read set · Project context discovery · Few-shot exemplars
- [Scope](#scope) — Context budget cap · Hybrid positive-negative · Deviation rules · Conditional activation
- [Output shape](#output-shape) — Content-per-field · Structured markers · Progressive disclosure · Length control
- [Verification](#verification) — Falsifiable criteria · Three-layer · Mostly-done-is-failure
- [Register](#register) — Audience specification · Dehumanization · Hybrid behavioral envelope
- [Reasoning](#reasoning) — Rubric-based self-reflection
- [Recovery](#recovery) — Fresh-spawn revision
- [Choosing strategies](#choosing-strategies)

---

## Grounding

Makes the actor (you, or a worker) act on real state rather than priors. Grounding failures are the most common and most destructive class — an actor writing code based on imagined file contents is worse than one that did nothing.

### Role / self-anchoring (specific credentials)

**Mechanism.** Role tokens at prompt start receive attention from every later position, biasing generation toward the register, vocabulary, and methodology the role implies. Specific credentials activate richer knowledge networks than generic ones.

**As your own cognitive move.** Before you start working on something, name in writing what role you're operating in. "I'm operating as a refactoring auditor in this turn — my job is to find what's load-bearing, not to defend the original." This loads vocabulary and methodology before you do the work, the same way it would for a worker.

**As worker-prompt language.**
> You are a senior backend engineer with 10 years of distributed-systems experience, specializing in event-driven architectures.

**Narrative case.** A user asked an agent to evaluate two design proposals. Without self-anchoring, the agent defaulted to "helpful comparison" — produced a balanced both-sides summary. With self-anchoring ("you are a staff engineer who has been on-call for the system being changed"), the agent surfaced the actual operational risk of proposal B that the balanced summary had elided.

**Stack hints.** Pairs naturally with functional-pipeline (next entry) and conditional-activation (later) when the same agent serves multiple modes.

**Avoid.** Generic "you are an expert." Activates nothing specific. Fictional awards and grandiose credential inflation add tokens without adding activation.

**Slot (worker-prompt use):** 1.

### Functional role with process pipeline

**Mechanism.** Names a sequence the actor must follow, making the sequence part of the role rather than a separate instruction. Sequence-as-identity is more binding than sequence-as-task.

**As your own cognitive move.** When the work has a known correct sequence (debugging, ingesting a user message, planning a phase), name the sequence at the top of your turn and explicitly walk it. "Process: ingest → cross-reference → identify the gap → propose. I will not propose before identifying the gap."

**As worker-prompt language.**
> You are a debugging agent. Your process is: reproduce → observe → hypothesize → test → localize → propose fix. You do not skip steps. You do not propose a fix before localizing the cause.

**Narrative case.** Without a pipeline, an agent asked to debug a failing test went straight to "here's a fix that should work" — without reproducing or localizing. The fix was plausible-wrong. With a pipeline, the same agent reproduced the failure, observed the actual stack trace, and surfaced that the test was wrong, not the code.

**Stack hints.** Pairs with self-anchoring above; reduces the need for a long mission slot.

**Slot:** 1, influences 4.

### Mandatory read-before-write protocol

**Mechanism.** "You MUST ReadFile before WriteFile" is phrased as an invariant the actor can verify against its own tool-call sequence. Self-enforcing in a way vague "be careful" instructions aren't.

**As your own cognitive move.** Before you write about or modify a file you haven't read in this session, read it. Treat your own memory of the file as a hypothesis, not a fact. If you say "the file currently contains X" without having read it this session, you have hallucinated.

**As worker-prompt language.**
> HARD RULE. Before modifying any file, call ReadFile on that file. Output containing edits without a prior ReadFile call is invalid.

**Narrative case.** An agent edited a config file based on what the file "usually" looks like — wrote two lines that already existed and removed a critical line that had been added since the agent's last read. With the protocol, the agent re-read first, saw the new line, and produced a clean edit.

**Stack hints.** Always combines with explicit-read-set (next entry).

**Slot:** 2 + 5.

### Explicit read set (paths, not descriptions)

**Mechanism.** Exact paths are auditable — orchestrator can verify via tool-call log. "Read the relevant context" is not auditable and usually produces the wrong reads.

**As your own cognitive move.** When you're planning your own next move, name the exact files / messages you need to ground against in writing — paths, not descriptions. "I need to re-read the user's last two messages and the failing test output at tests/test_X.py line 42." Catches "I have a feeling about this" and forces you to ground.

**As worker-prompt language.**
> Files to read, in order:
> - src/auth/token.py
> - src/auth/test_token.py
> - docs/auth_contract.md
> Read all three before any other action.

**Narrative case.** Without an explicit set, a worker asked to "audit the auth module" read 14 files (most irrelevant), saturated context, produced a shallow audit. With an explicit 3-file set, the worker read deeply and produced a sharper audit.

**Stack hints.** Always paired with mandatory-read-before-write (above).

**Slot:** 2.

### Project context discovery

**Mechanism.** Points at project-specific convention files (CLAUDE.md, AGENTS.md, README, style guides) and mandates reading. Training doesn't know your project's conventions; the project has documented them.

**As your own cognitive move.** On entering a new project context, read its convention file before doing anything else. Even when the user says "just do X" — your X-in-this-project may differ from X-in-general by the project's conventions. The convention file is the agent's primary grounding.

**As worker-prompt language.**
> Before drafting: read CLAUDE.md for conventions and .claude/skills/ for applicable skills. Apply whatever they document.

**Narrative case.** Without convention reading, a worker added error handling using `return None` on error paths — the project's convention is `raise`. The reviewer rejected the PR. With a CLAUDE.md read mandate, the worker matched the project style.

**Slot:** 3.

### Few-shot exemplars

**Mechanism.** Models pattern-match against examples more reliably than descriptions. One concrete input→output anchors format, tone, and depth in ways paragraphs of description don't.

**As your own cognitive move.** Before producing a structured output (a commit message, a release note, a prompt), look up one good example of that shape from earlier in the project (or a sibling project). Match its shape rather than improvising from description.

**As worker-prompt language.**
> Example of the expected output format:
> ```
> FIX: auth token expires during long uploads
>
> Cause: session refresh was gated on user activity, missed during multi-minute uploads.
> Fix: refresh on upload progress events.
> ```
> Match this shape for each fix you commit.

**Narrative case.** Without an example, a worker asked for "a clear commit message" produced a verbose paragraph. With one example, the worker matched its terse shape.

**Avoid.** On verifiable-answer tasks (math, lookups). The example anchors style; if there's a correct answer, the example adds bias without value.

**Slot:** 7, can reinforce 4.

---

## Scope

Contains the work. Default failure is expansion — actors trained to be helpful add features, fix tangential issues, over-document. Scope strategies are almost all negative-prompting in some form.

### Context budget cap

**Mechanism.** Hard numerical caps on tasks and files make scope auditable. The actor can check whether it has exceeded; exceeding triggers a specific response, not a silent overrun.

**As your own cognitive move.** Cap your own work in writing before starting. "I will touch at most 3 files in this turn. If the work expands past 3, I stop and decompose rather than push through." This prevents helpfulness-driven expansion you'd otherwise rationalize.

**As worker-prompt language.**
> You may touch at most 5 files. At most 3 distinct logical tasks. If the work requires more, stop and emit `## SCOPE_EXCEEDED` with a decomposition plan.

**Narrative case.** Without a cap, an agent asked to "fix the bug" produced a 12-file diff that improved adjacent error handling, refactored helper functions, and updated documentation. With a cap, the same agent emitted SCOPE_EXCEEDED on noticing the bug fix touched the limit, surfacing the discovered work as deferrable.

**Slot:** 5.

### Hybrid positive-negative scope

**Mechanism.** Pairs "in scope" with "explicitly out of scope." Negative half activates avoidance pathways with specific targets, preventing "while I'm here" drift.

**As your own cognitive move.** When you start a task, write down both halves: "I am doing X. I am explicitly NOT doing Y, even though Y is related." The negative half is what catches you mid-drift.

**As worker-prompt language.**
> In scope: fixing the token refresh bug in src/auth/token.py.
> Out of scope: refactoring unrelated code; adding tests beyond the one required to prove the fix; updating documentation outside inline comments. If you notice out-of-scope issues, add them to `<deferred_work>` but do not act on them.

**Narrative case.** "Improve error handling" without a negative half → agent rewrites every error path it touches. With "in scope: error handling on the upload flow; out of scope: error handling elsewhere even if seemingly related" → tight diff.

**Slot:** 5.

### Deviation rules (auto-fix / ask / defer)

**Mechanism.** Names a decision procedure for work the actor discovers during execution. Three labeled paths instead of a binary between "strictly stay in scope" (misses real bugs) and "be helpful" (unbounded expansion).

**As your own cognitive move.** When mid-task you notice something out-of-scope, classify it before reacting: AUTO-FIX (blocking, in-file), ASK (architectural), DEFER (out-of-scope, non-blocking). The classification gates your response.

**As worker-prompt language.**
> If you discover work not in your task list:
> - AUTO-FIX: bug, missing critical functionality, or blocking error in a file you're already modifying.
> - ASK: architectural change, new dependency, or refactor touching files outside scope.
> - DEFER: out-of-scope, not blocking. Add to `<deferred_work>`.

**Narrative case.** Worker noticed an unrelated typo while fixing a bug. Without deviation rules → either fixed it (scope creep) or ignored it (lost). With → DEFER, captured in `<deferred_work>`, surfaced to orchestrator for separate dispatch.

**Slot:** 5.

### Conditional activation / mode switching

**Mechanism.** Different instructions for different modes, selected by an explicit trigger. Keeps the prompt focused on the active mode rather than covering every case generally.

**As your own cognitive move.** When you can serve multiple modes (planner / executor / verifier), name which mode you're in at the top of your turn. "Mode: planner. I am not executing in this turn." Suppresses cross-mode bleed.

**As worker-prompt language.**
> Mode: EXECUTOR. (Not planner. Not verifier.) Follow the executor rules below only. Ignore instructions labeled for other modes.

**Narrative case.** Worker prompt that tried to cover planner-and-executor in one shot produced a weak plan and a half-finished implementation. Split into two prompts (mode: planner, then mode: executor), each produced strong output.

**Slot:** 1 or 5.

---

## Output shape

Makes output parseable and prevents format theater. Format without content constraints produces organized-looking emptiness.

### Content-per-field constraint

**Mechanism.** A constraint on the *content* of a structural element, not just the element. "Use bullet points" permits empty bullets; "each bullet must contain a concrete code example" requires actual content.

**As your own cognitive move.** When you produce a structured output, audit each field: does this contain substance, or is it format? "Each bullet has a specific file/line; each section answers the heading question with concrete content."

**As worker-prompt language.**
> Use bullet points. Each bullet must include a concrete example (a specific file, a specific command, a specific line of code). Bullets that only restate concepts are invalid — revise.

**Narrative case.** Asked for a "report with three sections," worker produced three sections of generic prose. Asked again with content-per-field ("each bullet must name a specific file and a specific action"), worker produced the same three sections with substance.

**Slot:** 7.

### Structured completion markers

**Mechanism.** Worker ends with an exact machine-parseable string. Orchestrator matches by regex rather than interpreting prose. Turns "is the worker done" from a judgment call into a boolean.

**As your own cognitive move.** When you finish a substantive piece of work, name the marker explicitly. Don't trail off into prose — declare done in a way the user (or a downstream check) can verify. Even a "Status: COMPLETE" or "Status: NEEDS-INPUT" line at the bottom of your output gives the next reader a contract.

**As worker-prompt language.**
> Your final message must contain exactly one of:
> - `## PHASE COMPLETE` — all success criteria met, all artifacts verified.
> - `## CHECKPOINT REACHED` — you require human input.
> - `## SCOPE_EXCEEDED` — work exceeds the allowed budget.
> - `## ISSUES FOUND` — blockers prevent completion.
> Absence of a marker means output is invalid.

**Narrative case.** Without markers, orchestrator had to read 800-word worker returns to figure out success state. With four markers, orchestrator could grep the marker in milliseconds and route accordingly.

**Slot:** 7.

### Progressive disclosure (summary-first)

**Mechanism.** Answer has two layers: short top-layer summary, detailed body below. Matches attention availability — reader sees the answer first, can stop or drill in.

**As your own cognitive move.** Lead with the answer. State the conclusion in one or two sentences before the reasoning. The reader who needs only the conclusion stops; the reader who needs reasoning continues.

**As worker-prompt language.**
> Structure as:
> 1. TL;DR — two sentences. First states the answer; second states the key constraint or caveat.
> 2. Details — full reasoning, as many paragraphs as the task needs.

**Narrative case.** A research worker's verbose 1200-word output buried the answer in paragraph 4. Same worker with progressive disclosure: 2-line TL;DR up top, full reasoning below — orchestrator could decide in 10 seconds whether to read further.

**Slot:** 7.

### Length control (contextual, not absolute)

**Mechanism.** Absolute word counts are arbitrary. Contextual anchors map length to purpose.

**As your own cognitive move.** Before producing a long output, name its length anchor in writing. "Length: short enough that an on-call engineer can decide whether to escalate within 30 seconds." This calibrates the output to its use, not to a number.

**As worker-prompt language.**
> Length: short enough that an on-call engineer can decide within 30 seconds whether to page the author. Longer if detail is load-bearing; shorter if not.

**Narrative case.** "Make it concise" produced a 450-word reply. "Length anchored to a 30-second decision window" produced an 80-word reply that the on-call could actually use.

**Slot:** 5 or 7.

---

## Verification

Makes success checkable. Without it, "done" is the actor's self-report — not evidence.

### Falsifiable success criteria

**Mechanism.** Each criterion is empirically checkable, not a vibe. "User can log in" is vibe; "POST /login returns 200 with a valid JWT for a known-good user and 401 for a known-bad one" is falsifiable.

**As your own cognitive move.** Before declaring your own work done, name the criterion as a runnable check. If you can't, you don't know yet whether you're done. Reach for the strongest check available — a command, a file existence, a string match — not a feeling.

**As worker-prompt language.**
> Success criteria. You may not emit `## PHASE COMPLETE` until you have verified each:
> - [ ] `tests/test_token_refresh.py` exists and passes (`pytest tests/test_token_refresh.py`).
> - [ ] `src/auth/token.py:refresh_on_upload_progress` is called from `src/uploads/handler.py`.
> - [ ] No other tests regress (`pytest tests/ -q` exits 0).
> "Mostly done" is failure.

**Narrative case.** Worker reported "feature implemented." Spot-check found tests didn't exist. With falsifiable criteria including a `pytest` command the worker had to run, the worker either ran it and reported pass/fail or emitted ISSUES FOUND.

**Slot:** 6.

### Three-layer verification (existence → substance → wiring)

**Mechanism.** Existence checks the file is there. Substance checks it has real content (not a stub). Wiring checks it's connected (called, imported, registered). A file can exist without substance; substantive can be orphaned.

**As your own cognitive move.** When you finish work that creates or modifies code, walk the three layers in your head before declaring done. New function? Confirm it exists, has substance, and has at least one caller. All three matter.

**As worker-prompt language.**
> Before declaring done, for every file touched:
> - Existence: confirm the file exists on disk.
> - Substance: confirm content is non-trivial (not stub, not commented-out).
> - Wiring: confirm imports, exports, and call sites connect. New functions have at least one caller.

**Narrative case.** Worker wrote a beautiful new utility function. Three-layer check caught: function exists, has substance, but is never called from anywhere. Orphaned. Re-dispatch fixed the wiring.

**Slot:** 6 or 8.

### "Mostly done is failure" framing

**Mechanism.** Explicit framing that partial completion isn't acceptable. The actor can't hedge by claiming most of the work is done.

**As your own cognitive move.** Refuse the soft landing. If a criterion is unmet, the work is not done — even if "almost everything" is done. Either ship complete or surface specific gaps.

**As worker-prompt language.**
> This is a binary gate. Either every success criterion passes and you emit `## PHASE COMPLETE`, or at least one fails and you emit `## ISSUES FOUND` with the specific failures. "Mostly done" is failure. "I'll leave the last one for later" is failure.

**Narrative case.** Worker reported "4 of 5 criteria passed, 5th will pass after small adjustment." Without mostly-done-is-failure framing, orchestrator might have accepted. With it, worker emitted ISSUES FOUND with the 5th criterion's specific failure — orchestrator dispatched a fresh worker on just that gap.

**Slot:** 6.

---

## Register

Calibrates tone, audience, warmth. RLHF biases models toward warmth, which is often wrong.

### Audience specification

**Mechanism.** Names who the reader is. Model adapts vocabulary, assumed knowledge, depth.

**As your own cognitive move.** Before producing an output, name the reader. "This goes to the user, who is a developer with full project context." Or: "This goes to a worker who has zero context and needs full briefing." The audience determines what to assume vs. spell out.

**As worker-prompt language.**
> Audience: a senior systems engineer who knows Linux internals and is debugging a performance regression. Assume familiarity with perf, strace, kernel scheduling. Do not explain basics.

**Narrative case.** Worker producing a "report" without audience defaulted to "explain everything from scratch." Same worker with audience spec produced a tight report that started at the project's actual conceptual level.

**Slot:** 4 or 5.

### Dehumanization (reduce warmth bias)

**Mechanism.** Explicitly instructs against RLHF-trained warmth. Patterns leak as "Great question!" preambles and over-apologetic hedges.

**As your own cognitive move.** When the user values directness, kill warmth in your own output. Don't open with "Great question," don't apologize for the model's nature, don't hedge on definite claims. State, support, stop.

**As worker-prompt language.**
> Do not open with 'Great question' or similar. Do not hedge with 'this may or may not,' 'it depends,' or 'as an AI.' State the answer, support it with evidence, stop.

**Narrative case.** A debugging worker produced "Thanks for the question! I'd be happy to help. As an AI, I should mention that there could be many causes…" Same worker with dehumanization: skipped to the diagnosis.

**Slot:** 5.

### Hybrid positive-negative behavioral envelope

**Mechanism.** Every behavioral axis gets a "do X" and "do not do Y" clause. Pair defines a narrower envelope than either alone.

**As your own cognitive move.** When you can name a likely behavioral drift, name both halves to yourself. "I'm focusing on the bug. I'm not adding security advice unprompted, not suggesting unrelated refactors, not apologizing for the code's existence."

**As worker-prompt language.**
> Positive: focus solely on resolving the bug described. State what you did and why.
> Negative: do not provide unsolicited security advice. Do not suggest unrelated refactors. Do not apologize for the bug's existence.

**Narrative case.** Worker fixing a bug also added six lines of unrelated security advice. Hybrid envelope ("do not provide unsolicited security advice") suppressed the next session's drift.

**Slot:** 5.

---

## Reasoning

Forces real thinking rather than pattern-match.

### Rubric-based self-reflection (hidden)

**Mechanism.** The actor evaluates its own draft against an explicit rubric before producing final output, iterating if the rubric isn't met. Simulates the human-rater evaluation RLHF was trained on.

**As your own cognitive move.** Before sending a substantive response, score it against 3-4 rubric rows in your head — does it address every requirement? Are claims supported? Is there a hedge that should be a definite claim? If any row scores poorly, revise before sending. Hide the rubric from the user — they see the result.

**As worker-prompt language.**
> Before emitting final output: internally score against this rubric (do not show to the user):
> - Does it address every requirement? (0/1 each)
> - Are claims supported by specific evidence? (0/1 each)
> - Does it surface trade-offs?
> If any category scores below full marks, iterate. Emit only when rubric passes.

**Narrative case.** Without self-reflection, an agent's first-draft analysis missed two requirements the user had asked for. With it, the same agent caught both during the rubric pass and revised before sending.

**Avoid.** Pass-fail tasks (a test passes or doesn't). Overhead without benefit.

**Slot:** 8.

---

## Recovery

Runs after a worker fails. Not about the worker — about the orchestrator's next move.

### Fresh-spawn revision (not conversation)

**Mechanism.** Failing worker's context is polluted by the reasoning that led to the failure. Continuing conversation asks it to correct against the same priors. Fresh worker with previous output plus explicit issue list doesn't carry those priors.

**As your own cognitive move.** When your own analysis fails (you misread something or produced something the user rejected), don't keep editing the failed analysis. Restart with the user's correction as input and the failed analysis as data — not as a base to patch.

**As worker-prompt language (orchestrator logic).**
> Revision is a new worker invocation, not a continuation. Its input: (a) the previous worker's output, (b) the issues found, (c) the original prompt. It does not see the previous worker's reasoning.

**Narrative case.** Worker produced buggy auth code. Orchestrator continued conversation: "fix the race condition." Worker added a lock in the wrong place. "Move the lock" — worker moved it to a different wrong place. Fresh-spawn with the explicit race description: clean fix.

**Slot:** Orchestrator behavior, not a worker prompt slot.

---

## Choosing strategies

Behavior → strategy, never the reverse. The composition order:

1. Name the success artifact. (Forcing question 1.)
2. For the actor (you, or a worker) to produce it, which behaviors must they exhibit? List them.
3. For each behavior, pick one strategy. Prefer the simplest that covers it.
4. If applied to a worker prompt: place strategies in their fitting slots (see `slots.md`). If applied to your own thinking: just apply them in order.
5. If two strategies conflict, resolve before action. Conflicts produce "format theater with hedges."

A common composition for a worker prompt:

- Slot 1: Role anchoring + functional pipeline (if sequenced work).
- Slot 2: Mandatory read protocol + explicit path list.
- Slot 3: Project context discovery.
- Slot 4: Specific mission + audience + simulate-before-execute (if intricate).
- Slot 5: Context budget cap + hybrid positive-negative + deviation rules + dehumanization.
- Slot 6: Falsifiable criteria + three-layer verification + "mostly done is failure."
- Slot 7: Structured markers + content-per-field + progressive disclosure.
- Slot 8: Rubric self-reflection (if quality graded).

For your own thinking, the equivalent stack varies by use-case archetype.
