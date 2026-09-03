# Roadmap: document skills around council

Council decides. It does not author design documents. These skills will, and each one calls council for the decisions inside it that are genuinely contested, then cites the resulting `decision-record.md`.

## Contract between council and document skills

- **Input to council** from a document skill: a brief in `skills/council/references/brief-template.md` shape, with `PURPOSE: record`, and a `CONTEXT` that names the document and section the decision belongs to.
- **Output from council**: `decision-record.md` at a path the document skill chooses (usually next to the document, `decisions/NNNN-<slug>.md`), plus `plan.md` in the run dir.
- **Citation**: the document links the record where the decision is applied. It does not restate the trade-offs; the record owns them.
- **Iteration**: the document skill re-triggers council with feedback on the plan when a decision is challenged. Council rewrites the record in place and appends History. The document skill re-reads the record and updates the affected section. Unlimited rounds; the human stops.
- **Artifacts**: each document skill may ship its own artifact built from `@agent-skills/ui`. Same tokens, same primitives, no runtime coupling. A document viewer that renders the linked decision records inline is the obvious shared candidate for `@agent-skills/artifact-kit` once two skills need it.

## Planned skills

| Skill | Produces | Council decisions it typically delegates | Status |
|---|---|---|---|
| `prd` | Product requirements: problem, users, scope, success metrics, non-goals | Scope cuts, metric choice, build vs buy | v0.2.0, untested |
| `spec` | Technical spec for one feature: behaviour, data, interfaces, rollout, testing | Data model shape, rollout strategy, migration approach | v0.2.0, untested |
| `api-design` | API or SDK surface: resources, contracts, versioning, errors, examples | Versioning scheme, pagination style, breaking-change policy | v0.2.0, untested |
| `system-design` | Components, data flow, capacity, failure modes, operations | Sync vs async, storage engine, consistency model, hosting | v0.2.0, untested |

## Diagrams

`diagram` is a shared utility skill: spec JSON → `.excalidraw` via stdlib Python, deterministic layout, palette from `@agent-skills/ui`, local preview artifact, SVG export. Document skills and council call it under the rules in `skills/diagram/references/rules.md`. It is our own implementation: the official Excalidraw package is 46 MB unpacked and loads fonts from a CDN, which our artifacts cannot do, and the popular third-party skill ships no licence. The viewer renders only the subset the generator emits; the `.excalidraw` file itself opens anywhere Excalidraw does.

## Order

`spec` first. It is the most common document, it exercises the contract end to end, and the council run from the frontend LCP problem is a ready-made test. `system-design` second, it reuses the notification-redesign test. `api-design` and `prd` after, once two skills have shown which parts of the contract want a shared package.

## Non-goals

- Council will not grow document-shaped outputs beyond `plan.md` and `decision-record.md`.
- Document skills will not run their own mini-councils. One decision engine.
- No skill depends on another at runtime. A document skill that finds council missing says so and asks the user to install it; it does not inline a copy.
