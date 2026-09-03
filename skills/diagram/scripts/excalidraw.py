#!/usr/bin/env python3
"""Build an .excalidraw file from a small declarative spec. Stdlib only.

usage: excalidraw.py <spec.json> <out.excalidraw>

Spec (JSON):
{
  "title": "Notification pipeline",             # optional, drawn as a heading
  "layout": "flow" | "columns" | "grid",         # default flow
  "direction": "LR" | "TB",                      # flow only, default LR
  "nodes": [ {"id": "api", "label": "API", "shape": "rect|ellipse|diamond", "tone": "1|2|3|danger|muted", "group": "A", "note": "small text under label"} ],
  "edges": [ {"from": "api", "to": "queue", "label": "enqueue", "style": "solid|dashed", "tone": "..."} ],
  "groups": [ {"id": "A", "label": "Option A: outbox + worker"} ],  # columns layout lays groups side by side
  "legend": [ {"tone": "1", "label": "chosen"} ]
}

Why a spec instead of hand-written elements: the agent is good at deciding what the picture says and bad at
computing coordinates. The layout here is deliberately simple and predictable, so the result never has
overlapping boxes or arrows that miss their targets.
"""
import json
import random
import sys
from collections import defaultdict

# Palette mirrors @agent-skills/ui tokens (light theme). Excalidraw files carry their own colours.
TONES = {
    "1": {"stroke": "#2f5d8a", "bg": "#dbe7f3"},
    "2": {"stroke": "#7a4b1f", "bg": "#f1e3d3"},
    "3": {"stroke": "#4f6b3a", "bg": "#e1ead7"},
    "danger": {"stroke": "#9b2c2c", "bg": "#f3dada"},
    "muted": {"stroke": "#6b6862", "bg": "#eeece7"},
}
INK = "#1c1b19"
FONT = 2          # 1 Virgil (hand), 2 Helvetica, 3 Cascadia. Helvetica reads better at small sizes.
NODE_W, NODE_H = 180, 64
GAP_X, GAP_Y = 90, 60
PAD = 32
rng = random.Random(7)


def _id(prefix):
    return f"{prefix}-{rng.randrange(1 << 30):08x}"


def _base(kind, x, y, w, h, tone="muted", **extra):
    t = TONES.get(tone, TONES["muted"])
    el = {
        "id": _id(kind), "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
        "strokeColor": t["stroke"], "backgroundColor": t["bg"], "fillStyle": "solid",
        "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
        "groupIds": [], "frameId": None, "roundness": {"type": 3} if kind == "rectangle" else None,
        "seed": rng.randrange(1 << 31), "version": 1, "versionNonce": rng.randrange(1 << 31),
        "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False,
    }
    el.update(extra)
    return el


def _text(x, y, w, h, text, size=16, container=None, align="center", color=INK):
    lines = text.split("\n")
    el = _base("text", x, y, w, h, "muted", strokeColor=color, backgroundColor="transparent", roundness=None)
    el.update({
        "text": text, "originalText": text, "fontSize": size, "fontFamily": FONT,
        "textAlign": align, "verticalAlign": "middle" if container else "top",
        "containerId": container, "lineHeight": 1.25, "baseline": size,
        "autoResize": True,
    })
    el["height"] = round(size * 1.25 * len(lines))
    return el


def _node(n, x, y):
    shape = {"rect": "rectangle", "ellipse": "ellipse", "diamond": "diamond"}.get(n.get("shape", "rect"), "rectangle")
    box = _base(shape, x, y, NODE_W, NODE_H, n.get("tone", "muted"))
    label = n["label"] + (f"\n{n['note']}" if n.get("note") else "")
    txt = _text(x, y, NODE_W, NODE_H, label, size=16 if not n.get("note") else 14, container=box["id"])
    box["boundElements"].append({"id": txt["id"], "type": "text"})
    return box, txt


def _edge(e, a, b, direction):
    # Anchor on box edges facing each other.
    ax, ay = a["x"] + a["width"] / 2, a["y"] + a["height"] / 2
    bx, by = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
    if abs(bx - ax) >= abs(by - ay):
        sx = a["x"] + a["width"] if bx > ax else a["x"]; sy = ay
        ex = b["x"] if bx > ax else b["x"] + b["width"]; ey = by
    else:
        sx = ax; sy = a["y"] + a["height"] if by > ay else a["y"]
        ex = bx; ey = b["y"] if by > ay else b["y"] + b["height"]
    t = TONES.get(e.get("tone", "muted"), TONES["muted"])
    arrow = _base("arrow", sx, sy, ex - sx, ey - sy, e.get("tone", "muted"), backgroundColor="transparent", roundness={"type": 2})
    arrow.update({
        "points": [[0, 0], [ex - sx, ey - sy]],
        "startBinding": {"elementId": a["id"], "focus": 0, "gap": 4},
        "endBinding": {"elementId": b["id"], "focus": 0, "gap": 4},
        "startArrowhead": None, "endArrowhead": "arrow", "lastCommittedPoint": None,
        "strokeStyle": e.get("style", "solid"), "strokeColor": t["stroke"],
    })
    a["boundElements"].append({"id": arrow["id"], "type": "arrow"})
    b["boundElements"].append({"id": arrow["id"], "type": "arrow"})
    out = [arrow]
    if e.get("label"):
        lw = max(60, len(e["label"]) * 8)
        lbl = _text((sx + ex) / 2 - lw / 2, (sy + ey) / 2 - 22, lw, 20, e["label"], size=13, container=arrow["id"])
        arrow["boundElements"].append({"id": lbl["id"], "type": "text"})
        out.append(lbl)
    return out


def _layers(nodes, edges):
    """Longest-path layering over a DAG; back edges ignored for ranking."""
    ids = [n["id"] for n in nodes]
    succ = defaultdict(list); indeg = defaultdict(int)
    for e in edges:
        if e["from"] in ids and e["to"] in ids and e["from"] != e["to"]:
            succ[e["from"]].append(e["to"]); indeg[e["to"]] += 1
    rank = {i: 0 for i in ids}
    order, q = [], [i for i in ids if indeg[i] == 0] or ids[:1]
    seen = set(q)
    while q:
        u = q.pop(0); order.append(u)
        for v in succ[u]:
            rank[v] = max(rank[v], rank[u] + 1)
            if v not in seen:
                seen.add(v); q.append(v)
    for i in ids:  # nodes unreachable from sources (cycles): place after their predecessors
        if i not in seen: rank[i] = max([rank.get(e["from"], 0) + 1 for e in edges if e["to"] == i] or [0])
    layers = defaultdict(list)
    for i in ids: layers[rank[i]].append(i)
    return [layers[k] for k in sorted(layers)]


def build(spec):
    nodes = spec.get("nodes", []); edges = spec.get("edges", []); groups = spec.get("groups", [])
    layout = spec.get("layout", "flow"); direction = spec.get("direction", "LR")
    by_id = {n["id"]: n for n in nodes}
    elements, boxes = [], {}
    y0 = PAD + (48 if spec.get("title") else 0)

    def place_flow(sub_nodes, sub_edges, ox, oy, direction):
        layers = _layers(sub_nodes, sub_edges)
        maxlen = max((len(l) for l in layers), default=1)
        for li, layer in enumerate(layers):
            for ni, nid in enumerate(layer):
                offset = (maxlen - len(layer)) / 2
                if direction == "LR":
                    x = ox + li * (NODE_W + GAP_X); y = oy + (ni + offset) * (NODE_H + GAP_Y)
                else:
                    x = ox + (ni + offset) * (NODE_W + GAP_X); y = oy + li * (NODE_H + GAP_Y)
                box, txt = _node(by_id[nid], x, y)
                boxes[nid] = box; elements.extend([box, txt])
        if direction == "LR":
            return len(layers) * (NODE_W + GAP_X) - GAP_X, maxlen * (NODE_H + GAP_Y) - GAP_Y
        return maxlen * (NODE_W + GAP_X) - GAP_X, len(layers) * (NODE_H + GAP_Y) - GAP_Y

    if layout == "columns" and groups:
        x = PAD
        for g in groups:
            gn = [n for n in nodes if n.get("group") == g["id"]]
            ge = [e for e in edges if by_id.get(e["from"], {}).get("group") == g["id"] and by_id.get(e["to"], {}).get("group") == g["id"]]
            w, h = place_flow(gn, ge, x + PAD, y0 + 56, "TB")
            fw = max(w, NODE_W) + 2 * PAD; fh = h + 56 + PAD
            frame = _base("frame", x, y0, fw, fh, "muted", backgroundColor="transparent", strokeColor="#bbb", roundness=None)
            frame["name"] = g.get("label", g["id"])
            for n in gn: boxes[n["id"]]["frameId"] = frame["id"]
            elements.insert(0, frame)
            x += fw + GAP_X
    elif layout == "grid":
        cols = max(1, round(len(nodes) ** 0.5))
        for i, n in enumerate(nodes):
            box, txt = _node(n, PAD + (i % cols) * (NODE_W + GAP_X), y0 + (i // cols) * (NODE_H + GAP_Y))
            boxes[n["id"]] = box; elements.extend([box, txt])
    else:
        place_flow(nodes, edges, PAD, y0, direction)

    for e in edges:
        if e["from"] in boxes and e["to"] in boxes:
            elements.extend(_edge(e, boxes[e["from"]], boxes[e["to"]], direction))
    # text elements bound to boxes must be updated after frames assigned
    for el in elements:
        if el["type"] == "text" and el.get("containerId") in boxes:
            el["frameId"] = boxes[el["containerId"]]["frameId"]

    if spec.get("title"):
        elements.insert(0, _text(PAD, PAD, 600, 28, spec["title"], size=22, align="left"))
    if spec.get("legend"):
        maxy = max((el["y"] + el["height"] for el in elements), default=y0) + GAP_Y
        for i, item in enumerate(spec["legend"]):
            sw = _base("rectangle", PAD + i * 200, maxy, 18, 18, item.get("tone", "muted"))
            elements.append(sw)
            elements.append(_text(PAD + i * 200 + 26, maxy - 2, 160, 20, item["label"], size=13, align="left"))
    return {
        "type": "excalidraw", "version": 2, "source": "agent-skills/diagram",
        "elements": elements,
        "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
        "files": {},
    }


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1]))
    doc = build(spec)
    with open(sys.argv[2], "w") as f:
        json.dump(doc, f, indent=1)
    n = sum(1 for e in doc["elements"] if e["type"] in ("rectangle", "ellipse", "diamond"))
    a = sum(1 for e in doc["elements"] if e["type"] == "arrow")
    print(f"wrote {sys.argv[2]}: {n} nodes, {a} edges")


if __name__ == "__main__":
    main()
