# plan.md template

The single file the user takes away. Written by the Chairman at the end of Stage 5 to `<run>/plan.md` and sent to the user. The user edits the Feedback section and re-triggers; the Chairman reads it back in Stage 0 of the next round.

Why one file: the user should not need to reopen the run directory to react. Everything they can act on, and everything they might disagree with, sits in one place with a blank section to answer in.

```markdown
# Council plan — round <n>

run: <absolute run dir>
previous: <path to previous plan.md, or "none">
date: <ISO date>

## Decision brief
<frozen brief, verbatim, tags kept>

## Verdict
<verdict block, verbatim>

## This week
<Executor Stage 5 plan, verbatim>

## Panel scores
| Adviser | Evidence | Actionability | Total |
|---|---|---|---|
<one row per adviser, summed over four reviewers>

## Where to read more
- Transcript: <run>/transcript.html
- Takes: <run>/outbox/<role>/stage2.md
- Reviews: <run>/outbox/<role>/stage3.md

## Feedback
<!-- Write here. Anything you disagree with, facts the panel got wrong, constraints they missed,
     a stakeholder to add, a verdict you want re-tested. Then re-trigger: /council <this file>. -->

```

## Re-trigger from feedback

When `/council` is invoked with a `plan.md` path, or the user says "re-run the council with my notes":

1. Read the file. If `## Feedback` is empty, say so and stop; nothing to re-run on.
2. New run dir, `round = previous + 1`. Log a `note` linking the previous run.
3. Rebuild the brief from the previous brief plus the feedback. Feedback lines are `given`. Where feedback contradicts a previous field, the feedback wins and the old value goes into a `PRIOR ROUND` block along with the previous verdict, so the panel argues against the last answer instead of repeating it.
4. Guard still runs. Feedback that only says "looks good" fails the stakes check: there is no new decision. Say so.
5. Continue from Stage 1 as normal. Same five advisers, fresh contexts. Old agents are gone with the old session anyway.
6. New `plan.md` carries `previous:` pointing to the old one, so rounds chain.
