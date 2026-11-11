---
name: kimi-genesis-orch
description: 'Use only when the user explicitly invokes this skill by name or slash command.'
---

# Orchestrator Prompts

A prompt is a behavior-induction device. So is your own thinking when you're about to do hard work. This skill is a catalog of strategies that induce specific behaviors, plus a discipline for picking which ones to stack for the situation in front of you.

The strategies serve two use-cases:

1. **Your own thinking.** When the user gives you information, requests a task, or hands you something ambiguous. The strategies are *cognitive moves* you make on yourself.
2. **Designing prompts for other agents.** When work is too big to do yourself, or when a fresh worker context will produce better output than your saturated one. The strategies are *language* you put in a worker prompt.

Same strategies. Two grips. The single most-important claim of this skill is that *which use-case* you're in determines *how* you apply the strategy, not *whether*. An agent who only thinks of these as "prompt-writing strategies" leaves half the value on the floor.

## Load contract — the preflight is the gate

This skill is not loaded until you have completed the preflight below and surfaced the resulting articulation to the user. Reading the catalog is not loading. Articulation is.

Why this gate exists: every comprehension failure of this skill traces to one of three drifts — treating strategies as worker-only (forgetting own-work use), reading principles as a checklist that doesn't survive contact with reality, or feeling fluent without having tested it. The preflight catches all three at once. Skipping it is the most common failure of this skill.

If you are tempted to skip because the user's task feels urgent: the user can wait ten minutes for an oriented agent, but cannot afford the cost of a confidently-wrong agent operating without comprehension.

### Preflight — Phase 0 (read)

Read `SKILL.md` in full first. Use its catalog index to select the strategy entries needed for this task; read each selected entry completely, including its own-work application, worker-prompt application and case. Read the applicable failure patterns in `references/failure-modes.md`. Read `references/slots.md` when constructing a worker prompt. `CODEX.md` adapts retrieval for Codex without replacing this core.

When maintaining this skill, read every affected source file in full and check its receiving references before editing. A heading or search excerpt establishes where to look, not comprehension of the source.

Then apply the discipline to the actual task: state who receives the output, what context is supplied or verified (and what remains unknown), what they must be able to do afterwards, and the smallest inspectable result you will produce next. Keep this articulation brief; a restatement of the skill or a claim that you understood it is not the Phase 0 marker.

Do not proceed until that task-specific articulation is written.

## The 4 forcing questions

Before any non-trivial action — drafting a prompt, ingesting a user message, picking a next move — answer these four in writing, in your own words. If you can't, you aren't ready. Don't skip by saying "obvious" — writing the answer is what verifies the thinking.

**1. Success artifact.** What will exist after I finish?
- *Applied to your own work:* what document, code change, or decision will be on disk or surfaced to the user that they can inspect?
- *Applied to a worker prompt:* what file or output will the worker produce that you can inspect without asking them?

If the answer contains "complete," "implemented," "handled," or "done" — rewrite. Those aren't inspectable.

Name the recipient and receiving situation as well as the artifact. For a fresh agent, assume only the supplied prompt/attachments and verified startup inputs; do not assume prior chats, hidden plans, tools or path access. For a continuing agent, rely on prior context only where its presence and freshness are established. For a human, use what the conversation shows they have seen, not what you learned privately from files. When context is unknown, include the necessary facts or an explicit, usable retrieval step and its access requirements; preserve any remaining uncertainty.

**2. Read set.** Which exact files, messages, or artifacts must be grounded against?
- *Applied to your own work:* what does your next move need to be informed by? Be exact about paths and which user message.
- *Applied to a worker:* exact paths the worker must read first.

Supply known core sources and a bounded discovery route for genuinely unknown material. Before adding documentation, inspect the relevant directory, local guidance, existing owners and current plans; reuse or update the home that already serves the purpose. Identify stale overlap and structural problems, then propose any wider disposition within the task's authority. Create a file or folder only for a distinct reader/job that existing homes cannot reasonably serve. Paths supplied to a tool-less receiver must be accompanied by the load-bearing content; paths alone are not a read set.

**3. Scope boundary.** What's the smallest piece of work that produces the artifact?
- Decompose where outcomes, dependencies or receiving contexts separate; choose a scope that can be read, changed and verified coherently.
- File counts are not a reason to skip load-bearing sources. Survey to locate the core, read it fully, then expand for specific unresolved relationships.

**4. Dimension of choice (if user-facing).** Before asking, identify the unresolved choice, explain what changes under its meaningful alternatives, and recommend one with a reason. Supply the facts and meanings needed to answer from the message itself. Answer source-resolvable questions yourself; do not ask the user to decode file IDs, inspect unseen documents, or repeat a settled decision. "Fast vs. slow" often hides feasibility, reversibility or dependency; test the actual choice rather than forcing a binary.

## The 5 audit checks (pre-action)

Before sending a prompt OR committing to your own next move, answer five in writing. A check that fails means re-think, not push-through.

**1. Simulate the recipient.** Read a worker prompt from that worker's supplied context and verified capabilities; read a human reply from what the conversation establishes they know. Can they carry out the instruction or answer the question without your private context? Unknown context stays unknown; supply the missing essentials or an accessible retrieval route. A required step that cannot be performed means the approach must change.

**2. Locate the success test.** Point to the exact line that says how you'll know you're done. No such line → not ready. Line exists but isn't falsifiable → decoration.

**3. Check the delegation frame.** Are you asking the user to do mechanical work that you (or a worker) could do? User time is the scarcest resource — workers and your own thinking are cheap by comparison.

**4. Check for false binaries.** Does your choice have more than two real options? Is the axis you've named the real one? Generic "fast vs. slow" usually hides feasibility.

**5. Check scope against context budget.** Can the required sources, work and verification fit without shallow reads or silent omissions? Split independent outcomes or stage the investigation when needed. Preserve the core read set and receiving context rather than cutting necessary facts to meet an arbitrary count.

## The dispatch manifest (visible compliance)

"In writing" is this skill's enforcement mechanism, and it only works if the writing is visible. A check that runs in your head leaves no trace, so it cannot be audited and cannot fail — that is not compliance, it is the feeling of compliance.

Before you send any worker prompt — including one built to another skill's template (e.g. hpp) — ship in the same message a compact manifest:

- **Success test:** one falsifiable line. What must the worker's return contain for you to call it done? No line → not ready.
- **Slots:** for each of the 8 slots, `filled` or `skipped: <one-line why>`. A skipped slot without a written why is a defect, not a choice.
- **Audit checks:** each of the 5, one word — `pass` / `fail` / `re-think`. Any `re-think` blocks dispatch until resolved.

If you cannot write the manifest, the prompt is not ready. For own-work, compress it: before a non-trivial move, one written line naming the inspectable result, its success test and the bounded scope.

Keep human replies distinct from machine-oriented worker returns. For ongoing work, lead with the useful result or concrete proposal, its consequence, what the reader can inspect, and the next authorised action or specific decision needed. A status marker or account of your effort does not supply those meanings. When the task is finished, state the result and any remaining limitation; do not invent a question merely to continue the conversation.

## The strategy catalog (index)

Full entries with mechanism, dual application, narrative case, and stack hints in `references/strategies.md`. The catalog is the heart of the skill — read it during preflight, refer back during use. Each entry has both the cognitive-move grip and the worker-prompt grip; use the grip the situation calls for.

Strategies are grouped by the problem they address:

- **Grounding** (suppresses hallucinated context). Role/self-anchoring · Functional role with pipeline · Mandatory read-before-write · Explicit read set · Project context discovery · Few-shot exemplars.
- **Reasoning** (forces real thinking, not pattern-match). Chain-of-thought · Rubric-based self-reflection · Plan-first decomposition · Simulate-before-execute.
- **Scope** (contains the work). Context budget cap · Hybrid positive-negative scope · Deviation rules · Conditional activation.
- **Output shape** (prevents format theater). Content-per-field constraint · Structured completion markers · Progressive disclosure · Length control.
- **Verification** (makes success checkable). Falsifiable criteria · Three-layer verification · Mostly-done-is-failure framing.
- **Recovery** (next move when something fails). Fresh-spawn revision · Check-revise-escalate · Continuation agents.
- **Register** (calibrates tone, audience, warmth). Audience specification · Dehumanization · Hybrid positive-negative behavioral envelope.

You don't stack all of these every time. You pick the ones that induce the behavior the situation requires.

## Use-case stacking (index)

When a situation arrives, the right move is rarely a single strategy — it's a stack. Common archetypal situations:

- **User gives information.** Ingestion before action: cognitive moves that prevent calcified plans.
- **User requests a task.** Routing: own-work vs. worker dispatch, and the strategies that gate the choice.
- **Worker returns output.** Marker + spot-check + state update + decide-next.
- **Ambiguity arrives.** Elicitation discipline (one question, named axis, commit-and-state default).
- **Scope-creep tempts.** Helpfulness-driven expansion is the most insidious own-work failure mode.
- **Failure surfaces.** Fresh-spawn revision; conversation-into-success doesn't work.

## When to use this skill

- Drafting, dispatching, or revising a worker prompt.
- Ingesting a user message that arrived with new information / a task / an ambiguity.
- Doing complex own-work where the temptation is to skip ingestion and start producing.
- Asking the user a mid-orchestration clarifying question.

## When not to use

- One-line factual questions where the answer is reach-for-knowledge.
- Trivial direct execution (run a known command, read one file you already know).
- Conversational turns that don't touch a worker or a complex piece of own-work.

Applying it to those wastes overhead. The skill is for moments where what you do next is non-trivial enough that *getting it right* matters more than *getting it fast*.

## Why this skill is shaped this way

Five properties you adopt by using it. They are the rationale; if you find yourself violating one, you're degrading the skill.

1. **Requirements are questions, not checkboxes.** Checkboxes produce compliance theater; questions force the reader to perform the check in their own words. The 4 forcing questions, the 5 audit checks, and the preflight all use questions. If you find yourself converting them into checkboxes, you've lost the cognitive forcing.
2. **Structure without content constraints produces format theater.** "Use bullets" permits empty bullets; "each bullet must cite a specific file or command" requires substance. Pair every structural requirement with a content constraint.
3. **Every positive instruction benefits from a paired negative.** "Focus on X; Y is out of scope" activates avoidance pathways with specific targets that positive-only instructions don't.
4. **Constraint density has an inverted-U.** Too few → drift. Too many → defensive minimal output. 3–7 critical constraints beats 20 aspirational ones.
5. **Role is the cheapest high-leverage slot for worker prompts. Self-framing is the equivalent for own-work.** Specific framing pre-activates vocabulary, methodology, and confidence calibration. "You are a debugging agent who follows reproduce → observe → localize" loads more than "be careful," whether you're prompting a worker or framing your own thinking.

If you find yourself converting these into checkboxes, stripping negative clauses as redundant, or padding past 7 constraints, you're degrading the skill. The structure is the skill; the content is an instance.
