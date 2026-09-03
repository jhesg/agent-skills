# Rules for drawing

A diagram is a claim about structure. Draw when the structure is the point; do not draw when it is decoration.

## Draw when

- Three or more components with relationships that are not a straight line
- A flow with branches, retries, or failure paths
- A state machine with four or more states
- Two or more options whose shapes differ, compared side by side
- Trust boundaries or ownership boundaries that the prose keeps having to restate

## Do not draw when

- A list would do. Five boxes in a row is a list.
- Two steps. "A calls B" is a sentence.
- The relationships are already a table: component, owner, failure mode.
- You would have to invent structure to fill the picture. If the spec has no edges, stop.

## Keep it honest

- One idea per diagram. A second idea is a second diagram.
- Twelve nodes or fewer. Past that, split by boundary or zoom level.
- Label every edge that a reader could misread. Unlabelled edges mean "calls" or "flows to"; anything else gets a label.
- Tones mean something (see SKILL.md). Never use a tone for looks. Add a legend when more than one tone appears.
- Comparison diagrams show the same level of detail per option. A rich chosen option next to a two-box rejected option is a rigged picture.
- Failure paths are dashed and `danger`. If a component can fail and the picture does not show it, say so in the caption.
- The caption states what the diagram leaves out. Every diagram leaves something out.

## In documents

- Spec, `.excalidraw`, and SVG live in `<doc dir>/diagrams/`. Commit all three. The spec is the source; the other two are builds.
- Markdown embeds the SVG with a caption line under it. The caption links the `.excalidraw` for editing.
- One architecture diagram per system-design document is expected. Spec documents draw only when the feature introduces new components or a branching flow. API and PRD documents rarely draw; a sequence of three calls is prose.
- Council records draw only when three or more options have visibly different shapes. Two options with the same shape are a table of trade-offs, which the record already has.

## Mermaid instead

Use Mermaid inline when all of these hold: the flow is linear or a simple tree, the document is read on GitHub where Mermaid renders natively, and no side-by-side comparison is needed. Never produce both for the same picture.
