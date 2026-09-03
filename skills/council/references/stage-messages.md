# Stage messages

The Chairman writes packets into `inbox/<role>/` and sends one-line pointers. Advisers write into `outbox/<role>/` and reply with one line. Keep messages to the pointer, no commentary; the files carry the content and the log carries the history.

## Stage 2 task line (appended to `inbox/<role>/stage2-task.md`, under the brief)

```
---
STAGE 2 TASK
Write your take on the brief above. 150 words max. Save it to outbox/<role>/stage2.md.
Reply with exactly one line: done: outbox/<role>/stage2.md
```

## Stage 1b packet (`inbox/<role>/stage1b-propose.md`, proposers only)

```
STAGE 1B: PROPOSE OPTIONS

The brief below has no options yet. The user asked the council to propose them. Propose from your lens, as your charter describes. Up to 2 options.

For each option:
NAME: <3–6 words>
WHAT: <one line>
FIRST IRREVERSIBLE STEP: <what, and how far in>
COST TO UNDO: <one line>

120 words total. Do not rank, do not recommend; that comes later and from others. Save to outbox/<role>/stage1b.md.
Reply with exactly one line: done: outbox/<role>/stage1b.md

---
BRIEF
<brief verbatim, OPTIONS marked "to be proposed">
```

Pointer message to send:

```
Stage 1b. Read inbox/<role>/stage1b-propose.md and do what it says.
```

## Stage 3 packet (`inbox/<role>/stage3-packet.md`)

```
STAGE 3: CROSS-REVIEW

Below are four responses to the same brief from other advisers. Labels A–D are arbitrary. You do not know who wrote what and should not guess.

For EACH response give:
- evidence: 1–5 (claims grounded in the brief or in stated reasoning, not assertion)
- actionability: 1–5 (could the Chairman act on it as written)
- 60 words max: what it gets right, what it gets wrong

Save exactly this format to outbox/<role>/stage3.md, nothing else:

A | evidence: n | actionability: n
<60 words>

B | evidence: n | actionability: n
<60 words>

C | ...
D | ...

Reply with exactly one line: done: outbox/<role>/stage3.md

---
RESPONSE A
<take>

RESPONSE B
<take>

RESPONSE C
<take>

RESPONSE D
<take>
```

Pointer message to send:

```
Stage 3. Read inbox/<role>/stage3-packet.md and do what it says.
```

## Stage 5 packet (`inbox/executor/stage5-verdict.md`, Executor only)

```
STAGE 5: PLAN

The Chairman has decided. Turn the verdict into this week's actions.

Rules:
- Name only stakeholders listed in the brief. If a needed person is not listed, write "unlisted: <role>" and stop there.
- Every action has an owner, a day, and a done-signal.
- Include one action that installs the leading indicator from the verdict.
- If the verdict is "Not decidable, need X", the plan is how to obtain X this week, nothing else.
- 200 words max.

Format:
MON: ...
TUE: ...
...
DEFER: <what not to touch this week and why>

Save to outbox/executor/stage5.md. Reply with exactly one line: done: outbox/executor/stage5.md

---
VERDICT
<verdict block verbatim>
```

Pointer message to send:

```
Stage 5. Read inbox/executor/stage5-verdict.md and do what it says.
```

## Length correction (any stage)

```
Your file <path> is <n> words. Cap is <cap>. Rewrite it to the cap in place, keep your strongest points, reply with the same done line.
```

## Log lines the Chairman writes for each exchange

Send: `{"ts":…,"stage":N,"from":"chairman","to":"<role>","type":"pointer","text":"<what was asked>","ref":"inbox/<role>/<file>"}`
Receipt: `{"ts":…,"stage":N,"from":"<role>","to":"chairman","type":"pointer","text":"done","ref":"outbox/<role>/<file>"}`
