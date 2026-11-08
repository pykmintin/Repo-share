# Elicitation

User-facing questions — moments where you stop and ask the user something rather than dispatching a worker or doing the work yourself. These are the highest-leverage moments in a session because the user is the bottleneck. A bad question wastes their time; a false binary actively misleads them.

The rest of this skill is about talking to workers or framing your own thinking. This file is about talking to the user. The discipline is different.

---

## The three rules

**Rule 1. Name the axis of choice before offering the choice.** If you can't state in one sentence what the real decision dimension is, you don't understand the problem well enough to ask anything. Go think first.

**Rule 2. One question per turn.** The user tolerates one well-framed question. Three stacked questions produce an answer to whichever one they pattern-matched first and silence on the rest.

**Rule 3. Commit and state, rather than ask, when you can.** Most "should I X or Y" questions are agent indecision dressed up as user respect. If either answer is defensible, pick one, state what you picked and why, let the user redirect if wrong. Faster, and better outcomes — user reacts to a concrete proposal rather than generating one from scratch.

---

## Naming the axis

Most common mistake: substituting a generic axis for the real one. Generic is easy to explain and produces a choice the user can make; the real axis is harder to articulate but produces a choice the user cares about.

Generic axes almost always wrong:

- "Fast or slow" → real axis is usually feasibility, risk, or dependency.
- "Simple or comprehensive" → real axis is usually throwaway vs. load-bearing.
- "Parallel or sequential" → real axis is usually shared-resources.
- "Creative or conservative" → real axis is usually who the output is for.
- "High-level or detailed" → real axis is usually act-now vs. reference-later.

When you reach for a generic axis, stop and ask: what specifically about this task makes one option better than the other? That's the real axis. Rephrase on it.

**Example.**

*Generic:* "Do you want a fast approach (Provider A) or a thorough approach (validate with all three)?"

*Real axis:* "The reason I'd use all three is to catch cases where Provider A silently misparses. The risk is high on transcripts that don't match Provider A's expected format. Do you know whether the transcripts match A's format, or should I validate across providers to find out?"

The second form doesn't ask for a choice — it asks for information that determines the right approach, committing to the implied action once the information is in.

---

## Scope questions

Scope is where misreading the user's frame is most destructive. They said "phase by phase" and you ask a project-wide question → you've demonstrated you didn't hear them. They'll either correct you (wastes time) or stop correcting you (worse).

Before asking any scope question, answer for yourself: what scope has the user signaled? Said "this phase" → phase scope. Said "this session" → session scope. Said nothing explicit → default to narrowest and let them widen.

**Weak.**
> There are a few things to figure out before we start. What's the state of the data? Are we working from real transcripts or synthetic ones? Should we initialize the project-wide state first, or jump straight into phase work? And do you have a preference on which transcripts to process first?

Four questions. Three scope levels. User has to unpack the whole thing before answering anything.

**Strong.**
> Working at phase scope as you said. For this phase, one question: which transcript do you want processed first? If no preference, I'll start with artifacts/logs/transcript_001.jsonl and move through in filename order.

One question. Scope honored. Default provided so the user can decline to answer and still get movement.

---

## Commit-and-state

Default assumption in most agent output is that every ambiguity requires user input. Wrong. Most ambiguities have a defensible default; the agent should pick it, state what was picked and why, let the user object.

Trade-off: asking respects the user's judgment but costs their time. Committing saves time but risks picking wrong. Right balance depends on the cost of being wrong. Cheap to reverse → commit. Expensive to reverse → ask.

**Rule of thumb.**
- **Commit** for defaults, tool choices, file naming, minor format decisions, most implementation details.
- **Ask** for scope changes, architectural decisions, destructive actions, anything that can't be undone in a minute.

**Weak.**
> Would you like me to write the scoreboard to artifacts/output/scoreboard.md or somewhere else? And in what format — markdown table, JSON, or YAML?

Two low-stakes questions, two reversible defaults, no reason to ask.

**Strong.**
> I'll write the scoreboard to artifacts/output/scoreboard.md as a markdown table. If you'd prefer a different path or format, say so and I'll adjust.

Commits, states, offers a redirect without requiring one.

---

## One-question discipline

Stacking questions is an agent tic — feels like thoroughness, produces partial answers and frustration.

When you have multiple things you'd like to know, pick the one whose answer most changes your next action. Ask that one. Defer the others — they often resolve themselves as a consequence of the first answer, or become clearly irrelevant.

**Weak.**
> Before I plan: (1) are we targeting Provider A, B, or both? (2) verified or unverified transcripts? (3) preferred test-coverage bar? (4) PII handling?

Four questions. User answers one and leaves the rest.

**Strong.**
> Before planning: are we targeting Provider A, both A and B, or all three? Once I know, I'll come back with a concrete plan and flag any other questions I hit.

One question. Names that follow-ups may come. Promises a concrete plan as next output, not more questions.

---

## When the user says the prompt is wrong

Specific pattern: user has read a prompt you drafted and said it's bad. Don't spend the next turn justifying, softening, or lightly editing. The whole prompt needs re-approaching.

Mistake: taking "this prompt is bad" as a request to fix a detail. Usually it's a request to fix the frame. User said "over-engineered" → fix isn't to trim a few lines, it's to ask "what's the simplest version that does the job" and draft that. User said "wrong perspective" → identify which perspective, rewrite from that stance.

**Weak.**
> You're right, let me tone down the voice. Here's a softer version. [Lightly edits tone, keeps 90% of the original.]

**Strong.**
> You're telling me the perspective is wrong, not the tone. Let me try again: what perspective did you want? [Or, if inferable:] I think you want the prompt written as if the worker is mid-task and needs a brief, concrete hand-off — not starting fresh needing full context. Is that right? [If yes, rewrite from that stance.]

---

## Shape of a good user-facing prompt

When you do need to ask:

1. **One sentence of context** — what you know, what's blocking.
2. **The question**, with axis named.
3. **A concrete default** you'll act on if the user doesn't respond.

**Template.**
> Context: I've scoped the phase around processing Provider A transcripts.
> Question: which transcript should I process first — the real one at artifacts/logs/real_001.jsonl, or a synthetic one to validate the pipeline first?
> Default if you don't say: I'll use the real transcript. If the parse fails I'll fall back to synthetic.

User can answer in one word, ignore and still get action, or redirect. Whatever they do, you move.

---

## Final check before asking

1. **Is the axis named and real?** Not "fast vs. slow," not "simple vs. comprehensive." Can't name it → not ready.
2. **Is it one question?** More than one → pick the one whose answer most changes next action, defer the rest.
3. **Could I have committed instead?** Cheap to reverse → commit and state.
4. **Is there a default?** User goes quiet → agent still moves.

Passes all four → respects user's time, advances work. Fails any → prompt for frustration.
