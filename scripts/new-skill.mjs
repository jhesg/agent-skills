#!/usr/bin/env node
// Scaffold skills/<name>/ and artifacts/<name>-<artifact>/ and register the marketplace entry.
// usage: pnpm new-skill <name> [artifact-name]   (artifact defaults to "view")
import { mkdirSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const [name, artifact = 'view'] = process.argv.slice(2);
if (!name || !/^[a-z][a-z0-9-]*$/.test(name)) { console.error('usage: pnpm new-skill <kebab-name> [artifact-name]'); process.exit(2); }
const root = new URL('..', import.meta.url).pathname;
const skill = join(root, 'skills', name);
const app = join(root, 'artifacts', `${name}-${artifact}`);
if (existsSync(skill)) { console.error(`skills/${name} exists`); process.exit(2); }

const w = (p, s) => { mkdirSync(join(p, '..'), { recursive: true }); writeFileSync(p, s); };

w(join(skill, 'SKILL.md'), `---
name: ${name}
description: <what it does>. Use when <concrete user phrases and situations>. Do not use when <near misses>.
---

# ${name}

<why this skill exists, in two sentences>

## Artifact

Open \`assets/${artifact}.html\` ... (say when: first action, or after which stage)

## Steps

1. ...
`);
w(join(skill, '.claude-plugin/plugin.json'), JSON.stringify({ name, version: '0.1.0', description: '<one line>', author: { name: 'Jhonatan', url: 'https://github.com/jhesg' }, license: 'MIT' }, null, 2) + '\n');
w(join(skill, 'references/.gitkeep'), '');
w(join(skill, 'evals/evals.json'), JSON.stringify({ skill_name: name, evals: [] }, null, 2) + '\n');

w(join(app, 'package.json'), JSON.stringify({
  name: `@agent-skills/${name}-${artifact}`, private: true, type: 'module',
  scripts: { dev: 'vite', build: 'vite build', typecheck: 'tsc -p tsconfig.json' },
  dependencies: { react: '^19.2.0', 'react-dom': '^19.2.0', '@agent-skills/ui': 'workspace:*', '@agent-skills/artifact-kit': 'workspace:*' },
  devDependencies: { '@agent-skills/vite-config': 'workspace:*', '@types/react': '^19.2.0', '@types/react-dom': '^19.2.0', typescript: '^5.9.0', vite: '^7.0.0' },
}, null, 2) + '\n');
w(join(app, 'vite.config.ts'), `import { defineArtifact } from '@agent-skills/vite-config';\n\nexport default defineArtifact({ skill: '${name}', name: '${artifact}', slotId: '${name}-data' });\n`);
w(join(app, 'tsconfig.json'), JSON.stringify({ extends: '../../tsconfig.base.json', include: ['src'] }, null, 2) + '\n');
w(join(app, 'index.html'), `<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>${name}</title>\n<script type="application/json" id="${name}-data"></script>\n</head>\n<body>\n<div id="root"></div>\n<script type="module" src="/src/main.tsx"></script>\n</body>\n</html>\n`);
w(join(app, 'src/main.tsx'), `import { createRoot } from 'react-dom/client';\nimport '@agent-skills/ui/tokens.css';\nimport { App } from './App';\n\ncreateRoot(document.getElementById('root')!).render(<App />);\n`);
w(join(app, 'src/App.tsx'), `import { Toolbar, Empty } from '@agent-skills/ui';\n\nexport function App() {\n  return (\n    <>\n      <Toolbar title="${name}" />\n      <main className="as-content"><Empty>Nothing yet.</Empty></main>\n    </>\n  );\n}\n`);
w(join(app, 'fixtures/.gitkeep'), '');

const mp = join(root, '.claude-plugin/marketplace.json');
const m = JSON.parse(readFileSync(mp, 'utf8'));
if (!m.plugins.some((p) => p.name === name)) {
  m.plugins.push({ name, description: '<one line>', source: './', strict: false, skills: [`./skills/${name}`] });
  writeFileSync(mp, JSON.stringify(m, null, 2) + '\n');
}
console.log(`scaffolded skills/${name} and artifacts/${name}-${artifact}; run pnpm install`);
