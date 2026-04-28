# Orchestrator Prompts — v3 (Full)

**What this is:** A skill that teaches an AI assistant how to write better prompts for other AI agents, and how to think more clearly before doing complex work itself.

**The problem it solves:** Most agents reflexively either (a) dump a vague task description into a worker prompt and hope for the best, or (b) skip thinking and start producing immediately. Both produce garbage. This skill forces a discipline: name the success artifact, define the read set, bound the scope, choose strategies that induce the right behavior, then act.

---

## How to load this into Claude

1. Open Claude (web or desktop app).
2. Start a new project or open an existing one.
3. In the project settings, look for **"Custom Instructions"** or **"Project Instructions."**
4. Paste the contents of `SKILL.md` into the instructions field.
5. Tell Claude: *"Load the orchestrator-prompts skill. Run the preflight."*
6. Claude will read the skill and ask you about your project before doing anything.

**Alternative:** If your Claude setup supports file references, point it at this entire folder and say *"Use the orchestrator-prompts skill in this folder."*

---

## What's in the box

| File | What it does |
|------|-------------|
| `SKILL.md` | The core. Framing, 4 forcing questions, 5 audit checks, strategy catalog index, when to use / when not to. |
| `references/strategies.md` | The full strategy catalog. Every strategy has two "grips" — how to apply it to your own thinking, and what text to put in a worker prompt. Also includes narrative cases (real examples of failure and success). |
| `references/failure-modes.md` | 11 named anti-patterns. Each has a mechanism, a catch (which audit detects it), a counter-pattern, and weak-vs-strong examples. |
| `references/stacking.md` | 6 archetypal situations (user gives info, user requests task, worker returns, ambiguity arrives, scope-creep tempts, failure surfaces). Shows which strategies to stack in which order for each. |
| `references/slots.md` | The 8-slot template for worker prompts. Each slot induces one class of behavior. Weak-vs-strong examples for every slot. |
| `references/elicitation.md` | How to ask the user a good clarifying question. One question per turn, named axis, commit-and-state default. |
| `assets/preflight.md` | The comprehension protocol. Phase 0 = read files. Phase 1 = internalize (dual-application check, narrative anchoring, articulation). Phase 2 = surface to user. |
| `assets/articulation.md` | Template for the articulation document you produce during preflight Q3. |

**Total size:** ~98 KB (~25,000 tokens). This is the complete skill. Nothing cut.

---

## How it works (plain language)

When you give Claude a non-trivial task, the skill makes it do this instead of winging it:

1. **Preflight.** Read the skill, pick 3 strategies you'll lean on, write an articulation showing you understand the project. Don't skip this — it's the gate.
2. **Forcing questions.** Before any action, answer 4 questions in writing: What's the success artifact? What's the read set? What's the scope boundary? What's the dimension of choice (if asking the user something)?
3. **Audit checks.** Before sending any prompt or committing to action, run 5 checks: simulate the actor, locate the success test, check delegation frame, check for false binaries, check scope against budget.
4. **Pick strategies.** Work backwards from the behavior you need to the strategy that induces it. Don't stack everything — 3-7 critical constraints beats 20 aspirational ones.
5. **Fill slots (if dispatching).** If the work goes to a worker, use the 8-slot template: Role → Read set → Project context → Mission → Constraints → Success criteria → Return format → Self-reflection.
6. **Scan failure modes.** Before action, ask "could my next move trigger this?" After failure, map it to a pattern.

---

## When to use this

- Drafting, dispatching, or revising a worker prompt.
- Ingesting a user message that arrived with new info / a task / ambiguity.
- Doing complex own-work where the temptation is to skip thinking and start producing.
- Asking the user a mid-orchestration clarifying question.

## When NOT to use this

- One-line factual questions.
- Trivial direct execution (run a known command, read one file you already know).
- Conversational turns that don't touch a worker or complex own-work.

---

## Why v3 is "full"

This version ships every strategy, every failure mode, every archetype narrative, every slot example, every elicitation rule, and the full preflight exercise. It's the complete teaching corpus. Use this when you want the agent to have access to everything — all the narrative cases, all the cognitive-move grips, all the stacking guidance.

**Trade-off:** ~25K tokens of context. That's substantial. If you're token-budget constrained or the agent only needs worker-prompt construction (not the full own-work + elicitation + archetype routing stack), consider v4 (medium) instead.
