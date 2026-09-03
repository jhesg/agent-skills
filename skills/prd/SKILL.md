---
name: prd
description: Write or update a product requirements document: problem and evidence, users and jobs, goals with measurable targets, scope, user stories, requirements, dependencies, launch and measurement. Use whenever the user says PRD, product requirements, product brief, one-pager for a feature, 'what should we build for X', or wants product agreement before design. Delegates genuinely contested product decisions to the council skill and cites the decision records. Do not use for how to build it (spec, system-design, api-design).
---

# Product requirements

Produce a product requirements document: problem, users, goals, scope, requirements, launch. One file, `prd.md`, that a team can review, challenge, and revise for as long as the question stays open. Decisions inside it that are genuinely contested go to the council skill; this skill owns the document, council owns the reasoning.

## Why this split

A document skill that argues its own hard calls ends up defending them. Sending contested decisions to an independent panel, and citing the record it produces, keeps this document honest and keeps the reasoning reusable when the question reopens. It also keeps this skill small: it knows what a good product requirements contains, not how to adjudicate every trade-off inside one.

## Files

| File | Purpose |
|---|---|
| `references/template.md` | Section list with guidance per section, plus Decision records, Changelog, Feedback |
| `references/review-checklist.md` | What to verify before delivering |
| `references/council-handoff.md` | How to send a decision to council and cite the result |

## Workflow

### 1. Intake

Read everything the user pointed at: their message, files, repo, existing docs. Fill the template. Tag every section `given` (from the user or sources), `inferred` (you derived it, say from what), or `missing`. Do not fill a `missing` section with invention; a confident-looking blank is worse than a visible gap.

If a section that decides the document's shape is `missing`, ask, at most 3 questions, then continue. For `product requirements` those are usually the first three sections of the template. Everything else can carry a proposed default in Open questions.

### 2. Find the contested decisions

Walk the draft and list every place where two or more credible options exist. For each, decide: contested or not.

Contested means all of: two or more credible options, hard to reverse or weeks of consequence, and either stakeholders disagree or the trade-off is not obvious from the constraints. Typical contested decisions in a product requirements:

- scope cuts between must and should
- primary success metric
- target segment for v1
- build vs buy vs partner
- launch: gated, staged, or full

Uncontested decisions you make inline, with a one-line reason, in the section where they apply. Contested ones go to council, at most 3 per draft unless the user asks for more. The rest become Open questions with a proposed default. Why the cap: each council run is several agent calls; a document with eight panels is a document nobody waits for.

### 3. Delegate to council

Follow `references/council-handoff.md`. In short: build a council brief with `PURPOSE: record`, `RECORD PATH: <doc dir>/decisions/NNNN-<slug>.md`, and `CONTEXT` naming this document and section. Run council. When the record exists, write the decision into the section as one sentence plus a link to the record. Do not restate the trade-offs; the record owns them.

If council is not installed, say so and ask the user to install it (`claude plugin install council@jhesg-agent-skills`). Do not run a mini-panel inline; one decision engine.

### 4. Draft

Write `prd.md` from the template. Sections:

| Section | What goes there |
|---|---|
| Problem statement | One paragraph. Who hurts, how, how often. No solution language. |
| Evidence | Data, quotes, tickets, support volume, competitor moves. Each with a source. Assertions without a source are marked as such. |
| Users and jobs | Segments and the job each is trying to get done. Primary segment for v1 named. |
| Goals and metrics | Table: goal, metric, baseline, target, measurement window. One primary metric. |
| Non-goals | What we will not do in this version, and why, so it stops coming back. |
| Scope | Must, should, won't for this version. Every must traces to a goal. |
| User stories and flows | As-a / I-want / so-that, grouped by segment. Key flows in steps or a Mermaid diagram. |
| Requirements | Functional requirements, each tagged with the story it serves and must/should. Non-functional where the product cares: speed, accessibility, locales. |
| UX notes | Constraints and references for design. Not the design. |
| Dependencies and risks | Teams, systems, legal, data. Risk, likelihood, mitigation. |
| Launch and measurement | Rollout shape, audience, kill criteria, when we read the metric and what we do at each outcome. |
| Alternatives considered | One line per alternative and why not. Contested ones link a decision record. |
| Open questions | Each with an owner and a proposed default. |
| Decision records | Table: decision, record path, status |
| Changelog | One line per round |
| Feedback | Empty, for the user |

Prose is for reasoning; tables are for anything with three or more parallel items. Keep the first section readable by someone who reads nothing else.

### 5. Review

Run `references/review-checklist.md` against the draft. Fix what fails. Anything you cannot fix goes to Open questions with an owner.

### 6. Deliver

Write the file where the user asked, or `docs/prd/<slug>.md` by default. Send it (`SendUserFile` when available). Report which decisions went to council and which were made inline.

## Iteration

When invoked with a path to an existing `prd.md` and its Feedback section is non-empty:

1. Read the feedback. Classify each item: content change, or challenge to a recorded decision.
2. Content changes: edit the section in place.
3. Decision challenges: open that decision's council `plan.md`, put the feedback in its Feedback section, re-trigger council on it. Council rewrites the record in place with a History line. Update the citing section from the new record.
4. Append one Changelog line naming what moved. Clear the Feedback section.
5. Send the updated file.

Rounds are unlimited. The user stops by not re-triggering. If Feedback is empty, say so and stop; nothing to do.

## Output

1. `prd.md` at the chosen path
2. `decisions/NNNN-<slug>.md` per council run, next to the document
3. A short report: sections tagged `inferred` or `missing`, decisions delegated, decisions inline, open questions
