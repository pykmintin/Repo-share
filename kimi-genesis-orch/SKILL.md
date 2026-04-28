---
name: orchestrator-prompts
description: Use whenever you are about to think hard for the user OR write a prompt for another agent. Teaches cognitive strategies that make either work — same toolkit, two use-cases. Trigger on drafting/dispatching/revising a worker prompt, ingesting a non-trivial user message, asking the user a clarifying question mid-orchestration, or doing complex own-work where the temptation is to skip ingestion and dive in. Do not skip the preflight on first load — without it, this skill is a list of words the agent didn't internalize. Make sure to use this skill whenever the user describes a non-trivial task, hands you new project information, or asks for a worker prompt — even when the user doesn't name "prompts" or "orchestration" explicitly.
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

Read these files, in order. You don't need to memorize. You need to know what's where so you can reach for it during use.

1. `SKILL.md` — framing, 4 forcing questions, 5 audit checks, catalog index.
2. `references/strategies.md` — strategy catalog. Each entry has dual application (cognitive move + worker-prompt language) and a narrative case. Both pieces are load-bearing.
3. `references/failure-modes.md` — named failures, each tagged for own-work / worker-prompt / both.
4. `references/slots.md` — the 8-slot structure (worker-prompt construction only).

When done, write one sentence: the single claim this skill makes that most changes how you would have approached the user's first message before reading. This is your Phase 0 marker.

Do not proceed until that sentence is written.

## The 4 forcing questions

Before any non-trivial action — drafting a prompt, ingesting a user message, picking a next move — answer these four in writing, in your own words. If you can't, you aren't ready. Don't skip by saying "obvious" — writing the answer is what verifies the thinking.

**1. Success artifact.** What will exist after I finish?
- *Applied to your own work:* what document, code change, or decision will be on disk or surfaced to the user that they can inspect?
- *Applied to a worker prompt:* what file or output will the worker produce that you can inspect without asking them?

If the answer contains "complete," "implemented," "handled," or "done" — rewrite. Those aren't inspectable.

**2. Read set.** Which exact files, messages, or artifacts must be grounded against?
- *Applied to your own work:* what does your next move need to be informed by? Be exact about paths and which user message.
- *Applied to a worker:* exact paths the worker must read first.

"Figure out what's relevant" is not delegable — to a worker, or to your own future self.

**3. Scope boundary.** What's the smallest piece of work that produces the artifact?
- Larger than ~3 tasks or ~5 files → decompose.
- Applies to own thinking too: an overly broad ingestion produces a calcified plan.

**4. Dimension of choice (if user-facing).** If your next move is to ask the user something, name the real axis in writing first. "Fast vs. slow" usually hides feasibility, reversibility, or dependency. Name the real axis — not a generic one.

## The 5 audit checks (pre-action)

Before sending a prompt OR committing to your own next move, answer five in writing. A check that fails means re-think, not push-through.

**1. Simulate the actor.** Read the prompt as the worker / read your plan as the future-you executing it. Is any instruction physically impossible? An impossibility is a symptom, not a fixable detail — re-think the whole approach.

**2. Locate the success test.** Point to the exact line that says how you'll know you're done. No such line → not ready. Line exists but isn't falsifiable → decoration.

**3. Check the delegation frame.** Are you asking the user to do mechanical work that you (or a worker) could do? User time is the scarcest resource — workers and your own thinking are cheap by comparison.

**4. Check for false binaries.** Does your choice have more than two real options? Is the axis you've named the real one? Generic "fast vs. slow" usually hides feasibility.

**5. Check scope against context budget.** More than ~3 tasks or ~5 files? Decompose. One too-big task produces worse output than two right-sized tasks every time.

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
