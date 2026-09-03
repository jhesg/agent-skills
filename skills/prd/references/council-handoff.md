# Council handoff

How this skill sends a contested decision to the council skill and consumes the result. Council is a separate skill; it must be installed. This file does not duplicate its logic.

## Send

1. Choose the record path: `<doc dir>/decisions/NNNN-<slug>.md`, NNNN zero-padded, next free number.
2. Build a brief in council's shape (`skills/council/references/brief-template.md` in the agent-skills repo, or the installed plugin's copy). Required fields:

```
PURPOSE: record
RECORD PATH: <doc dir>/decisions/NNNN-<slug>.md
DECISION: <one sentence, the choice this section must make>
OPTIONS: <the credible options you found, or "to be proposed">
HARD CONSTRAINTS: <from the document's constraints section>
DEADLINE: <from the document, or none stated>
REVERSIBILITY: <per option>
STAKEHOLDERS: <from the document's owner and reviewers>
SUCCESS IN 6 MONTHS: <from the document's goals>
CONTEXT: This decision belongs to <document path>, section "<section>". <2–4 lines of the section's current state>
```

3. Invoke council with that brief. Prefer the Skill tool (`council`) when available; otherwise follow the installed plugin's SKILL.md as the Chairman yourself. Council opens its viewer, runs, and writes the record at RECORD PATH plus a `plan.md` in its run dir.

## Consume

1. Read the record's `Decision outcome`. Write one sentence in the document section: the decision and its deciding reason, then `See decisions/NNNN-<slug>.md`.
2. Add a row to the document's Decision records table with status from the record.
3. Do not copy pros and cons into the document. If a reviewer wants them, the link is right there.

## Re-open

When feedback challenges a recorded decision: open the council `plan.md` for that record (its path is in the record's History), write the feedback into its Feedback section, re-trigger council with that plan path. Council rewrites the record in place and appends History. Then update the citing sentence and the table row.

## If council is missing

Say: "This decision is contested and should go to the council skill, which is not installed. Install with `claude plugin install council@jhesg-agent-skills`, or tell me to decide inline and I will mark it as an inline decision with lower confidence." Never run a panel inside this skill.
