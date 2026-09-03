# Design system

Small on purpose. Artifacts are reading surfaces for humans supervising agents: logs, transcripts, plans, diffs. Calm, dense, legible. Not a marketing site.

## Tokens (`@agent-skills/ui/tokens.css`)

| Token | Light | Dark | Use |
|---|---|---|---|
| `--as-bg` | `#f6f5f2` | `#161513` | page |
| `--as-panel` | `#ffffff` | `#1f1e1b` | toolbar, code blocks |
| `--as-ink` | `#1c1b19` | `#ece9e2` | text |
| `--as-muted` | `#6b6862` | `#9a968d` | secondary text, labels |
| `--as-line` | `#e3e0da` | `#33312c` | borders |
| `--as-pill` | `#eeece7` | `#2a2925` | chips |
| `--as-accent-1` | `#2f5d8a` | `#7fb0e0` | primary actor (e.g. chairman) |
| `--as-accent-2` | `#7a4b1f` | `#d9a066` | secondary actors (e.g. advisers) |
| `--as-accent-3` | `#4f6b3a` | `#9dc47f` | derived / system |
| `--as-danger` | `#9b2c2c` | `#e08a8a` | errors, failed checks |

Spacing: `--as-s1` 4px, `--as-s2` 8px, `--as-s3` 12px, `--as-s4` 16px, `--as-s6` 24px. Radius: `--as-r1` 6px, `--as-r2` 8px, `--as-rpill` 999px. Content width: `--as-content` 920px.

Type: `--as-font` system-ui stack, 14px/1.45. `--as-mono` ui-monospace stack, 13px/1.45. Headings are weight 600, never larger than 15px in toolbars.

## Primitives (`@agent-skills/ui`)

| Component | Purpose |
|---|---|
| `Toolbar` | Sticky header: title, controls, status slot |
| `Select` | Labelled native select |
| `Toggle` | Labelled checkbox |
| `Pill` | Small metadata chip |
| `Bubble` | Chat-style row: actor column + body. `tone` picks accent |
| `CodeBlock` | Pre-wrapped monospace, scroll-capped |
| `Disclosure` | `<details>` with muted summary |
| `Empty` | Centered muted message |
| `Status` | Right-aligned muted status text with bold count |

Primitives take `className` and spread rest props. No variants beyond `tone`. If you need more, you probably need a new primitive, not an option.

## Language

- Actor names lower-case as they appear in logs. Do not title-case them.
- Timestamps as local time, `HH:MM:SS`. Dates only when the span crosses a day.
- Labels are nouns: "Channel", "Stage". Buttons are verbs.
- Empty state text says what would fill it: "Waiting for log/events.jsonl…", not "No data".
