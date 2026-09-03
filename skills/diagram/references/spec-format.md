# Spec format

JSON. Every field except `nodes` is optional.

```json
{
  "title": "Heading drawn at the top",
  "layout": "flow",              // flow | columns | grid
  "direction": "LR",             // flow only: LR | TB
  "nodes": [
    {
      "id": "api",               // unique, used by edges
      "label": "API handler",    // one or two words per line, \n allowed
      "note": "small text",      // optional second line, smaller
      "shape": "rect",           // rect | ellipse | diamond
      "tone": "1",               // 1 | 2 | 3 | danger | muted
      "group": "A"               // columns layout: which frame
    }
  ],
  "edges": [
    { "from": "api", "to": "pg", "label": "insert", "style": "solid", "tone": "muted" }
  ],
  "groups": [
    { "id": "A", "label": "Option A: outbox + worker" }
  ],
  "legend": [
    { "tone": "1", "label": "owned" }
  ]
}
```

## Conventions

- Shapes: `rect` for components and steps, `ellipse` for external systems and actors, `diamond` for decisions and failure sinks.
- `style: "dashed"` for failure paths, async hops, and optional edges. Pair with `tone: "danger"` for failures.
- In `columns`, edges across groups are drawn but discouraged; comparisons read better when each column is self-contained.
- Node width is fixed. Keep labels under 18 characters per line; use `\n` to wrap.

## Example: flow

See `fixtures/spec-flow.json` in the artifact source, or the SKILL.md workflow. Six nodes, five edges, one failure path, legend with three tones.

## Example: comparison

See `fixtures/spec-columns.json`. Three groups, three nodes each, same detail level per option, tones mark chosen, rejected, and risk.
