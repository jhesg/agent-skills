# spec

Write a technical spec for one feature: what changes, how, how it rolls out, how you know it works. Hard design calls go to a panel and come back as decision records.

## Use it when

- You need engineering agreement before coding a feature.
- A change touches data, rollout, or external systems and people will ask "why this way".
- An old spec needs updating after review.

Not for product requirements (use prd), whole-system architecture (system-design), or API contracts (api-design).

## How it works

![How spec works](https://raw.githubusercontent.com/jhesg/agent-skills/main/skills/spec/docs/how-it-works.svg)

1. Intake: the skill reads your message, files, and repo, fills the template, and marks what it knows, what it guessed, and what is missing. It asks at most three questions.
2. It finds the hard calls. Obvious ones are decided inline with a one-line reason. Genuinely contested ones, at most three, go to the [council](https://github.com/jhesg/agent-skills/tree/main/skills/council) skill, which writes a decision record next to your document.
3. It drafts the document, cites the records instead of re-arguing them, and runs a review checklist.
4. You get `spec.md` plus a `decisions/` folder. Write in the Feedback section, run it again, it updates in place. As many rounds as you want.

## What is in the document

Summary, problem and goals, non-goals, current state, proposed design, alternatives, rollout, observability, testing, security, open questions, decision records, changelog.

## Try it

```
Write a tech spec for saved searches on our job board: users save filters and get a daily email digest of new matches. Next.js frontend, NestJS API, Postgres. We already have a notifications table and a daily cron.
```

You get: a spec with the data model, digest job design, rollout behind a flag, and one or two decision records, likely on per-search vs per-user digests.

```
/spec docs/specs/saved-searches.md — feedback: digest should be per search, and legal wants unsubscribe per search.
```

You get: the same file updated in place, a changelog line, and the affected decision re-argued if it was a recorded one.

## Install

```bash
claude plugin marketplace add jhesg/agent-skills
claude plugin install spec@jhesg-agent-skills
claude plugin install council@jhesg-agent-skills   # optional, for contested decisions
```

Internals for agents: [SKILL.md](SKILL.md). Template: [references/template.md](references/template.md).
