# api-design.md template

Fill every section. Keep the HTML comments while drafting, they are the guidance; delete them before delivering. Tag sections `given | inferred | missing` in the intake pass and remove tags at delivery.

```markdown
# <Title>

- Status: draft | in review | agreed | superseded
- Owner: <name>
- Date: <ISO date>
- Round: <n>

## Purpose and consumers
<!-- Who calls this, from where, how often, what they are trying to do. -->


## Principles
<!-- Conventions this API follows, inherited from an existing API where one exists. Naming, casing, time formats, ids. -->


## Resources
<!-- Nouns, relationships, ownership. One paragraph per resource. -->


## Operations
<!-- Table: operation, method and path or RPC name, auth, idempotent, rate limit class, notes. -->


## Schemas
<!-- Request and response per operation, with a realistic example each. Required vs optional explicit. -->


## Errors
<!-- Catalog: code, HTTP status or equivalent, when, what the client should do. Every operation lists which it can return. -->


## Pagination, filtering, sorting
<!-- One mechanism, applied everywhere it applies. -->


## Versioning and deprecation
<!-- How versions are expressed, what counts as breaking, deprecation notice period, sunset process. -->


## Auth and limits
<!-- Authn, authz model, rate limits, quotas, abuse controls. -->


## SDK ergonomics
<!-- If an SDK ships: method shapes, retries, pagination helpers, error types. Skip when no SDK. -->


## Examples
<!-- One happy path end to end, one error path end to end, as real requests and responses. -->


## Compatibility
<!-- Effect on existing clients. Migration notes if any. -->


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
<!-- Write here. Disagreements, missing constraints, decisions to re-test. Then re-trigger: /api-design <this file> -->
```
