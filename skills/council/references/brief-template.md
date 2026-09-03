# Brief template

Fill every field. Tag each `given` (user said it), `inferred` (you derived it, say from what), or `missing`. Keep the user's wording where possible; you are organising, not rewriting. Options keep the user's order.

```
PURPOSE: <decide | record>                                                    [given|inferred]
RECORD PATH: <where decision-record.md must be written, or "run dir">         [given|inferred]
DECISION: <one sentence, the choice to make>                                   [given|inferred|missing]
OPTIONS:
  A. <option>                                                                   [given|inferred]
  B. <option>                                                                   [given|inferred]
  (C. ...)
HARD CONSTRAINTS: <budget, legal, contractual, technical limits>               [given|inferred|missing]
DEADLINE: <date or "none stated">                                              [given|inferred|missing]
REVERSIBILITY: <one-way door | two-way door>, <cost to undo>                   [given|inferred|missing]
STAKEHOLDERS: <name — role — stake>, one per line                              [given|missing]
SUCCESS IN 6 MONTHS: <what the user says "good" looks like>                    [given|inferred|missing]
CONTEXT: <2–5 lines of the user's own situation, verbatim where possible>      [given]

ASSUMPTIONS (only if user chose to proceed with gaps):
  - <field>: <assumed value> — because <reason>
```

`RECORD PATH` lets a caller, usually a document skill such as spec or system-design, say where the living record belongs, typically `<doc dir>/decisions/NNNN-<slug>.md`. Default is the run dir. Stage 6 writes the record there and links it from plan.md.

`PURPOSE` is `record` when the user says the team needs an ADR, a decision record, or a written history of the choice. Otherwise `decide`. Record mode passes the guard on its own and turns on the Stage 1b augment round, because "what else did we consider" is a question a record must answer.

Why the tags matter: advisers read only this brief. If they cannot tell what the user actually said from what you guessed, an inferred fact becomes a hard input and the whole panel argues from your assumption. Tagged, they can challenge it, which is the Assumption Auditor's job.

Why no ranking: if the Chairman orders or frames options, the panel inherits a lean before it speaks. The Chairman judges at Stage 4, not Stage 0.

Stakeholders are `given` or `missing`, never inferred. The Executor names real people from this list. Inventing a "your manager" the user never mentioned produces a plan with fictional recipients.
