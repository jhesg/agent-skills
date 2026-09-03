# Artifact guidelines

An artifact is a single HTML file a skill opens for a human. It is built, not written. Follow these so every artifact in the repo feels like the same product.

## Shape

- One Vite app under `artifacts/<skill>-<artifact>/`. Use `defineArtifact` from `@agent-skills/vite-config`; do not hand-roll the config.
- Entry `index.html` + `src/main.tsx` + `src/App.tsx`. Keep `App` thin; put logic in hooks or `@agent-skills/artifact-kit`.
- Build output goes to `skills/<skill>/assets/<artifact>.html`. Commit it with the source change.

## Data in

Two modes, one code path:

```tsx
const { data, mode } = useArtifactData<MyData>({
  slotId: 'council-data',           // <script type="application/json" id="council-data">
  live: { url: '/log/events.jsonl', intervalMs: 2000 },
});
```

- Static: the skill's server fills the slot and the page reads it once. Export mode.
- Live: the slot is empty, the page polls the skill's local server. Watch mode.

Never fetch anything except relative paths on the same origin. Artifacts run from `file://` or from the skill's `127.0.0.1` server. No CDNs, no fonts from Google, no analytics. If it is not in the bundle, it does not exist.

## Fixtures

`fixtures/` in the artifact folder mirrors the runtime directory the skill produces. Vite serves it in dev, so `pnpm dev <artifact>` shows real-looking data with no skill run. Keep fixtures small and honest: they are the artifact's test.

## UI

- Import tokens once in `main.tsx`: `import '@agent-skills/ui/tokens.css'`.
- Use primitives before writing new markup. When a second artifact needs a new primitive, move it into `@agent-skills/ui`.
- Both themes, via `prefers-color-scheme`. Never a colour literal outside `tokens.css`.
- System font stack. No webfonts.
- Filters and controls in a sticky `Toolbar`. Content in a single column, max width from tokens.
- Empty and loading states are designed, not accidental. Use `Empty`.

## Size

Target under 300 KB built. React 19 + primitives lands around 150 KB. If an artifact needs a heavy library, ask whether the skill's Python script can do the work and hand the page plain JSON instead.

## Accessibility baseline

Real `<select>`, `<button>`, `<details>` elements. Labels on controls. Focus visible. Contrast from tokens, already checked.

## Checklist before commit

- [ ] `pnpm dev <artifact>` renders with fixtures, both themes
- [ ] `pnpm build` output opens from `file://` with the slot filled
- [ ] No network requests except relative ones
- [ ] `pnpm check` green
