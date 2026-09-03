# Working in this repo

Read this before touching anything. It is short on purpose.

## The one invariant

A skill folder under `skills/` must work when copied alone. No relative path leaves it. No runtime dependency is installed. Its artifacts are single HTML files with everything inlined. If a change breaks that, the change is wrong, however elegant.

Why: Claude Code rejects plugin component paths that resolve outside the plugin root, and users install skills one at a time. Sharing happens at build time, in `packages/`, never at runtime.

## Adding a skill

1. `pnpm new-skill <name>` scaffolds `skills/<name>/` and `artifacts/<name>-*/` and adds a marketplace entry.
2. Write `SKILL.md` following `docs/SKILL_GUIDELINES.md`. Explain why, not just what; the model reading it is smart.
3. Build the artifact from `@agent-skills/ui` and `@agent-skills/artifact-kit`. Add to those packages when two artifacts need the same thing; keep it local when one does.
4. `pnpm check` must pass. It builds and diffs `skills/` so committed assets match source.
5. Commit the built asset with the source change. One commit, reviewable together.

## Artifacts

Read `docs/ARTIFACT_GUIDELINES.md` and `docs/DESIGN_SYSTEM.md`. Summary: tokens from `@agent-skills/ui`, no external CDN, no fetch to anything but the local server the skill starts, light and dark from `prefers-color-scheme`, data enters through a `<script type="application/json" id="<name>-data">` slot that the skill's server fills for static export.

## Runtime servers

Skills that need a server at runtime ship a Python stdlib script in `scripts/`. Python is on every machine Claude Code runs on; Node is not guaranteed. Vite is a build tool here, never a runtime.

## Git

- Conventional commits, imperative mood: `feat(council): ...`, `chore(repo): ...`, `docs: ...`
- Trailer on every commit: `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`
- Push after each coherent stage so any stage can be reverted alone.
- `pnpm check` before every push.

## Don'ts

- Don't import between artifacts. Promote to a package instead.
- Don't add a dependency to a shipped skill. Build it in.
- Don't hand-edit `skills/*/assets/*.html`. Edit the artifact source and rebuild.
- Don't write `.claude/agents/` definitions for a skill. Charters live in the skill's `references/` so they travel with it.
