"""Compile every reference solution, fill in/check expected outputs, and write web/data/problems/*.json.

Run on Linux/WSL (needs g++):  python3 scripts/build_problems.py [slug ...]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "runner"))
sys.path.insert(0, str(ROOT / "scripts"))

from app.runner import equal, run_request  # noqa: E402
from problems_src import P  # noqa: E402
import problems_src_2  # noqa: E402,F401  (registers the second batch into P)
import problems_src_3  # noqa: E402,F401
import problems_src_4  # noqa: E402,F401
import problems_src_5  # noqa: E402,F401
import problems_src_6  # noqa: E402,F401
import problems_src_7  # noqa: E402,F401
import problems_src_8  # noqa: E402,F401
import problems_src_9  # noqa: E402,F401

OUT = ROOT / "web" / "data" / "problems"


def build(p: dict) -> bool:
    tests = [{"args": t["args"]} for t in p["tests"]]
    res = run_request({"code": p["reference"], "spec": p["spec"], "tests": tests, "compare": "exact"})
    if res.get("fatal") or not res["compile"]["ok"]:
        print(f"  !! {p['slug']}: {res.get('fatal') or res['compile']['raw'][:800]}")
        return False
    ok = True
    for t, r in zip(p["tests"], res["results"]):
        if r["error"] or not r["has_output"]:
            print(f"  !! {p['slug']}: reference failed on {t['args']}: {r['error']} {r['stderr'][:200]}")
            ok = False
            continue
        if "expected" in t and not equal(r["output"], t["expected"], p.get("compare", "exact")):
            print(f"  !! {p['slug']}: expected {t['expected']} but reference gave {r['output']}")
            ok = False
        t.setdefault("expected", r["output"])
    if ok:
        OUT.mkdir(parents=True, exist_ok=True)
        data = dict(p)
        data.setdefault("tier", "crafted")
        (OUT / f"{p['slug']}.json").write_text(json.dumps(data, indent=2) + "\n")
    return ok


def main():
    only = set(sys.argv[1:])
    good = bad = 0
    for p in P:
        if only and p["slug"] not in only:
            continue
        if build(p):
            good += 1
        else:
            bad += 1
    print(f"built {good}, failed {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
