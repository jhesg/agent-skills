#!/usr/bin/env node
// Validate every skill under skills/: frontmatter, plugin manifest, marketplace entry,
// no absolute or parent-escaping paths, assets present, scripts executable.
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join, relative } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const skillsDir = join(root, 'skills');
const marketplace = JSON.parse(readFileSync(join(root, '.claude-plugin/marketplace.json'), 'utf8'));
const listed = new Set(marketplace.plugins.flatMap((p) => p.skills ?? []).map((s) => s.replace(/^\.\/skills\//, '')));

let failures = 0;
const fail = (skill, msg) => { failures++; console.error(`✗ ${skill}: ${msg}`); };

function walk(dir, out = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, out); else out.push(p);
  }
  return out;
}

for (const name of readdirSync(skillsDir)) {
  const dir = join(skillsDir, name);
  if (!statSync(dir).isDirectory()) continue;
  const skillMd = join(dir, 'SKILL.md');
  if (!existsSync(skillMd)) { fail(name, 'missing SKILL.md'); continue; }
  const md = readFileSync(skillMd, 'utf8');
  const fm = md.match(/^---\n([\s\S]*?)\n---/);
  if (!fm) fail(name, 'SKILL.md has no frontmatter');
  else {
    const fmName = fm[1].match(/^name:\s*(.+)$/m)?.[1]?.trim();
    const desc = fm[1].match(/^description:\s*(.+)$/m)?.[1]?.trim();
    if (fmName !== name) fail(name, `frontmatter name "${fmName}" ≠ folder "${name}"`);
    if (!desc || desc.length < 40) fail(name, 'description missing or too short to trigger reliably');
  }
  const manifest = join(dir, '.claude-plugin/plugin.json');
  if (!existsSync(manifest)) fail(name, 'missing .claude-plugin/plugin.json');
  else {
    const pj = JSON.parse(readFileSync(manifest, 'utf8'));
    if (pj.name !== name) fail(name, `plugin.json name "${pj.name}" ≠ folder`);
    if (!pj.version) fail(name, 'plugin.json missing version');
  }
  if (!listed.has(name)) fail(name, 'not listed in .claude-plugin/marketplace.json');

  for (const f of walk(dir)) {
    const rel = relative(dir, f);
    if (/\.(md|py|json|html|mjs|sh)$/.test(f)) {
      const txt = readFileSync(f, 'utf8');
      if (/\]\((\.\.\/)+/.test(txt) || /(^|\s)\.\.\/[\w-]+/m.test(txt)) fail(name, `${rel}: parent-escaping path`);
      if (/\/Users\/|\/home\/[a-z]/.test(txt)) fail(name, `${rel}: absolute home path`);
    }
    if (rel.startsWith('scripts/') && f.endsWith('.py') && !(statSync(f).mode & 0o111)) fail(name, `${rel}: not executable`);
  }
  const assetRefs = [...md.matchAll(/assets\/([\w.-]+\.html)/g)].map((m) => m[1]);
  for (const a of new Set(assetRefs)) if (!existsSync(join(dir, 'assets', a))) fail(name, `assets/${a} referenced but missing (run pnpm build)`);
  if (!failures) console.log(`✓ ${name}`);
}
process.exit(failures ? 1 : 0);
