---
name: api-design
description: Write or update an API or SDK design: resources and naming, operations, request and response schemas, error catalog, pagination, versioning and deprecation, auth and limits, examples. Use whenever the user says API design, REST or GraphQL or RPC contract, SDK surface, 'design the endpoints for X', public API, webhook payloads, or wants a contract agreed before implementation. Delegates genuinely contested contract decisions to the council skill and cites the decision records. Do not use for the internals behind the API (spec, system-design) or product requirements (prd).
---

# API design

Produce an API or SDK surface: resources, contracts, errors, versioning, examples. One file, `api-design.md`, that a team can review, challenge, and revise for as long as the question stays open. Decisions inside it that are genuinely contested go to the council skill; this skill owns the document, council owns the reasoning.

## Why this split

A document skill that argues its own hard calls ends up defending them. Sending contested decisions to an independent panel, and citing the record it produces, keeps this document honest and keeps the reasoning reusable when the question reopens. It also keeps this skill small: it knows what a good api design contains, not how to adjudicate every trade-off inside one.

## Files

| File | Purpose |
|---|---|
| `references/template.md` | Section list with guidance per section, plus Decision records, Changelog, Feedback |
| `references/review-checklist.md` | What to verify before delivering |
| `references/council-handoff.md` | How to send a decision to council and cite the result |

## Workflow

### 1. Intake

Read everything the user pointed at: their message, files, repo, existing docs. Fill the template. Tag every section `given` (from the user or sources), `inferred` (you derived it, say from what), or `missing`. Do not fill a `missing` section with invention; a confident-looking blank is worse than a visible gap.

If a section that decides the document's shape is `missing`, ask, at most 3 questions, then continue. For `api design` those are usually the first three sections of the template. Everything else can carry a proposed default in Open questions.

### 2. Find the contested decisions

Walk the draft and list every place where two or more credible options exist. For each, decide: contested or not.

Contested means all of: two or more credible options, hard to reverse or weeks of consequence, and either stakeholders disagree or the trade-off is not obvious from the constraints. Typical contested decisions in a api design:

- versioning scheme and breaking-change policy
- pagination style
- error format
- REST vs RPC vs GraphQL
- sync response vs async job with polling or webhook
- idempotency mechanism

Uncontested decisions you make inline, with a one-line reason, in the section where they apply. Contested ones go to council, at most 3 per draft unless the user asks for more. The rest become Open questions with a proposed default. Why the cap: each council run is several agent calls; a document with eight panels is a document nobody waits for.

### 3. Delegate to council

Follow `references/council-handoff.md`. In short: build a council brief with `PURPOSE: record`, `RECORD PATH: <doc dir>/decisions/NNNN-<slug>.md`, and `CONTEXT` naming this document and section. Run council. When the record exists, write the decision into the section as one sentence plus a link to the record. Do not restate the trade-offs; the record owns them.

If council is not installed, say so and ask the user to install it (`claude plugin install council@jhesg-agent-skills`). Do not run a mini-panel inline; one decision engine.

### 4. Draft

Write `api-design.md` from the template. Sections:

| Section | What goes there |
|---|---|
| Purpose and consumers | Who calls this, from where, how often, what they are trying to do. |
| Principles | Conventions this API follows, inherited from an existing API where one exists. Naming, casing, time formats, ids. |
| Resources | Nouns, relationships, ownership. One paragraph per resource. |
| Operations | Table: operation, method and path or RPC name, auth, idempotent, rate limit class, notes. |
| Schemas | Request and response per operation, with a realistic example each. Required vs optional explicit. |
| Errors | Catalog: code, HTTP status or equivalent, when, what the client should do. Every operation lists which it can return. |
| Pagination, filtering, sorting | One mechanism, applied everywhere it applies. |
| Versioning and deprecation | How versions are expressed, what counts as breaking, deprecation notice period, sunset process. |
| Auth and limits | Authn, authz model, rate limits, quotas, abuse controls. |
| SDK ergonomics | If an SDK ships: method shapes, retries, pagination helpers, error types. Skip when no SDK. |
| Examples | One happy path end to end, one error path end to end, as real requests and responses. |
| Compatibility | Effect on existing clients. Migration notes if any. |
| Alternatives considered | One line per alternative and why not. Contested ones link a decision record. |
| Open questions | Each with an owner and a proposed default. |
| Decision records | Table: decision, record path, status |
| Changelog | One line per round |
| Feedback | Empty, for the user |

Prose is for reasoning; tables are for anything with three or more parallel items. Keep the first section readable by someone who reads nothing else.

### 4b. Diagrams

Use the `diagram` skill when the picture carries structure text cannot: rarely. A sequence of three calls is prose. Draw only for async patterns with polling or webhooks where ordering matters. Files land in `<doc dir>/diagrams/` as spec, `.excalidraw`, and SVG; the document embeds the SVG with a one-line caption that links the `.excalidraw` for editing. Same palette as every artifact here, so tones mean the same thing across documents: 1 chosen, 2 alternative, 3 external, danger failure.

If `diagram` is not installed, use a Mermaid block inline for a simple flow and say a richer diagram was skipped. Never draw a list.

### 5. Review

Run `references/review-checklist.md` against the draft. Fix what fails. Anything you cannot fix goes to Open questions with an owner.

### 6. Deliver

Write the file where the user asked, or `docs/api-design/<slug>.md` by default. Send it (`SendUserFile` when available). Report which decisions went to council and which were made inline.

## Iteration

When invoked with a path to an existing `api-design.md` and its Feedback section is non-empty:

1. Read the feedback. Classify each item: content change, or challenge to a recorded decision.
2. Content changes: edit the section in place.
3. Decision challenges: open that decision's council `plan.md`, put the feedback in its Feedback section, re-trigger council on it. Council rewrites the record in place with a History line. Update the citing section from the new record.
4. Append one Changelog line naming what moved. Clear the Feedback section.
5. Send the updated file.

Rounds are unlimited. The user stops by not re-triggering. If Feedback is empty, say so and stop; nothing to do.

## Output

1. `api-design.md` at the chosen path
2. `decisions/NNNN-<slug>.md` per council run, next to the document
3. A short report: sections tagged `inferred` or `missing`, decisions delegated, decisions inline, open questions
