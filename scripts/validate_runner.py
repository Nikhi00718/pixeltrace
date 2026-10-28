"""Run every problem's reference through the live runner with tracing on, and check the scene mapping.

  python scripts/validate_runner.py [slug ...]

Checks: tests pass, the visual test produces a non-empty trace that ends normally, and every variable
the scene maps appears in at least one traced frame. Needs the runner (docker compose up).
"""

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "web" / "data" / "problems"
RUNNER_URL = os.environ.get("RUNNER_URL", "http://127.0.0.1:8765")


def mapped_names(layers):
    names = set()
    for layer in layers:
        if layer.get("kind") == "row":
            names |= mapped_names(layer.get("children", []))
            continue
        for k in ("var", "edges", "adj", "n", "state"):
            if layer.get(k):
                names.add(layer[k])
        for k in ("pointers", "vars", "window", "lookup", "heads"):
            for x in layer.get(k, []) or []:
                names.update(x if isinstance(x, list) else [x])
        if isinstance(layer.get("water"), list):
            names.update(layer["water"])
    return names


def check(p):
    body = {
        "code": p["reference"],
        "spec": {**p["spec"], "output": p["spec"].get("output", "return")},
        "tests": [{"args": t["args"], "expected": t["expected"]} for t in p["tests"]],
        "compare": p.get("compare", "exact"),
        "trace": p.get("visualTest", 0),
    }
    req = urllib.request.Request(f"{RUNNER_URL}/run", data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    t0 = time.time()
    r = json.loads(urllib.request.urlopen(req, timeout=180).read())
    ms = int((time.time() - t0) * 1000)
    if r.get("fatal"):
        return f"fatal: {r['fatal']}", ms
    if not r["compile"]["ok"]:
        return "compile: " + r["compile"]["raw"][:300], ms
    bad = [x for x in r["results"] if not x["passed"]]
    if bad:
        return f"test {bad[0]['i']}: expected {bad[0]['expected']} got {bad[0]['output']} {bad[0]['error']}", ms
    tr = r["trace"] or {}
    steps = tr.get("steps") or []
    if not steps:
        return f"empty trace: {tr.get('end')}", ms
    if tr["end"]["kind"] != "exit":
        return f"trace ended by {tr['end']}", ms
    seen = set()
    for s in steps:
        for f in s["stack"]:
            seen |= set(f["vars"])
    missing = mapped_names(p["scene"]["layers"]) - seen
    if missing:
        return f"never traced: {sorted(missing)} (saw {sorted(seen)})", ms
    return f"ok · {len(steps)} steps", ms


def main():
    only = set(sys.argv[1:])
    fails = 0
    for f in sorted(PROBLEMS.glob("*.json")):
        p = json.loads(f.read_text(encoding="utf8"))
        if only and p["slug"] not in only:
            continue
        try:
            msg, ms = check(p)
        except Exception as e:  # noqa: BLE001
            msg, ms = f"error: {e}", 0
        ok = msg.startswith("ok")
        fails += not ok
        print(f"{'OK ' if ok else 'BAD'} {p['slug']:<50} {ms:>6} ms  {msg}")
    print(f"\n{fails} failing")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
