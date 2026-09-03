#!/usr/bin/env python3
"""Serve or export a council run directory as a group-chat transcript.

Live:   python3 serve_log.py <run_dir> [--port 8765]
        Opens http://localhost:<port>/ ; page polls log/events.jsonl every 2s.
Static: python3 serve_log.py <run_dir> --static <out.html>
        Writes one self-contained HTML with events and referenced files inlined.

Stdlib only. No dependencies. Safe to copy with the skill folder.
"""
import argparse
import json
import os
import re
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIEWER = HERE.parent / "assets" / "viewer.html"
SLOT_RE = re.compile(r'(<script type="application/json" id="council-data">)(.*?)(</script>)', re.S)


def read_text(p: Path):
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def collect(run_dir: Path) -> dict:
    """Gather everything the viewer needs into one JSON-serialisable dict."""
    files = {}
    events_raw = read_text(run_dir / "log" / "events.jsonl") or ""
    files["log/events.jsonl"] = events_raw
    mapping = read_text(run_dir / "log" / "stage3-mapping.json")
    if mapping is not None:
        files["log/stage3-mapping.json"] = mapping
    refs = set()
    for line in events_raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        ref = ev.get("ref")
        if ref:
            refs.add(ref)
    # Stage 3 outputs feed the derived adviser↔adviser channel even if unreferenced.
    for sub in ("outbox",):
        base = run_dir / sub
        if base.is_dir():
            for role_dir in base.iterdir():
                for f in role_dir.glob("*.md"):
                    refs.add(str(f.relative_to(run_dir)))
    for rel in sorted(refs):
        content = read_text(run_dir / rel)
        if content is not None:
            files[rel] = content
    return {"files": files, "run_dir": str(run_dir)}


class Handler(SimpleHTTPRequestHandler):
    run_dir: Path = Path(".")

    def translate_path(self, path):
        # Serve viewer at root, run_dir files elsewhere. Block traversal.
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if clean in ("", "/", "/index.html"):
            return str(VIEWER)
        rel = os.path.normpath(clean.lstrip("/"))
        if rel.startswith(".."):
            return str(self.run_dir / "__forbidden__")
        return str(self.run_dir / rel)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):  # quiet
        pass


def serve(run_dir: Path, port: int):
    Handler.run_dir = run_dir
    httpd = HTTPServer(("127.0.0.1", port), Handler)
    print(f"council viewer: http://127.0.0.1:{port}/  (run dir: {run_dir})", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


def export(run_dir: Path, out: Path):
    html = read_text(VIEWER)
    if html is None:
        sys.exit(f"viewer template missing: {VIEWER}")
    data = json.dumps(collect(run_dir)).replace("</", "<\\/")
    if not SLOT_RE.search(html):
        sys.exit("viewer.html has no council-data slot; rebuild the artifact")
    html = SLOT_RE.sub(lambda m: m.group(1) + data + m.group(3), html, count=1)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--static", metavar="OUT_HTML")
    a = ap.parse_args()
    run_dir = Path(a.run_dir).resolve()
    if not run_dir.is_dir():
        sys.exit(f"not a directory: {run_dir}")
    if a.static:
        export(run_dir, Path(a.static).resolve())
    else:
        serve(run_dir, a.port)


if __name__ == "__main__":
    main()
