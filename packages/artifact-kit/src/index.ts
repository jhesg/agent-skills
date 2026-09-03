import { useEffect, useRef, useState } from 'react';

/** Parse JSON Lines. Bad lines are skipped, not fatal: a half-written line during a live poll is normal. */
export function parseJsonl<T = unknown>(raw: string): T[] {
  const out: T[] = [];
  for (const line of raw.split('\n')) {
    const t = line.trim();
    if (!t) continue;
    try { out.push(JSON.parse(t) as T); } catch { /* partial write, skip */ }
  }
  return out;
}

/** Read the JSON slot the skill's server fills for static export. Empty or missing slot → null. */
export function readJsonSlot<T = unknown>(id: string): T | null {
  const el = document.getElementById(id);
  const txt = el?.textContent?.trim();
  if (!txt) return null;
  try { return JSON.parse(txt) as T; } catch { return null; }
}

/** Fetch a relative path from the same origin with cache busting. null on any failure. */
export async function fetchText(path: string): Promise<string | null> {
  try {
    const r = await fetch(`/${path.replace(/^\//, '')}?t=${Date.now()}`, { cache: 'no-store' });
    return r.ok ? await r.text() : null;
  } catch { return null; }
}

/** Local HH:MM:SS. Falls back to the raw string when unparsable so nothing silently disappears. */
export function formatTime(ts: string | undefined): string {
  if (!ts) return '';
  const d = new Date(ts);
  return isNaN(d.getTime()) ? ts : d.toLocaleTimeString();
}

export type DataMode = 'static' | 'live' | 'waiting';

export interface UseArtifactDataOptions<T> {
  /** id of the <script type="application/json"> element. When it has content, the page is static. */
  slotId: string;
  /** Live loader: given fetchText, return the data or null if not ready yet. Called on an interval. */
  load: (fetchText: (path: string) => Promise<string | null>) => Promise<T | null>;
  intervalMs?: number;
}

/**
 * One hook, two modes. Static when the slot is filled (export), live polling otherwise (watch).
 * Why one hook: the artifact should not know which mode it is in beyond a label; the skill decides.
 */
export function useArtifactData<T>({ slotId, load, intervalMs = 2000 }: UseArtifactDataOptions<T>) {
  const [data, setData] = useState<T | null>(() => readJsonSlot<T>(slotId));
  const [mode, setMode] = useState<DataMode>(() => (readJsonSlot(slotId) ? 'static' : 'waiting'));
  const loadRef = useRef(load);
  loadRef.current = load;

  useEffect(() => {
    if (mode === 'static') return;
    let alive = true;
    const tick = async () => {
      const next = await loadRef.current(fetchText);
      if (!alive) return;
      if (next !== null) { setData(next); setMode('live'); }
    };
    void tick();
    const id = setInterval(tick, intervalMs);
    return () => { alive = false; clearInterval(id); };
  }, [mode, intervalMs]);

  return { data, mode };
}
