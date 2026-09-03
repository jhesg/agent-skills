import { useMemo, useState } from 'react';
import { formatTime, useArtifactData } from '@agent-skills/artifact-kit';
import { Bubble, CodeBlock, Disclosure, Empty, Pill, Select, Toggle, Toolbar, type Tone } from '@agent-skills/ui';
import { buildFeed, channelKey, loadLive, type CouncilData, type CouncilEvent } from './model';

declare const __ARTIFACT_SLOT_ID__: string;

function tone(e: CouncilEvent): Tone {
  if (e.derived) return 3;
  if (e.from === 'chairman') return 1;
  return 2;
}

export function App() {
  const { data, mode } = useArtifactData<CouncilData>({ slotId: __ARTIFACT_SLOT_ID__, load: loadLive });
  const [channel, setChannel] = useState('all');
  const [stage, setStage] = useState('all');
  const [expand, setExpand] = useState(false);

  const feed = useMemo(() => (data ? buildFeed(data) : { events: [], mapping: null }), [data]);
  const channels = useMemo(() => [...new Set(feed.events.filter((e) => e.from && e.to).map((e) => channelKey(e.from, e.to)))].sort(), [feed]);
  const stages = useMemo(() => [...new Set(feed.events.map((e) => String(e.stage)))].sort(), [feed]);
  const shown = feed.events.filter((e) => (channel === 'all' || channelKey(e.from, e.to) === channel) && (stage === 'all' || String(e.stage) === stage));

  const status = data
    ? <>{mode} · <b>{feed.events.filter((e) => !e.derived).length}</b> events</>
    : (mode === 'static' ? 'static · no log' : 'live · waiting for log');

  return (
    <>
      <Toolbar title="Council" status={status}>
        <Select label="Channel" value={channel} onChange={(e) => setChannel(e.target.value)}>
          <option value="all">All</option>
          {channels.map((c) => <option key={c} value={c}>{c}</option>)}
        </Select>
        <Select label="Stage" value={stage} onChange={(e) => setStage(e.target.value)}>
          <option value="all">All</option>
          {stages.map((s) => <option key={s} value={s}>Stage {s}</option>)}
        </Select>
        <Toggle label="Expand files" checked={expand} onChange={(e) => setExpand(e.target.checked)} />
      </Toolbar>
      <main className="as-content">
        {!data && <Empty>Waiting for log/events.jsonl…</Empty>}
        {data && shown.length === 0 && <Empty>No events for this filter.</Empty>}
        {shown.map((e, i) => {
          const content = e.body ?? (e.ref ? data?.files[e.ref] : undefined);
          return (
            <Bubble key={`${e.ts}-${e.from}-${e.to}-${i}`} from={e.from || '?'} to={e.to} ts={formatTime(e.ts)} tone={tone(e)}
              meta={<><Pill>stage {e.stage ?? '?'}</Pill><Pill>{e.type || 'event'}</Pill></>} text={e.text}>
              {content !== undefined && (
                <Disclosure summary={e.ref ?? 'review'} open={expand}>
                  <CodeBlock>{content}</CodeBlock>
                </Disclosure>
              )}
              {content === undefined && e.ref && <div className="as-bubble__to">→ {e.ref} (not readable)</div>}
            </Bubble>
          );
        })}
      </main>
    </>
  );
}
