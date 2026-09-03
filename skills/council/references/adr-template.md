# decision-record.md template

Written by the Chairman at Stage 6, every run, next to `plan.md`. MADR-style. It is the history projection of the run: what was on the table, why the rest lost, when to look again. `plan.md` is for acting this week; this file is for the person who reopens the question in a year.

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
```

Why every run: the cost is one template fill from files already on disk. Teams lose more to re-deriving old decisions than they save by skipping the record on small ones.
