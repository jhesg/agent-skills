import { existsSync, renameSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import react from '@vitejs/plugin-react';
import { defineConfig, type Plugin } from 'vite';
import { viteSingleFile } from 'vite-plugin-singlefile';

export interface ArtifactOptions {
  /** Skill folder under skills/ that owns this artifact. */
  skill: string;
  /** Output file name without extension: skills/<skill>/assets/<name>.html */
  name: string;
  /** id of the <script type="application/json"> slot the skill's server fills. Informational; kept for tooling. */
  slotId?: string;
  /** Dev server port. Defaults to a stable hash of the artifact name in 5200–5299. */
  port?: number;
}

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

function stablePort(name: string): number {
  let h = 0;
  for (const c of name) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return 5200 + (h % 100);
}

/** Rename the single emitted index.html to <name>.html so several artifacts can share one assets/ dir. */
function renameOutput(outDir: string, name: string): Plugin {
  return {
    name: 'agent-skills:rename-output',
    closeBundle() {
      const from = join(outDir, 'index.html');
      const to = join(outDir, `${name}.html`);
      if (existsSync(from)) {
        rmSync(to, { force: true });
        renameSync(from, to);
      }
    },
  };
}

/**
 * Vite config for one skill artifact.
 * Why single-file: skills are copied, not built, by their users. The HTML must carry everything.
 * Why publicDir=fixtures with copyPublicDir=false: dev serves realistic data, the build ships none of it.
 */
export function defineArtifact(opts: ArtifactOptions) {
  const outDir = join(repoRoot, 'skills', opts.skill, 'assets');
  return defineConfig({
    plugins: [react(), viteSingleFile({ removeViteModuleLoader: true }), renameOutput(outDir, opts.name)],
    publicDir: 'fixtures',
    server: { port: opts.port ?? stablePort(`${opts.skill}-${opts.name}`), strictPort: false },
    build: {
      outDir,
      emptyOutDir: false,
      copyPublicDir: false,
      assetsInlineLimit: Number.MAX_SAFE_INTEGER,
      cssCodeSplit: false,
      modulePreload: false,
      reportCompressedSize: false,
      target: 'es2022',
    },
    define: { __ARTIFACT_SLOT_ID__: JSON.stringify(opts.slotId ?? `${opts.skill}-data`) },
  });
}
