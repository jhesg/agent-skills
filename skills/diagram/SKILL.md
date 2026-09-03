---
name: diagram
description: Draw an Excalidraw diagram from a short declarative spec, with predictable layout and the shared design palette, then preview it. Use whenever a picture would carry information text cannot — architecture with three or more components, a flow with branches, a state machine, or two or more options compared side by side — and whenever the user says diagram, draw, sketch, architecture picture, flow chart, "show me how X connects", excalidraw, or asks to compare flows or decisions visually. Also use from other skills (spec, system-design, api-design, prd, council) when their rules call for a diagram. Do not use for lists, two-step flows, or anything a table conveys; say so and use the table.
---

# Diagram

Turn "what the picture should say" into an `.excalidraw` file, deterministically, and look at it before delivering. The file opens in excalidraw.com, the VS Code Excalidraw extension, and Obsidian, so humans can hand-edit it later. Nothing leaves the machine.

## Why a spec, not raw elements

Agents are good at deciding what a diagram means and bad at computing coordinates. Hand-placed Excalidraw JSON produces overlapping boxes and arrows that miss. `scripts/excalidraw.py` takes nodes, edges, groups, and a layout name, and does the geometry. Three layouts cover nearly every engineering picture; if one does not fit, the picture probably wants to be a table.

## Files

| File | Purpose |
|---|---|
| `scripts/excalidraw.py` | Spec JSON → `.excalidraw`. Stdlib Python. |
| `scripts/preview.py` | Serves `assets/viewer.html` with the diagram, live-reloads on file change, exports a standalone HTML |
| `assets/viewer.html` | Built viewer, renders the subset the generator emits, SVG export button |
| `references/spec-format.md` | Every spec field, with examples |
| `references/rules.md` | When to draw, when not to, and how to keep diagrams honest |

## Workflow

1. **Decide whether to draw.** Read `references/rules.md`. If the content fails the test there, do not draw; say why and use prose or a table. A diagram nobody needed costs attention every time the document is read.
2. **Write the spec.** One idea per diagram, 12 nodes or fewer, every non-obvious edge labelled. Tones carry meaning, so add a legend whenever more than one tone is used. Save as `<doc dir>/diagrams/<slug>.spec.json`; the spec is the editable source of truth for regeneration.
3. **Generate.**
   ```bash
   python3 <skill-dir>/scripts/excalidraw.py <slug>.spec.json <slug>.excalidraw
   ```
4. **Preview.** Start `preview.py` on the file and open it in the Browser pane if one is available; otherwise give the user the URL. Look at it. Check the reading order matches the story, labels are legible, nothing overlaps. Fix the spec, regenerate; the preview reloads.
   ```bash
   python3 <skill-dir>/scripts/preview.py <slug>.excalidraw --port 8770
   ```
5. **Export for the document.** `preview.py --svg <slug>.svg` writes an SVG next to the file. Markdown embeds the SVG; the `.excalidraw` sits beside it for editing. Never embed a diagram without also committing its spec.
   ```bash
   python3 <skill-dir>/scripts/preview.py <slug>.excalidraw --svg <slug>.svg
   ```
6. **Deliver.** Send the SVG (`SendUserFile`) and name the `.excalidraw` and spec paths. Say in one line what the diagram shows and what it deliberately leaves out.

## Layouts

| Layout | Use for | Geometry |
|---|---|---|
| `flow` | Pipelines, request paths, dependencies | Layered by longest path from sources. `direction` LR or TB |
| `columns` | Comparing options or flows side by side | One frame per group, each group laid out top to bottom, frames left to right |
| `grid` | Inventories with no meaningful edges | Square-ish grid |

## Tones

Same palette as every artifact in this family. Meaning is fixed so readers learn it once:

| Tone | Meaning |
|---|---|
| `1` | Chosen, primary, owned by us |
| `2` | Alternative, secondary, rejected option |
| `3` | External, derived, third party |
| `danger` | Failure path, risk, blocker |
| `muted` | Neutral, context |

## Working with other skills

Document skills call this one for architecture and comparison pictures; council may call it to compare options in a decision record. They pass the doc dir so files land in `<doc dir>/diagrams/`. If this skill is not installed, they fall back to Mermaid inline. Mermaid is fine for a simple linear flow that GitHub must render; use this skill when layout or side-by-side comparison matters.

## Limits, stated plainly

The viewer renders what the generator emits: rectangles, ellipses, diamonds, straight arrows, text, frames. A hand-edited file with freehand strokes or images still opens in Excalidraw proper but may not render fully here. Roughness is cosmetic and ignored in the preview. Fonts are system fonts; the file declares Helvetica so Excalidraw renders it consistently.
