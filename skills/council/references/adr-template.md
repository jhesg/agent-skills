# decision-record.md template

Written by the Chairman at Stage 6, every run. MADR-style. It is the history projection: what was on the table, why the rest lost, when to look again. `plan.md` is for acting this week; this file is for the person who reopens the question in a year.

It is a living document. Round 1 creates it in the run dir. Every later round updates the same file in place, wherever the user has moved it, and appends to `## History`. One record per decision, however many rounds. The user stops iterating by not re-triggering; there is no round limit.

Fill from run files only. Do not add reasoning that did not happen in the run; if a section has nothing, write "not raised by the panel". A record that invents tidy justifications after the fact is worse than a thin one.

```markdown
# <Decision title, imperative, e.g. "Use pg-boss for the job queue">

- Status: proposed | accepted | superseded by <link>
- Date: <ISO date>
- Round: <n>, previous: <path or none>
- Deciders: <stakeholders from brief marked as deciding>
- Council run: <run dir>, transcript: <run>/transcript.html

## Context and problem statement
<brief CONTEXT and DECISION, verbatim where possible>

## Decision drivers
<HARD CONSTRAINTS, SUCCESS IN 6 MONTHS, deadline. One bullet each>

## Considered options
<every option in the frozen brief, including ones added in Stage 1b, tagged given | proposed>

## Decision outcome
Chosen: <VERDICT line>
Because: <DECIDING POINT, quoted>

### Rejected options
<one bullet per non-chosen option: REJECTED line from the verdict>

### Consequences
- Good: <from Expansionist take and verdict>
- Bad: <BIGGEST RISK, other Contrarian items tagged high>
- Watch: <LEADING INDICATOR>

## Options at a glance
<!-- Only when three or more options have visibly different shapes. Use the diagram skill, columns layout, one frame per option, same detail per option, tones: 1 chosen, 2 rejected, danger risk. Embed the SVG from <record dir>/diagrams/, caption links the .excalidraw. Two options with the same shape: delete this section, the table below is the comparison. If diagram is not installed, delete this section. -->

## Pros and cons of the options
### <Option>
- Good: <from Stage 2 takes and Stage 3 reviews>
- Bad: <same>
- Panel score: evidence <n>, actionability <n>
(repeat per option)

## Assumptions carried
<ASSUMPTIONS block from brief, plus Assumption Auditor's two flagged items>

## Revisit when
<KILL CRITERIA, plus any date-bound facts the verdict depended on>

## History
- Round 1, <date>: created. Verdict: <one line>. Run: <run dir>
- Round 2, <date>: feedback "<quoted gist>". Changed: <what moved: option added, verdict flipped, assumption corrected>. Verdict: <one line>. Run: <run dir>
```

On an update round, rewrite every section from the new run, keep the History intact, add one line. If the verdict changed, set the old one's status line to `superseded` inside the History entry, not by deleting it. Someone reading the record should be able to see the decision move.

Why every run: the cost is one template fill from files already on disk. Teams lose more to re-deriving old decisions than they save by skipping the record on small ones.
