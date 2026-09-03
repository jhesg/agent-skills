# Skill guidelines

A skill is a folder Claude reads when a task matches its description. Write it for a capable reader who has never seen this repo.

## Folder

```
skills/<name>/
  .claude-plugin/plugin.json   name, version, description
  SKILL.md                     frontmatter + instructions, under ~200 lines
  references/                  charters, templates, long guidance, read on demand
  scripts/                     Python stdlib runtime helpers, executable
  assets/                      built artifacts, committed, never hand-edited
  evals/evals.json             test prompts (optional but encouraged)
```

## SKILL.md

- Frontmatter `description` is the trigger. Say what it does and when to use it, with concrete phrases users type. Say when not to use it. Be a little pushy; skills under-trigger.
- Body explains why, then how. Stages with clear barriers. Tables for role and file maps.
- Reference files by relative path from the skill folder. Never by absolute path, never outside the folder.
- If the skill starts a server or opens an artifact, say exactly when: first action, or after a specific stage.
- State honest ceilings. If a guarantee is instruction-based rather than enforced, say so in the words the model should use to the user.

## Portability test

Copy the folder to `/tmp/x/` and read SKILL.md as if you were Claude with only that folder. Every path resolves? Every script runs with `python3` alone? Every asset opens from `file://`? Then it ships.

## Subagent-based skills

- Charters live in `references/`, passed inline as the `Agent` prompt. Not in `.claude/agents/`, which is machine-local.
- Name the subagent type generically (`general-purpose`). Restrict behaviour by instruction and explain why the restriction matters.
- Keep agents alive across stages with `SendMessage`. Say so explicitly; a fresh `Agent` call loses context.
- Include a single-context fallback for hosts without subagents.

## Evals

Three prompts minimum: a clear hit, a clear miss the guard should reject, and an edge case. Put them in `evals/evals.json`. Run them with the skill-creator workflow when the skill changes materially.
