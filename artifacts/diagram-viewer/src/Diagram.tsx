import { forwardRef } from 'react';
import { bounds, type ExElement } from './excalidraw';

const LINE = 1.25;

/** Renders the generator subset as plain SVG. Roughness ignored on purpose: the preview is for checking structure. */
export const Diagram = forwardRef<SVGSVGElement, { elements: ExElement[] }>(function Diagram({ elements }, ref) {
  const els = elements.filter((e) => !e.isDeleted);
  const byId = new Map(els.map((e) => [e.id, e]));
  const b = bounds(els);
  const arrowColors = [...new Set(els.filter((e) => e.type === 'arrow').map((e) => e.strokeColor ?? '#000'))];

  return (
    <svg ref={ref} viewBox={`${b.x} ${b.y} ${b.w} ${b.h}`} width={b.w} height={b.h} style={{ maxWidth: '100%', height: 'auto', display: 'block' }}
      fontFamily="Helvetica, Arial, sans-serif">
      <defs>
        {arrowColors.map((c) => (
          <marker key={c} id={`ah-${c.slice(1)}`} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill={c} />
          </marker>
        ))}
      </defs>
      <rect x={b.x} y={b.y} width={b.w} height={b.h} fill="#ffffff" />
      {els.map((e) => {
        const stroke = e.strokeColor ?? '#000', fill = e.backgroundColor ?? 'transparent';
        const dash = e.strokeStyle === 'dashed' ? '8 6' : undefined;
        switch (e.type) {
          case 'frame':
            return (
              <g key={e.id}>
                <rect x={e.x} y={e.y} width={e.width} height={e.height} fill="none" stroke="#bbbbbb" strokeWidth={1.5} rx={6} />
                <text x={e.x + 8} y={e.y + 18} fontSize={13} fill="#6b6862">{e.name ?? ''}</text>
              </g>
            );
          case 'rectangle':
            return <rect key={e.id} x={e.x} y={e.y} width={e.width} height={e.height} rx={10} fill={fill} stroke={stroke} strokeWidth={2} strokeDasharray={dash} />;
          case 'ellipse':
            return <ellipse key={e.id} cx={e.x + e.width / 2} cy={e.y + e.height / 2} rx={e.width / 2} ry={e.height / 2} fill={fill} stroke={stroke} strokeWidth={2} strokeDasharray={dash} />;
          case 'diamond': {
            const { x, y, width: w, height: h } = e;
            return <polygon key={e.id} points={`${x + w / 2},${y} ${x + w},${y + h / 2} ${x + w / 2},${y + h} ${x},${y + h / 2}`} fill={fill} stroke={stroke} strokeWidth={2} strokeDasharray={dash} />;
          }
          case 'arrow': {
            const p0 = e.points?.[0] ?? [0, 0], p1 = e.points?.[e.points.length - 1] ?? [0, 0];
            return <line key={e.id} x1={e.x + p0[0]} y1={e.y + p0[1]} x2={e.x + p1[0]} y2={e.y + p1[1]} stroke={stroke} strokeWidth={2} strokeDasharray={dash} markerEnd={`url(#ah-${stroke.slice(1)})`} />;
          }
          case 'text': {
            const size = e.fontSize ?? 16, lines = (e.text ?? '').split('\n');
            const c = e.containerId ? byId.get(e.containerId) : undefined;
            const anchor = (e.textAlign ?? 'center') === 'center' ? 'middle' : 'start';
            let cx: number, ty: number;
            if (c && c.type !== 'arrow') { cx = c.x + c.width / 2; ty = c.y + c.height / 2 - (size * LINE * lines.length) / 2 + size; }
            else if (c) { cx = e.x + e.width / 2; ty = e.y + size; }
            else { cx = e.x + (anchor === 'middle' ? e.width / 2 : 0); ty = e.y + size; }
            return (
              <g key={e.id}>
                {lines.map((ln, i) => (
                  <text key={i} x={cx} y={ty + i * size * LINE} fontSize={i === 0 ? size : Math.max(11, size - 2)} textAnchor={anchor} fill={stroke}>{ln}</text>
                ))}
              </g>
            );
          }
          default:
            return <rect key={e.id} x={e.x} y={e.y} width={e.width} height={e.height} fill="none" stroke="#bbb" strokeDasharray="4 4" />;
        }
      })}
    </svg>
  );
});
