# prd.md template

Fill every section. Keep the HTML comments while drafting, they are the guidance; delete them before delivering. Tag sections `given | inferred | missing` in the intake pass and remove tags at delivery.

```markdown
# <Title>

- Status: draft | in review | agreed | superseded
- Owner: <name>
- Date: <ISO date>
- Round: <n>

## Problem statement
<!-- One paragraph. Who hurts, how, how often. No solution language. -->


## Evidence
<!-- Data, quotes, tickets, support volume, competitor moves. Each with a source. Assertions without a source are marked as such. -->


## Users and jobs
<!-- Segments and the job each is trying to get done. Primary segment for v1 named. -->


## Goals and metrics
<!-- Table: goal, metric, baseline, target, measurement window. One primary metric. -->


## Non-goals
<!-- What we will not do in this version, and why, so it stops coming back. -->


## Scope
<!-- Must, should, won't for this version. Every must traces to a goal. -->


## User stories and flows
<!-- As-a / I-want / so-that, grouped by segment. Key flows in steps or a Mermaid diagram. -->


## Requirements
<!-- Functional requirements, each tagged with the story it serves and must/should. Non-functional where the product cares: speed, accessibility, locales. -->


## UX notes
<!-- Constraints and references for design. Not the design. -->


## Dependencies and risks
<!-- Teams, systems, legal, data. Risk, likelihood, mitigation. -->


## Launch and measurement
<!-- Rollout shape, audience, kill criteria, when we read the metric and what we do at each outcome. -->


## Alternatives considered
<!-- One line per alternative and why not. Contested ones link a decision record. -->


## Open questions
<!-- Each with an owner and a proposed default. -->


## Decision records
| Decision | Record | Status |
|---|---|---|
| <one line> | decisions/NNNN-<slug>.md | proposed / accepted / superseded |

## Decisions made inline
- <decision>: <one-line reason>

## Changelog
- Round 1, <date>: created.

## Feedback
<!-- Write here. Disagreements, missing constraints, decisions to re-test. Then re-trigger: /prd <this file> -->
```
