import { useRef, useState } from 'react';
import { useArtifactData } from '@agent-skills/artifact-kit';
import { Empty, Pill, Toggle, Toolbar } from '@agent-skills/ui';
import { Diagram } from './Diagram';
import { svgToString, type DiagramData, type ExDoc } from './excalidraw';

declare const __ARTIFACT_SLOT_ID__: string;

async function loadLive(fetchText: (p: string) => Promise<string | null>): Promise<DiagramData | null> {
  const raw = await fetchText('diagram.excalidraw');
  if (raw === null) return null;
  try { return { excalidraw: JSON.parse(raw) as ExDoc, name: 'diagram.excalidraw' }; } catch { return null; }
}

export function App() {
  const { data, mode } = useArtifactData<DiagramData>({ slotId: __ARTIFACT_SLOT_ID__, load: loadLive, intervalMs: 1500 });
  const [fit, setFit] = useState(true);
  const svgRef = useRef<SVGSVGElement>(null);
  const [copied, setCopied] = useState(false);

  const els = data?.excalidraw.elements ?? [];
  const nodes = els.filter((e) => ['rectangle', 'ellipse', 'diamond'].includes(e.type)).length;
  const arrows = els.filter((e) => e.type === 'arrow').length;

  const copySvg = async () => {
    if (!svgRef.current) return;
    try { await navigator.clipboard.writeText(svgToString(svgRef.current)); setCopied(true); setTimeout(() => setCopied(false), 1500); } catch { /* clipboard blocked */ }
  };

  return (
    <>
      <Toolbar title="Diagram" status={data ? <>{mode} · <b>{nodes}</b> nodes · <b>{arrows}</b> edges</> : `${mode} · waiting for diagram.excalidraw`}>
        {data?.name && <Pill>{data.name}</Pill>}
        <Toggle label="Fit to width" checked={fit} onChange={(e) => setFit(e.target.checked)} />
        <button type="button" className="as-select" onClick={copySvg} disabled={!data}>{copied ? 'Copied' : 'Copy SVG'}</button>
      </Toolbar>
      <main className="as-content" style={{ maxWidth: fit ? undefined : 'none', overflowX: 'auto' }}>
        {!data && <Empty>Waiting for diagram.excalidraw…</Empty>}
        {data && <div style={fit ? undefined : { width: 'max-content' }}><Diagram ref={svgRef} elements={els} /></div>}
      </main>
    </>
  );
}
