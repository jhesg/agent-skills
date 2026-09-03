# system-design.md template

Fill every section. Keep the HTML comments while drafting, they are the guidance; delete them before delivering. Tag sections `given | inferred | missing` in the intake pass and remove tags at delivery.

```markdown
# <Title>

- Status: draft | in review | agreed | superseded
- Owner: <name>
- Date: <ISO date>
- Round: <n>

## Context and scope
<!-- What system, what boundary, what is explicitly outside it. -->


## Requirements
<!-- Functional in bullets. Non-functional as numbers with how each is measured: latency percentiles, throughput, availability, durability, RPO/RTO. -->


## Constraints
<!-- Team, budget, hosting, compliance, deadlines, existing systems that cannot change. -->


## Architecture
<!-- Component list with one-line responsibility each, then a Mermaid diagram. Every arrow in the diagram appears in Data flow. -->


## Data flow
<!-- The main paths, step by step: request, write, read, async, failure. Which component owns each step. -->


## Storage and consistency
<!-- What is stored where, why that engine, consistency guarantees per path, retention. -->


## Capacity
<!-- Table: dimension, current, 12-month, assumption. Show the arithmetic, not just the result. -->


## Failure modes
<!-- Table: component, failure, blast radius, detection, mitigation, recovery. Include dependency outages. -->


## Security
<!-- Trust boundaries, authn/authz per boundary, secrets, data classification. -->


## Operations
<!-- Deploy, rollback, observe, on-call runbook pointers, cost line. -->


## Migration and rollout
<!-- How we get from today's system to this one without a stop-the-world. -->


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
<!-- Write here. Disagreements, missing constraints, decisions to re-test. Then re-trigger: /system-design <this file> -->
```
