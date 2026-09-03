---
name: council
description: Convene a five-adviser decision council with independent subagents, structured brief, blind cross-review, a Chairman verdict, and a group-chat transcript humans can watch live. Use whenever the user is stuck between two or more real options with consequences that last weeks or are hard to reverse — phrases like "should I", "A or B", "can't decide", "torn between", "help me think through this decision", or any explicit ask for a panel, council, devil's advocate, or multiple perspectives. Also trigger for career moves, hiring/firing, pricing, architecture choices, product bets, and vendor picks when the user is weighing options rather than asking a fact. Do not trigger for factual questions with one answer, decisions reversible in a day, or when the user already decided and only wants a plan.
---

# Council

Five advisers, each in its own subagent context, answer a curated brief, score each other blind, and a Chairman (you, the main session) issues one verdict. All content moves through files in a run directory; messages between agents are one-line pointers. That gives an append-only log, a live transcript viewer, and a replayable run. Portable: every prompt and script lives in this folder.

## Roles

| Role | You? | File |
|---|---|---|
| Chairman | Yes, main session | this file |
| Contrarian | subagent | `references/advisers/contrarian.md` |
| First-Principles | subagent | `references/advisers/first-principles.md` |
| Expansionist | subagent | `references/advisers/expansionist.md` |
| Assumption Auditor | subagent | `references/advisers/assumption-auditor.md` |
| Executor | subagent | `references/advisers/executor.md` |

Also: `references/brief-template.md`, `references/stage-messages.md`, `references/plan-template.md`, `references/adr-template.md`, `scripts/serve_log.py`, `assets/viewer.html`.

The Chairman never writes adviser content. You route, strip labels, log, aggregate, decide. If you catch yourself arguing a side before Stage 4, stop: that is the panel's job.

## Why this shape

The naive version runs all five voices in one context and "anonymizes" them for peer review. That review is theater, the model knows what it wrote. Separate subagents fix it structurally. Word caps keep sprawl down so the verdict rests on sharp inputs. The Executor plans after the verdict because a week plan for an undecided question is fiction. Files instead of message bodies cost about the same tokens for advisers, save Chairman output tokens on review packets, and buy the audit trail and viewer for free.

## Run directory

Create one per run. Use the scratchpad if your system prompt lists one, else `./.council-run/<timestamp>/`. Absolute path, you will hand it to agents.

```
<run>/
  brief.md
  inbox/<role>/        Chairman writes, adviser reads      (stage2-task.md, stage3-packet.md, stage5-verdict.md)
  outbox/<role>/       adviser writes, Chairman reads      (stage2.md, stage3.md, stage5.md)
  log/events.jsonl     Chairman only, append-only
  log/stage3-mapping.json  Chairman only
  verdict.md
```

Roles as directory names: `contrarian`, `first-principles`, `expansionist`, `assumption-auditor`, `executor`.

Why the split: advisers get Read and Write tools to use the bus. Anything they can read, they could use to de-anonymize Stage 3. Role names live only in `log/` and in directory names; packets carry A–D labels only; charters tell advisers to open only paths named in their messages. Not enforceable, but reliable. Describe the guarantee as "independent contexts, labels stripped", never "anonymous".

## Log protocol

Append one JSON line to `log/events.jsonl` on every send and every receipt. Advisers never write the log, and their outbox holds only the requested output, no drafts or scratch notes. The log records what crossed between agents, nothing else. A human watching should see a conversation, not anyone's inner monologue; inconclusive reasoning has no use to them and buries the exchanges that do.

```json
{"ts":"<ISO-8601 UTC>","stage":<0-5>,"from":"chairman","to":"contrarian","type":"pointer","text":"Review packet ready","ref":"inbox/contrarian/stage3-packet.md"}
{"ts":"...","stage":3,"from":"contrarian","to":"chairman","type":"pointer","text":"Review done","ref":"outbox/contrarian/stage3.md"}
```

`type` is one of `brief`, `pointer`, `verdict`, `plan`, `note`. `ref` is relative to the run dir. Use `note` for guard exits, clarifications, length corrections, anything a human replaying the run would want to see. The viewer renders each line as a chat bubble with the referenced file inline, and joins `stage3-mapping.json` to reviews so humans see adviser-to-adviser exchanges the agents themselves could not.

## Viewer

First action of every run, before the brief: create the run dir, start the viewer, put it in front of the user. They should see the log fill from the first line.

```bash
python3 <skill-dir>/scripts/serve_log.py <run> --port 8765
```

Run it in the background. Open `http://127.0.0.1:8765/` in the Browser pane if one is available (`preview_start` with the URL), otherwise give the user the URL. Channels: All, Chairman ↔ each adviser, adviser ↔ adviser (derived from Stage 3), plus a stage filter. After Stage 5, export a standalone copy:

```bash
python3 <skill-dir>/scripts/serve_log.py <run> --static <run>/transcript.html
```

Send `transcript.html` to the user. Stdlib only, no install.

## Stage 0: Brief and trigger guard

Viewer is already up (see above). If the input is a `plan.md` path, follow the re-trigger procedure in `references/plan-template.md` to rebuild the brief, then continue here.

Read the user's input as the product owner would: you bridge customer and team. Fill `references/brief-template.md`, tag each field `given`, `inferred`, or `missing`. Do not fill gaps with your own answers, only with the user's words or a labeled inference.

Run the guard, even on explicit `/council` invocation:

| Check | Fails when |
|---|---|
| Real decision | One option and the user is not asking for alternatives. Zero or one option is fine when the user asks the council to propose them; mark `OPTIONS: to be proposed` and run Stage 1b |
| Reversibility | Trivially undone in a day or less |
| Stakes | No consequence beyond the week and none inferable |

One condition passes the guard regardless of the table: the user says the team needs an ADR, a decision record, or a written history of the choice. Set `PURPOSE: record`, log a `note` saying the council convened for record value, and continue. A trivial decision with a record requirement is still worth the panel, because the deliverable is the reasoning, not the pick.

If any check fails and no record need is stated, do not spawn agents. Log a `note` and say plainly:

> Council not convened. Reason: [failed check, one line]. Full panel cost is not justified by this input. Here is [direct answer / Executor-style plan] instead. Say "convene anyway" to override.

Never downgrade silently. "Convene anyway" always wins.

If checks pass but fields are `missing`, ask at most 3 questions and wait. If the user says proceed, move `missing` and `inferred` fields into an `ASSUMPTIONS` block at the top. Write `brief.md`, log `type: brief`, show it to the user before spawning. Options keep the user's order, no ranking, no opinion.

## Stage 1: Spawn the panel

For each role: write `inbox/<role>/stage2-task.md` containing the brief verbatim plus the Stage 2 task line from `references/stage-messages.md`. If options are still to be proposed, skip that file for now and prepare Stage 1b packets instead. Log a pointer. Then spawn five subagents in one turn, `run_in_background: true`, prompt:

```
<adviser charter file content, verbatim>

---
RUN DIRECTORY: <absolute run path>
YOUR ROLE ID: <role>
Read inbox/<role>/<first task file> and do what it says.
```

The first task file is `stage2-task.md`, or `stage1b-propose.md` for the three proposers when options are to be discovered. Advisers not involved in Stage 1b are spawned later, at Stage 2, so they never see the proposal round.

Record each agent's ID/name. Stages 3 and 5 continue these same agents with `SendMessage`; a fresh `Agent` call would lose context and break the design. If an agent is lost, respawn it and replay its inbox from files.

## Stage 1b: Option discovery (when `OPTIONS: to be proposed`, or `PURPOSE: record`)

Runs after spawning, before Stage 2. Two modes, same packet: **discover** when no options exist, **augment** when options exist but the purpose is record, so the record can answer "what else did we consider". In augment mode proposers see the given options and must propose outside them. Three advisers propose, each from their own lens, so the option set is not one person's framing:

| Adviser | Asked for |
|---|---|
| First-Principles | options that fall out of the problem once the current framing is stripped |
| Expansionist | the option with the largest upside if it works |
| Executor | the cheapest option to start and the cheapest to stop |

Write `inbox/<role>/stage1b-propose.md` from the Stage 1b template for those three, send pointers, log. Each returns up to 2 options: name, one line, first irreversible step, cost to undo, 120 words total. The other two advisers idle; they judge options, they do not author them, so their later critique stays independent.

Consolidate: merge duplicates, keep at most 4, write them into the brief as `OPTIONS:` tagged `proposed`, in the order received, no ranking. Fill `REVERSIBILITY` per option from the proposals. Log a `note` naming which adviser proposed what; the brief itself carries no attribution, so the panel argues the option, not the author. Show the updated brief to the user. They may edit, drop, or add. Freeze, then continue to Stage 2 with the frozen brief written to every inbox `stage2-task.md`.

Why the user sees it before Stage 2: options are the frame. If the council debates a set the user would never accept, everything after is wasted.

## Stage 2: Author

Wait for all five. Each replies with one line, `done: outbox/<role>/stage2.md`. Log each receipt. Check word count only, not merit. Over 150: send the length correction, log a `note`.

## Stage 3: Blind cross-review

For each adviser, write `inbox/<role>/stage3-packet.md` from the Stage 3 template: the other four takes, shuffled, labeled A–D. Record the mapping in `log/stage3-mapping.json` as `{"<reviewer>": {"A": "<author>", ...}}`. Send each adviser the Stage 3 pointer message. Log sends and receipts. Each returns `outbox/<role>/stage3.md` with, per response, `evidence 1–5`, `actionability 1–5`, and 60 words.

## Stage 4: Verdict

Sum scores per adviser across the four reviewers. Write `verdict.md`, 300 words max including REJECTED lines, exact template:

```
VERDICT: <Do A | Do B | Not decidable, need <X> by <date>>
DECIDING POINT: <adviser role> said "<quoted claim>" — why it settled it
SCORES: <role: total> ... (top two must appear in reasoning above or explain why not)
BIGGEST RISK: <one Contrarian item tagged high likelihood + high severity, or say why you chose a lower-tagged one>
LEADING INDICATOR: <what to watch>
KILL CRITERIA: reverse this if <X> observed by <date>
REJECTED <option>: <one reason, drawn from a take or review, not invented here>
(one REJECTED line per non-chosen option)
```

The REJECTED lines exist for the decision record. A future reader needs why the others lost more than why the winner won.

"Not decidable" is a real verdict, not a hedge. Use it when the panel exposed a missing fact that flips the answer. If the door is two-way and options are close, say: pick either, decide within 24h, here is the tiebreak. Log `type: verdict`. Show it to the user before Stage 5.

## Stage 5: Plan

Write `inbox/executor/stage5-verdict.md` from the Stage 5 template with the verdict inline. Send the pointer. Executor returns `outbox/executor/stage5.md`, a week plan naming only stakeholders in the brief. Log `type: plan`. Export the transcript.

## Stage 6: Deliver plan.md and decision-record.md

Write `<run>/plan.md` from `references/plan-template.md`: brief, verdict, week plan, score table, links, and an empty Feedback section. Write `decision-record.md` from `references/adr-template.md`, every run, from run files only, at `RECORD PATH` if the brief names one, else in the run dir. Send both (`SendUserFile` when available, otherwise the paths). Two projections of one run: plan is for acting this week, record is for whoever reopens the question later. The plan is per round; the record is one living file per decision, updated in place on every later round with a History line. The user edits Feedback and re-triggers with `/council <path>/plan.md`; the re-trigger procedure is in `references/plan-template.md`. Rounds are unlimited, the user decides when to stop.

## Downstream documents

PRDs, specs, API designs, and system designs are not council outputs. They are separate skills that consume `decision-record.md` for their contested decisions and cite it. Council stays the decision engine; those skills own their document shapes. See `docs/ROADMAP.md` in the repo for the planned set and the contract between them.

## Fallback: no subagents

If `Agent` and `SendMessage` are unavailable, run stages in one context, still writing every file and log line so the viewer works. State at the top: "Single-context mode. Cross-review is not independent, treat scores as indicative." Skip Stage 3 scores, keep the written critique.

## Output to the user

1. Viewer URL, at the start
2. Frozen brief, before spawning
3. Verdict, before Stage 5
4. `plan.md` and `decision-record.md`, at the end. Plan for acting, record for history
5. `transcript.html`, alongside

Adviser output never reaches the user unless you relay it. `plan.md` is the relay.
