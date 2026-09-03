#!/usr/bin/env python3
"""Preview an .excalidraw file in the bundled viewer, or export it.

Live:   preview.py <file.excalidraw> [--port 8770]     serves viewer at / and the file at /diagram.excalidraw; page polls for changes
Static: preview.py <file.excalidraw> --static <out.html>   standalone HTML with the diagram inlined in the data slot
SVG:    preview.py <file.excalidraw> --svg <out.svg>     server-side SVG of the generator subset (no browser needed)

Stdlib only.
"""
import argparse
import html
import json
import re
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIEWER = HERE.parent / "assets" / "viewer.html"
SLOT_RE = re.compile(r'(<script type="application/json" id="diagram-data">)(.*?)(</script>)', re.S)


class Handler(SimpleHTTPRequestHandler):
    file: Path = Path(".")

    def translate_path(self, path):
        clean = path.split("?", 1)[0]
        if clean in ("", "/", "/index.html"):
            return str(VIEWER)
        if clean == "/diagram.excalidraw":
            return str(self.file)
        return str(self.file.parent / "__nope__")

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass


def to_svg(doc: dict) -> str:
    """Render the generator's subset. Text metrics are approximate; the browser viewer is the reference."""
    els = [e for e in doc["elements"] if not e.get("isDeleted")]
    if not els:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"/>'
    minx = min(e["x"] for e in els) - 24; miny = min(e["y"] for e in els) - 24
    maxx = max(e["x"] + e["width"] for e in els) + 24; maxy = max(e["y"] + e["height"] for e in els) + 24
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx} {miny} {maxx-minx} {maxy-miny}" width="{maxx-minx}" height="{maxy-miny}" font-family="Helvetica, Arial, sans-serif">',
           f'<rect x="{minx}" y="{miny}" width="{maxx-minx}" height="{maxy-miny}" fill="#ffffff"/>']
    by_id = {e["id"]: e for e in els}
    for e in els:
        t = e["type"]; x, y, w, h = e["x"], e["y"], e["width"], e["height"]
        stroke, fill = e.get("strokeColor", "#000"), e.get("backgroundColor", "transparent")
        dash = ' stroke-dasharray="8 6"' if e.get("strokeStyle") == "dashed" else ""
        if t == "frame":
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#bbbbbb" stroke-width="1.5" rx="6"/>')
            out.append(f'<text x="{x+8}" y="{y+18}" font-size="13" fill="#6b6862">{html.escape(e.get("name") or "")}</text>')
        elif t == "rectangle":
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>')
        elif t == "ellipse":
            out.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>')
        elif t == "diamond":
            pts = f"{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}"
            out.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>')
        elif t == "arrow":
            pts = " ".join(f"{x+px},{y+py}" for px, py in e["points"])
            out.append(f'<polyline points="{pts}" fill="none" stroke="{stroke}" stroke-width="2"{dash} marker-end="url(#ah-{stroke[1:]})"/>')
        elif t == "text":
            size = e.get("fontSize", 16); lines = e["text"].split("\n")
            c = by_id.get(e.get("containerId"))
            anchor = "middle" if e.get("textAlign", "center") == "center" else "start"
            if c and c["type"] != "arrow":
                cx = c["x"] + c["width"] / 2; total = size * 1.25 * len(lines)
                ty = c["y"] + c["height"] / 2 - total / 2 + size
            elif c and c["type"] == "arrow":
                cx = x + w / 2; ty = y + size
            else:
                cx = x + (w / 2 if anchor == "middle" else 0); ty = y + size
            for i, ln in enumerate(lines):
                fs = size if i == 0 else max(11, size - 2)
                out.append(f'<text x="{cx}" y="{ty + i*size*1.25}" font-size="{fs}" text-anchor="{anchor}" fill="{stroke}">{html.escape(ln)}</text>')
    colors = {e["strokeColor"] for e in els if e["type"] == "arrow"}
    defs = "".join(f'<marker id="ah-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in colors)
    out.insert(1, f"<defs>{defs}</defs>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file"); ap.add_argument("--port", type=int, default=8770)
    ap.add_argument("--static"); ap.add_argument("--svg")
    a = ap.parse_args()
    f = Path(a.file).resolve()
    if not f.is_file():
        sys.exit(f"not a file: {f}")
    if a.svg:
        Path(a.svg).write_text(to_svg(json.loads(f.read_text())), encoding="utf-8"); print(f"wrote {a.svg}"); return
    if a.static:
        html_src = VIEWER.read_text(encoding="utf-8")
        if not SLOT_RE.search(html_src):
            sys.exit("viewer.html has no diagram-data slot; rebuild the artifact")
        data = json.dumps({"excalidraw": json.loads(f.read_text()), "name": f.name}).replace("</", "<\\/")
        Path(a.static).write_text(SLOT_RE.sub(lambda m: m.group(1) + data + m.group(3), html_src, count=1), encoding="utf-8")
        print(f"wrote {a.static}"); return
    Handler.file = f
    httpd = HTTPServer(("127.0.0.1", a.port), Handler)
    print(f"diagram preview: http://127.0.0.1:{a.port}/  ({f})", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
