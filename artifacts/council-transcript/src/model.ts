import { parseJsonl } from '@agent-skills/artifact-kit';

/** One line of log/events.jsonl, written by the Chairman on every send and receipt. */
export interface CouncilEvent {
  ts: string;
  stage: number;
  from: string;
  to: string;
  type: 'brief' | 'pointer' | 'verdict' | 'plan' | 'note' | 'review' | string;
  text?: string;
  ref?: string;
  /** Derived review rows carry their body inline instead of a ref. */
  body?: string;
  derived?: boolean;
}

/** reviewer → label → author. Chairman-only file; the viewer joins it so humans see who reviewed whom. */
export type Stage3Mapping = Record<string, Record<string, string>>;

/** What the skill's server hands us: raw file contents keyed by path relative to the run dir. */
export interface CouncilData {
  files: Record<string, string>;
  run_dir?: string;
}

export interface ParsedReview { label: string; evidence: string; actionability: string; body: string }

/** Parse a Stage 3 file: blocks headed "A | evidence: n | actionability: n". */
export function parseReview(text: string): ParsedReview[] {
  const re = /^([A-D])\s*\|\s*evidence:\s*(\d)\s*\|\s*actionability:\s*(\d)\s*$/gim;
  const heads: Array<{ label: string; evidence: string; actionability: string; start: number; end: number }> = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(text))) heads.push({ label: m[1]!.toUpperCase(), evidence: m[2]!, actionability: m[3]!, start: m.index, end: m.index + m[0].length });
  return heads.map((h, i) => ({ label: h.label, evidence: h.evidence, actionability: h.actionability, body: text.slice(h.end, heads[i + 1]?.start ?? text.length).trim() }));
}

export function safeJson<T>(s: string | undefined): T | null {
  if (!s) return null;
  try { return JSON.parse(s) as T; } catch { return null; }
}

/** Turn raw files into the event list the feed renders: logged events plus derived adviser→adviser reviews. */
export function buildFeed(data: CouncilData): { events: CouncilEvent[]; mapping: Stage3Mapping | null } {
  const events = parseJsonl<CouncilEvent>(data.files['log/events.jsonl'] ?? '');
  const mapping = safeJson<Stage3Mapping>(data.files['log/stage3-mapping.json']);
  const derived: CouncilEvent[] = [];
  if (mapping) {
    for (const reviewer of Object.keys(mapping)) {
      const path = `outbox/${reviewer}/stage3.md`;
      const txt = data.files[path];
      if (!txt) continue;
      const done = events.find((e) => e.from === reviewer && e.stage === 3 && e.ref === path);
      for (const r of parseReview(txt)) {
        const author = mapping[reviewer]?.[r.label];
        if (!author) continue;
        derived.push({ ts: done?.ts ?? '', stage: 3, from: reviewer, to: author, type: 'review', derived: true,
          text: `Response ${r.label} · evidence ${r.evidence}/5 · actionability ${r.actionability}/5`, body: r.body });
      }
    }
  }
  const all = [...events, ...derived].sort((a, b) => String(a.ts).localeCompare(String(b.ts)));
  return { events: all, mapping };
}

export const channelKey = (a: string, b: string) => [a, b].sort().join(' ↔ ');

/** Live loader: read the log, mapping, every referenced file, and every outbox stage3 file. */
export async function loadLive(fetchText: (p: string) => Promise<string | null>): Promise<CouncilData | null> {
  const log = await fetchText('log/events.jsonl');
  if (log === null) return null;
  const files: Record<string, string> = { 'log/events.jsonl': log };
  const mappingRaw = await fetchText('log/stage3-mapping.json');
  if (mappingRaw !== null) files['log/stage3-mapping.json'] = mappingRaw;
  const refs = new Set(parseJsonl<CouncilEvent>(log).map((e) => e.ref).filter((r): r is string => Boolean(r)));
  const mapping = safeJson<Stage3Mapping>(mappingRaw ?? undefined);
  if (mapping) for (const r of Object.keys(mapping)) refs.add(`outbox/${r}/stage3.md`);
  await Promise.all([...refs].map(async (r) => { const t = await fetchText(r); if (t !== null) files[r] = t; }));
  return { files };
}
