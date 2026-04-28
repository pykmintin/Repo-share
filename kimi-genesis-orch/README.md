# Orchestrator Prompts — v4 (Medium)

**What this is:** A slimmer version of the orchestrator-prompts skill. Same core discipline — think before acting, name the artifact, bound the scope, fill the slots — but with the pedagogical scaffolding trimmed to the load-bearing minimum.

**The problem it solves:** Same as v3. Most agents reflexively dump vague tasks into workers or skip thinking entirely. This skill forces the discipline. The difference is v4 cuts the content that's valuable for *learning* the skill but not necessary for *using* it once loaded.

---

## How to load this into Claude

1. Open Claude (web or desktop app).
2. Start a new project or open an existing one.
3. In the project settings, look for **"Custom Instructions"** or **"Project Instructions."**
4. Paste the contents of `SKILL.md` into the instructions field.
5. Tell Claude: *"Load the orchestrator-prompts skill. Run the preflight."*
6. Claude will read the skill and ask you about your project before doing anything.

**Alternative:** If your Claude setup supports file references, point it at this folder and say *"Use the orchestrator-prompts skill in this folder."*

---

## What's in the box

| File | What it does |
|------|-------------|
| `SKILL.md` | The core. Framing, 4 forcing questions, 5 audit checks, strategy catalog index, preflight Phase 0 (read order), when to use / when not to. |
| `references/strategies.md` | Strategy catalog — **load-bearing sections only.** Grounding, Scope, Output shape, Verification, Register (complete). Plus Rubric self-reflection, Fresh-spawn revision, and the Choosing strategies composition table. |
| `references/slots.md` | The full 8-slot template for worker prompts. Every slot, every interaction rule, skip discipline. |
| `references/failure-modes.md` | 5 failure patterns (not 11). The ones most relevant to worker-prompt construction and recovery: Kitchen-sink prompts, Scope expansion, Format theater, Checklist theater, Conversation-into-success. |

**What's NOT here (deliberately cut):**

| Cut from v3 | Why it's gone |
|-------------|---------------|
| `stacking.md` (archetype narratives) | Teaches *how to learn* the skill. Not needed once loaded. |
| `elicitation.md` (user-facing questions) | Valuable for agents that talk to users a lot. If your use-case is mostly worker dispatch, this is overhead. |
| `articulation.md` (preflight template) | Part of the learning exercise. The preflight Phase 0 read order is inlined into SKILL.md instead. |
| Chain-of-thought, Plan-first, Simulate (from Reasoning) | Own-work reasoning strategies. If you're mostly writing worker prompts, you don't need these. |
| Check-revise-escalate, Continuation agents (from Recovery) | Loop management. If your workflow is single-prompt dispatch, not revision loops, these don't fire. |
| Strategies to suspect (placebo list) | Nice to know. Not load-bearing. |
| Failure modes 1-3, 5, 7, 9 | Scope leap, False binary, User-as-tool, Physically impossible, Revision loops, Confident-wrong. Relevant to own-work and specific scenarios. Cut for worker-prompt focus. |

**Total size:** ~58 KB (~15,000 tokens). **42% smaller than v3.**

---

## How it works (plain language)

Same as v3, but with less reading before the agent gets to work:

1. **Preflight.** Read 4 files (not 6). Write one sentence: the claim that most changes how you'd approach the user's first message. That's it. No Phase 1-2 exercise — the skill assumes the agent can apply strategies without the full narrative-anchoring workbook.
2. **Forcing questions.** Same 4 questions. Same audit checks. Same discipline.
3. **Pick strategies.** Reach into the catalog. Same composition order. Same slot placement.
4. **Fill slots.** Same 8-slot template. All interactions documented. Skip discipline included.
5. **Scan failure modes.** 5 patterns instead of 11. The ones that matter for prompt construction.

---

## When to use v4 instead of v3

**Use v4 (medium) when:**
- Token budget matters. You need the skill loaded in every worker context.
- The agent's job is primarily **worker-prompt construction**, not extensive own-work + user negotiation.
- You don't need archetype narratives or the full preflight exercise — just the template and the strategy language.
- You've already learned the skill and want the operational reference, not the teaching corpus.

**Use v3 (full) when:**
- You want the complete teaching corpus — every narrative case, every cognitive-move grip, every archetype.
- The agent does extensive own-work, user-facing elicitation, and multi-turn orchestration.
- Token budget is not a constraint.
- You're still learning the skill and want the full scaffolding.

---

## How this was built

v4 was derived from v3 through systematic testing. We ran the full skill against stress scenarios, then ran a skeleton (SKILL.md only) version, then asked the skeleton what it missed. The answer: `slots.md` and the worker-prompt language from `strategies.md` were the highest-value missing pieces. Everything else was either already inferable from SKILL.md or relevant only to specific use-cases.

The cut content saves ~10,000 tokens with no quality loss on worker-prompt-heavy scenarios.
