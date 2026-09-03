#!/usr/bin/env node
// Zip one skill folder into dist/<name>.skill (plain zip; same format the Save-skill card accepts).
// Excludes evals/ and anything gitignored. Runs validate first.
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const name = process.argv[2];
if (!name) { console.error('usage: pnpm package <skill-name>'); process.exit(2); }
const root = new URL('..', import.meta.url).pathname;
const dir = join(root, 'skills', name);
if (!existsSync(join(dir, 'SKILL.md'))) { console.error(`no skill at skills/${name}`); process.exit(2); }

execFileSync('node', [join(root, 'scripts/validate-skills.mjs')], { stdio: 'inherit' });

const dist = join(root, 'dist');
mkdirSync(dist, { recursive: true });
const out = join(dist, `${name}.skill`);
rmSync(out, { force: true });
execFileSync('zip', ['-qr', out, name, '-x', `${name}/evals/*`, '*/__pycache__/*', '*/.DS_Store'], { cwd: join(root, 'skills'), stdio: 'inherit' });
console.log(`wrote dist/${name}.skill`);
