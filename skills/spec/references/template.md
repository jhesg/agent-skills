# spec.md template

Fill every section. Keep the HTML comments while drafting, they are the guidance; delete them before delivering. Tag sections `given | inferred | missing` in the intake pass and remove tags at delivery.

```markdown
# <Title>

- Status: draft | in review | agreed | superseded
- Owner: <name>
- Date: <ISO date>
- Round: <n>

## Summary
<!-- Three sentences: what changes, for whom, why now. -->


## Problem and goals
<!-- The user-visible or operational problem. Goals as outcomes, measurable where possible. -->


## Non-goals
<!-- What this spec deliberately leaves out, so reviewers stop asking. -->


## Current state
<!-- How it works today. Link code, tables, endpoints. Numbers where they matter: volumes, latencies, error rates. -->


## Proposed design
<!-- Behaviour first, then data model, then interfaces. State machines and edge cases explicit. UI states if any: loading, empty, error, success. -->


## Alternatives considered
<!-- One line per alternative and why not. Contested ones link a decision record instead of restating it. -->


## Rollout
<!-- Flags, migrations, backfills, ordering, and the reversible step at each stage. What 'done' looks like. -->


## Observability
<!-- Metrics, logs, alerts added or changed. What tells us it works, what tells us it broke. -->


## Testing
<!-- Unit, integration, E2E. Name identifiers external suites depend on (routes, test ids, flag keys) and whether they change. -->


## Security and privacy
<!-- New data, new access paths, PII handling. 'None' is acceptable when true. -->


## Open questions
<!-- Each with an owner and a proposed default so work can start. -->


## Decision records
| Decision | Record | Status |
|---|---|---|
| <one line> | decisions/NNNN-<slug>.md | proposed / accepted / superseded |

## Decisions made inline
- <decision>: <one-line reason>

## Changelog
- Round 1, <date>: created.

## Feedback
<!-- Write here. Disagreements, missing constraints, decisions to re-test. Then re-trigger: /spec <this file> -->
```
