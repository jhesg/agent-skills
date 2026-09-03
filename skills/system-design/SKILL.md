---
name: system-design
description: Write or update a system design document: components, data flow, storage and consistency, capacity estimates, failure modes, security, operations, cost. Use whenever the user says system design, architecture doc, 'how should we build the platform for X', redesign a subsystem, scale something, or wants an architecture review artefact. Delegates genuinely contested architecture decisions to the council skill and cites the decision records. Do not use for a single feature inside an existing design (spec), product requirements (prd), or API surface (api-design).
---

# System design

Produce a system design: components, data flow, capacity, failure modes, operations. One file, `system-design.md`, that a team can review, challenge, and revise for as long as the question stays open. Decisions inside it that are genuinely contested go to the council skill; this skill owns the document, council owns the reasoning.

## Why this split

A document skill that argues its own hard calls ends up defending them. Sending contested decisions to an independent panel, and citing the record it produces, keeps this document honest and keeps the reasoning reusable when the question reopens. It also keeps this skill small: it knows what a good system design contains, not how to adjudicate every trade-off inside one.

## Files

| File | Purpose |
|---|---|
| `references/template.md` | Section list with guidance per section, plus Decision records, Changelog, Feedback |
| `references/review-checklist.md` | What to verify before delivering |
| `references/council-handoff.md` | How to send a decision to council and cite the result |

## Workflow

### 1. Intake

Read everything the user pointed at: their message, files, repo, existing docs. Fill the template. Tag every section `given` (from the user or sources), `inferred` (you derived it, say from what), or `missing`. Do not fill a `missing` section with invention; a confident-looking blank is worse than a visible gap.

If a section that decides the document's shape is `missing`, ask, at most 3 questions, then continue. For `system design` those are usually the first three sections of the template. Everything else can carry a proposed default in Open questions.

### 2. Find the contested decisions

Walk the draft and list every place where two or more credible options exist. For each, decide: contested or not.

Contested means all of: two or more credible options, hard to reverse or weeks of consequence, and either stakeholders disagree or the trade-off is not obvious from the constraints. Typical contested decisions in a system design:

- synchronous vs asynchronous boundaries
- storage engine and data ownership
- consistency model
- hosting and runtime
- build vs buy for a component
- multi-tenant vs per-tenant isolation

Uncontested decisions you make inline, with a one-line reason, in the section where they apply. Contested ones go to council, at most 3 per draft unless the user asks for more. The rest become Open questions with a proposed default. Why the cap: each council run is several agent calls; a document with eight panels is a document nobody waits for.

### 3. Delegate to council

Follow `references/council-handoff.md`. In short: build a council brief with `PURPOSE: record`, `RECORD PATH: <doc dir>/decisions/NNNN-<slug>.md`, and `CONTEXT` naming this document and section. Run council. When the record exists, write the decision into the section as one sentence plus a link to the record. Do not restate the trade-offs; the record owns them.

If council is not installed, say so and ask the user to install it (`claude plugin install council@jhesg-agent-skills`). Do not run a mini-panel inline; one decision engine.

### 4. Draft

Write `system-design.md` from the template. Sections:

| Section | What goes there |
|---|---|
| Context and scope | What system, what boundary, what is explicitly outside it. |
| Requirements | Functional in bullets. Non-functional as numbers with how each is measured: latency percentiles, throughput, availability, durability, RPO/RTO. |
| Constraints | Team, budget, hosting, compliance, deadlines, existing systems that cannot change. |
| Architecture | Component list with one-line responsibility each, then a Mermaid diagram. Every arrow in the diagram appears in Data flow. |
| Data flow | The main paths, step by step: request, write, read, async, failure. Which component owns each step. |
| Storage and consistency | What is stored where, why that engine, consistency guarantees per path, retention. |
| Capacity | Table: dimension, current, 12-month, assumption. Show the arithmetic, not just the result. |
| Failure modes | Table: component, failure, blast radius, detection, mitigation, recovery. Include dependency outages. |
| Security | Trust boundaries, authn/authz per boundary, secrets, data classification. |
| Operations | Deploy, rollback, observe, on-call runbook pointers, cost line. |
| Migration and rollout | How we get from today's system to this one without a stop-the-world. |
| Alternatives considered | One line per alternative and why not. Contested ones link a decision record. |
| Open questions | Each with an owner and a proposed default. |
| Decision records | Table: decision, record path, status |
| Changelog | One line per round |
| Feedback | Empty, for the user |

Prose is for reasoning; tables are for anything with three or more parallel items. Keep the first section readable by someone who reads nothing else.

### 5. Review

Run `references/review-checklist.md` against the draft. Fix what fails. Anything you cannot fix goes to Open questions with an owner.

### 6. Deliver

Write the file where the user asked, or `docs/system-design/<slug>.md` by default. Send it (`SendUserFile` when available). Report which decisions went to council and which were made inline.

## Iteration

When invoked with a path to an existing `system-design.md` and its Feedback section is non-empty:

1. Read the feedback. Classify each item: content change, or challenge to a recorded decision.
2. Content changes: edit the section in place.
3. Decision challenges: open that decision's council `plan.md`, put the feedback in its Feedback section, re-trigger council on it. Council rewrites the record in place with a History line. Update the citing section from the new record.
4. Append one Changelog line naming what moved. Clear the Feedback section.
5. Send the updated file.

Rounds are unlimited. The user stops by not re-triggering. If Feedback is empty, say so and stop; nothing to do.

## Output

1. `system-design.md` at the chosen path
2. `decisions/NNNN-<slug>.md` per council run, next to the document
3. A short report: sections tagged `inferred` or `missing`, decisions delegated, decisions inline, open questions
