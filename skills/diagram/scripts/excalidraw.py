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


def _edge(e, a, b, direction, route="straight", clearance=0):
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
    if route == "under":      # LR back edge: drop below all nodes, run back, rise into the target
        sx, sy = ax, a["y"] + a["height"]; ex, ey = bx, b["y"] + b["height"]
        low = clearance - sy
        pts = [[0, 0], [0, low], [ex - sx, low], [ex - sx, ey - sy]]
        arrow["x"], arrow["y"] = sx, sy
    elif route == "side":     # TB back edge: swing out to the right of all nodes
        sx, sy = a["x"] + a["width"], ay; ex, ey = b["x"] + b["width"], by
        far = clearance - sx
        pts = [[0, 0], [far, 0], [far, ey - sy], [ex - sx, ey - sy]]
        arrow["x"], arrow["y"] = sx, sy
    else:
        pts = [[0, 0], [ex - sx, ey - sy]]
    arrow["width"] = max(abs(q[0]) for q in pts); arrow["height"] = max(abs(q[1]) for q in pts)
    arrow.update({
        "points": pts,
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
        if route == "under":
            lx, ly = arrow["x"] + pts[2][0] / 2 - lw / 2, arrow["y"] + pts[1][1] + 4
        elif route == "side":
            lx, ly = arrow["x"] + pts[1][0] + 6, arrow["y"] + pts[2][1] / 2 - 10
        else:
            lx, ly = (sx + ex) / 2 - lw / 2, (sy + ey) / 2 - 22
        lbl = _text(lx, ly, lw, 20, e["label"], size=13, container=arrow["id"], align="left" if route == "side" else "center")
        arrow["boundElements"].append({"id": lbl["id"], "type": "text"})
        out.append(lbl)
    return out


def _layers(nodes, edges):
    """Kahn layering. When a cycle blocks progress, the blocked node with the most processed
    predecessors is released; the edges that pointed back at it become back edges. Returns (layers, rank)."""
    ids = [n["id"] for n in nodes]
    succ = defaultdict(list); indeg = defaultdict(int)
    for e in edges:
        if e["from"] in ids and e["to"] in ids and e["from"] != e["to"]:
            succ[e["from"]].append(e["to"]); indeg[e["to"]] += 1
    rank = {i: 0 for i in ids}; done = set()
    q = [i for i in ids if indeg[i] == 0]
    while len(done) < len(ids):
        if not q:  # cycle: release the node whose remaining in-degree is smallest
            pending = [i for i in ids if i not in done]
            pick = min(pending, key=lambda i: (indeg[i], ids.index(i)))
            indeg[pick] = 0; q.append(pick)
        u = q.pop(0)
        if u in done: continue
        done.add(u)
        for v in succ[u]:
            if v in done: continue
            rank[v] = max(rank[v], rank[u] + 1)
            indeg[v] -= 1
            if indeg[v] <= 0: q.append(v)
    layers = defaultdict(list)
    for i in ids: layers[rank[i]].append(i)
    return [layers[k] for k in sorted(layers)], rank


def build(spec):
    global NODE_W
    nodes = spec.get("nodes", []); edges = spec.get("edges", []); groups = spec.get("groups", [])
    longest = max([len(l) for n in nodes for l in (n["label"] + ("\n" + n["note"] if n.get("note") else "")).split("\n")] or [0])
    NODE_W = max(180, longest * 8 + 28)
    layout = spec.get("layout", "flow"); direction = spec.get("direction", "LR")
    by_id = {n["id"]: n for n in nodes}
    elements, boxes = [], {}
    y0 = PAD + (48 if spec.get("title") else 0)

    def place_flow(sub_nodes, sub_edges, ox, oy, direction):
        layers, _ = _layers(sub_nodes, sub_edges)
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

    _, rank = _layers(nodes, edges)
    node_boxes = [b for b in boxes.values()]
    bottom = max((b["y"] + b["height"] for b in node_boxes), default=0) + GAP_Y
    right = max((b["x"] + b["width"] for b in node_boxes), default=0) + GAP_X
    for e in edges:
        if e["from"] in boxes and e["to"] in boxes:
            back = e.get("back") or rank.get(e["to"], 0) <= rank.get(e["from"], 0)
            if back and layout == "flow":
                route, clr = ("under", bottom) if direction == "LR" else ("side", right)
            else:
                route, clr = "straight", 0
            elements.extend(_edge(e, boxes[e["from"]], boxes[e["to"]], direction, route, clr))
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
