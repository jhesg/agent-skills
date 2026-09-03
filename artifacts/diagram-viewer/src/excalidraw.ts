/** The subset of Excalidraw elements the generator emits. Anything else is drawn as a grey placeholder. */
export interface ExElement {
  id: string; type: string; x: number; y: number; width: number; height: number;
  strokeColor?: string; backgroundColor?: string; strokeStyle?: string; isDeleted?: boolean;
  text?: string; fontSize?: number; textAlign?: string; containerId?: string | null;
  points?: [number, number][]; name?: string | null;
}
export interface ExDoc { type: string; version: number; elements: ExElement[] }
export interface DiagramData { excalidraw: ExDoc; name?: string }

export function bounds(els: ExElement[], pad = 24) {
  const live = els.filter((e) => !e.isDeleted);
  if (!live.length) return { x: 0, y: 0, w: 10, h: 10 };
  const minx = Math.min(...live.map((e) => e.x)) - pad;
  const miny = Math.min(...live.map((e) => e.y)) - pad;
  const maxx = Math.max(...live.map((e) => e.x + e.width)) + pad;
  const maxy = Math.max(...live.map((e) => e.y + e.height)) + pad;
  return { x: minx, y: miny, w: maxx - minx, h: maxy - miny };
}

/** Serialise the rendered SVG element to a standalone file string. */
export function svgToString(svg: SVGSVGElement): string {
  const clone = svg.cloneNode(true) as SVGSVGElement;
  clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  return new XMLSerializer().serializeToString(clone);
}
