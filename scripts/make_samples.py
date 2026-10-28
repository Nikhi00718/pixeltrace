"""Write hand-simulated traces (same format as the gdb tracer) to web/public/samples/ for the playground."""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "web" / "public" / "samples"
OUT.mkdir(parents=True, exist_ok=True)


def step(line, fn, frames, nodes=None, error=None):
    s = {"line": line, "fn": fn, "stack": frames, "nodes": nodes or {}}
    if error:
        s["error"] = error
    return s


def two_pointers():
    nums, target = [1, 3, 4, 5, 7, 10, 11], 9
    steps = []
    l, r = 0, len(nums) - 1
    base = {"numbers": nums, "target": target}
    steps.append(step(4, "twoSum", [{"fn": "twoSum", "line": 4, "vars": {**base, "l": l, "r": r}}]))
    while l < r:
        s = nums[l] + nums[r]
        steps.append(step(6, "twoSum", [{"fn": "twoSum", "line": 6, "vars": {**base, "l": l, "r": r, "s": s}}]))
        if s == target:
            break
        if s < target:
            l += 1
            steps.append(step(8, "twoSum", [{"fn": "twoSum", "line": 8, "vars": {**base, "l": l, "r": r, "s": s}}]))
        else:
            r -= 1
            steps.append(step(9, "twoSum", [{"fn": "twoSum", "line": 9, "vars": {**base, "l": l, "r": r, "s": s}}]))
    scene = {"theme": "dock", "layers": [
        {"kind": "array", "var": "numbers", "label": "sorted crates", "pointers": ["l", "r"], "window": ["l", "r"]},
        {"kind": "values", "vars": ["target", "s"]}]}
    return scene, {"steps": steps, "end": {"kind": "exit", "code": 0}, "truncated": False}


def reverse_list():
    vals = [1, 2, 3, 4, 5]
    addrs = [hex(0x5000 + 0x20 * i) for i in range(len(vals))]
    nxt = {a: (addrs[i + 1] if i + 1 < len(addrs) else None) for i, a in enumerate(addrs)}
    P = lambda a: {"$p": a} if a else None
    nodes = lambda: {a: {"val": vals[i], "next": nxt[a]} for i, a in enumerate(addrs)}
    steps = []
    prev, curr = None, addrs[0]
    head = addrs[0]
    fr = lambda line, extra: [{"fn": "reverseList", "line": line, "vars": {"head": P(head), "prev": P(prev), "curr": P(curr), **extra}}]
    steps.append(step(5, "reverseList", fr(5, {}), nodes()))
    while curr:
        n = nxt[curr]
        steps.append(step(6, "reverseList", fr(6, {"next": P(n)}), nodes()))
        nxt[curr] = prev
        steps.append(step(7, "reverseList", fr(7, {"next": P(n)}), nodes()))
        prev = curr
        steps.append(step(8, "reverseList", fr(8, {"next": P(n)}), nodes()))
        curr = n
        steps.append(step(9, "reverseList", fr(9, {"next": P(n)}), nodes()))
    steps.append(step(11, "reverseList", fr(11, {}), nodes()))
    scene = {"theme": "farm", "layers": [{"kind": "list", "vars": ["head", "prev", "curr", "next"], "heads": ["head"], "label": "train"}]}
    return scene, {"steps": steps, "end": {"kind": "exit", "code": 0}, "truncated": False}


def invert_tree():
    vals = [4, 2, 7, 1, 3, 6, 9]
    addrs = [hex(0x7000 + 0x30 * i) for i in range(7)]
    left = {addrs[i]: (addrs[2 * i + 1] if 2 * i + 1 < 7 else None) for i in range(7)}
    right = {addrs[i]: (addrs[2 * i + 2] if 2 * i + 2 < 7 else None) for i in range(7)}
    val = dict(zip(addrs, vals))
    P = lambda a: {"$p": a} if a else None
    nodes = lambda: {a: {"val": val[a], "left": left[a], "right": right[a]} for a in addrs}
    steps = []
    stack = []

    def snap(line):
        frames = [{"fn": "invertTree", "line": ln, "vars": {"root": P(a), **({"tmp": P(t)} if t is not None else {})}} for a, ln, t in stack]
        frames[-1]["line"] = line
        steps.append(step(line, "invertTree", frames, nodes()))

    def go(a):
        stack.append([a, 4, None])
        snap(4)
        if not a:
            stack.pop()
            return
        stack[-1][2] = left[a]
        snap(5)
        left[a], right[a] = right[a], left[a]
        snap(7)
        go(left[a])
        snap(8)
        go(right[a])
        snap(9)
        stack.pop()

    go(addrs[0])
    scene = {"theme": "forest", "layers": [{"kind": "tree", "var": "root", "pointers": ["root"], "label": "orchard"}]}
    return scene, {"steps": steps, "end": {"kind": "exit", "code": 0}, "truncated": False}


def islands():
    g = [list("11000"), list("11000"), list("00100"), list("00011")]
    C = lambda: [[{"$c": ch} for ch in row] for row in g]
    steps = []
    count = 0
    stack = []

    def snap(line, extra=None):
        frames = [{"fn": "numIslands", "line": 15, "vars": {"grid": C(), "count": count, **(extra or {})}}]
        for (r, c) in stack:
            frames.append({"fn": "sink", "line": line, "vars": {"grid": {"$alias": "grid"}, "r": r, "c": c}})
        steps.append(step(line, frames[-1]["fn"], frames))

    def sink(r, c):
        stack.append((r, c))
        snap(3)
        if r < 0 or c < 0 or r >= 4 or c >= 5 or g[r][c] != "1":
            stack.pop()
            return
        g[r][c] = "#"
        snap(4)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sink(r + dr, c + dc)
        stack.pop()

    for r in range(4):
        for c in range(5):
            snap(14, {"r": r, "c": c})
            if g[r][c] == "1":
                count += 1
                snap(16, {"r": r, "c": c})
                sink(r, c)
    scene = {"theme": "forest", "layers": [
        {"kind": "grid", "var": "grid", "palette": "islands", "label": "sea chart", "pointers": [["r", "c"]]},
        {"kind": "values", "vars": ["count"]}]}
    return scene, {"steps": steps, "end": {"kind": "exit", "code": 0}, "truncated": False}


for name, fn in [("two-pointers", two_pointers), ("reverse-list", reverse_list), ("invert-tree", invert_tree), ("islands", islands)]:
    scene, trace = fn()
    (OUT / f"{name}.json").write_text(json.dumps({"scene": scene, "trace": trace}))
    print(name, len(trace["steps"]), "steps")
