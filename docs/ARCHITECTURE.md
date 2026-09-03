# Architecture

## Problem

Skills must be portable: one folder, copy it, it works. Artifacts want the opposite: shared components, one design language, a real build. Held naively these pull apart, either every artifact re-implements its UI or every skill drags a `node_modules` behind it.

## Resolution

Share at build time, ship flat.

```
packages/ui, packages/artifact-kit        shared source
          │  import
artifacts/<skill>-<artifact>/             one Vite app per artifact
          │  vite build (single-file plugin)
skills/<skill>/assets/<artifact>.html     one HTML, everything inlined, committed
```

The skill never knows the packages exist. A user who installs `council` gets `viewer.html`, not React. Two artifacts built from the same `Pill` component share look and behaviour without sharing a byte at runtime.

## Why commit built assets

Plugin install is a copy, not a build. If assets were gitignored, `claude plugin install` would deliver a skill with a hole in it. `pnpm check` rebuilds and diffs, so a stale asset fails CI and cannot merge.

## How this compares

| Approach | Used by | Trade-off |
|---|---|---|
| Flat `skills/<name>/SKILL.md`, marketplace.json at root | anthropics/skills, most community repos | Simple, portable, no shared UI. Artifacts, when present, are hand-written HTML per skill |
| One plugin per folder with `.claude-plugin/plugin.json`, marketplace lists them | anthropics/claude-code, claude-plugins-official | Good install story, still no build layer |
| This repo | — | Both of the above for `skills/`, plus a build layer that keeps artifacts consistent. Cost: a Node toolchain for contributors, none for users |

We keep the shipped shape identical to the first two rows so every existing install path works: marketplace add, plugin install, or plain folder copy.

## Constraints that shaped it

- Claude Code rejects component paths resolving outside the plugin root. So no `../packages` at runtime, ever.
- Runtime servers ship as Python stdlib. Node is not guaranteed where Claude Code runs; Python is.
- Artifacts get data through a JSON `<script>` slot, not through fetch to arbitrary hosts. The skill's own server fills the slot for static export and serves the same paths live.
- One artifact = one Vite app = one HTML. No multi-page artifacts. If a skill needs two views, it ships two files.

## Packages

- `@agent-skills/ui`: CSS tokens (`tokens.css`), theme handling, primitives (`Pill`, `Bubble`, `Toolbar`, `Select`, `Empty`, `CodeBlock`). React 19, no runtime CSS-in-JS.
- `@agent-skills/artifact-kit`: `useArtifactData` (static slot or live polling), `parseJsonl`, `readJsonSlot`, `formatTime`. No React dependency beyond the hook.
- `@agent-skills/vite-config`: `defineArtifact({ skill, name })` returning a Vite config with React, single-file output, target path `skills/<skill>/assets/<name>.html`, and a `publicDir` pointing at the artifact's `fixtures/` for dev.

## Versioning

Skills carry their own version in `.claude-plugin/plugin.json`. Packages are workspace-internal, unversioned, `workspace:*`. A skill's built asset is the only artefact users receive, so the skill version is the only one that matters.
