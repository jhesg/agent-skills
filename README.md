# agent-skills

Monorepo for agent skills and the artifacts that power them.

Two halves, one rule between them:

- `skills/` is what ships. Every folder is a complete skill: `SKILL.md`, references, scripts, and built artifacts. Copy one folder, or install it as a plugin, and it works. Nothing in it points outside itself.
- Everything else (`packages/`, `artifacts/`) is how the shipped artifacts get made. Shared React primitives, design tokens, runtime helpers, and one Vite app per artifact. Builds emit a single dependency-free HTML file into the owning skill's `assets/`.

Install one skill:

```bash
claude plugin marketplace add jhesg/agent-skills
claude plugin install council@jhesg-agent-skills
```

Or copy `skills/<name>/` anywhere Claude looks for skills.

## Skills

| Skill | What it does | Artifact |
|---|---|---|
| [council](skills/council) | Five-adviser decision council with independent subagents, blind review, verdict, plan.md, living decision record | live transcript viewer |
| [diagram](skills/diagram) | Excalidraw diagrams from a declarative spec, deterministic layout, shared palette | diagram preview + SVG export |
| [spec](skills/spec) | Technical spec for one feature; contested decisions go to council | — |
| [system-design](skills/system-design) | System design: components, flow, capacity, failure modes | — |
| [api-design](skills/api-design) | API or SDK surface: resources, contracts, errors, versioning | — |
| [prd](skills/prd) | Product requirements: problem, users, goals, scope, launch | — |

## Layout

```
skills/<name>/            shipped, self-contained, built assets committed
artifacts/<name>/         Vite + React source for one skill's artifact
packages/ui/              @agent-skills/ui        design tokens + primitives
packages/artifact-kit/    @agent-skills/artifact-kit  runtime helpers (live/static data, jsonl, urls)
packages/vite-config/     @agent-skills/vite-config   single-file build preset
docs/                     architecture, guidelines, design system
scripts/                  validate, package, scaffold
```

## Develop

```bash
pnpm install
pnpm dev council-transcript      # vite dev server for one artifact, fixture data
pnpm build                       # all artifacts → skills/*/assets/*.html
pnpm check                       # validate + typecheck + build + assets up to date
pnpm package council             # dist/council.skill
pnpm new-skill <name>            # scaffold skill + artifact
```

Built assets are committed. `pnpm check` fails if a build changes them, so `skills/` never drifts from source.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for why it is shaped this way and [docs/ROADMAP.md](docs/ROADMAP.md) for the document skills that will consume council decisions.
