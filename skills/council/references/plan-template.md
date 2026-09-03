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
- Decision record: <run>/decision-record.md
- Transcript: <run>/transcript.html
- Takes: <run>/outbox/<role>/stage2.md
- Reviews: <run>/outbox/<role>/stage3.md

## Feedback
<!-- Write here. Anything you disagree with, facts the panel got wrong, constraints they missed,
     a stakeholder to add, a verdict you want re-tested. Then re-trigger: /council <this file>. -->

```

## Re-trigger from feedback

When `/council` is invoked with a `plan.md` path, or the user says "re-run the council with my notes":

1. Read the plan. If `## Feedback` is empty, say so and stop; nothing to re-run on.
2. Follow the `Decision record:` link in the plan. That file is the canonical record for this decision, wherever the user has put it. If the link is dead, ask for the path or fall back to creating a fresh record and say so.
3. New run dir, `round = previous + 1`. Log a `note` linking the previous run and the record path.
4. Rebuild the brief from the record's current sections plus the feedback. Feedback lines are `given`. Where feedback contradicts a previous field, the feedback wins and the old value goes into a `PRIOR ROUND` block along with the previous verdict, so the panel argues against the last answer instead of repeating it.
5. Guard still runs. Feedback that only says "looks good" fails the stakes check: there is no new decision. Say so, and offer to mark the record `accepted` instead.
6. Continue from Stage 1 as normal. Same five roles, fresh contexts.
7. Stage 6 on an update round: write a new `plan.md` in the new run dir with `previous:` pointing at the old one, and **rewrite the canonical record in place** following `adr-template.md`, appending a History line. The plan is per round; the record is one file for the life of the decision.
8. Send the new plan and the updated record. Iterations are unlimited. The user ends the loop by not re-triggering, or by asking to mark the record `accepted`, which writes the status and a final History line without convening.
