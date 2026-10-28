"""Draft situation files for problems that don't have a crafted one yet, then validate them.

Input is a CSV of problem metadata only (no statements):  id,slug,title,difficulty,tags
(tags separated by ';'). Drafts that compile, pass their own tests, and produce a trace in
which every mapped variable exists are written to web/data/problems/ as tier "auto";
everything else goes to data/review/ with the reason.

  uv run --with anthropic --with httpx scripts/generate.py catalog.csv --limit 20
  uv run --with anthropic --with httpx scripts/generate.py catalog.csv --batch          # 50% cost, async
  uv run --with anthropic --with httpx scripts/generate.py --collect <batch_id>         # fetch + validate

Needs ANTHROPIC_API_KEY (or an `ant auth login` profile) and the runner (docker compose up).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

import anthropic
import httpx

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "web" / "data" / "problems"
REVIEW = ROOT / "data" / "review"
RUNNER_URL = os.environ.get("RUNNER_URL", "http://127.0.0.1:8765")
MODEL = os.environ.get("GEN_MODEL", "claude-opus-5-5")

WORLDS = ["arrays", "two-pointers", "sliding-window", "stack", "binary-search", "linked-list", "trees", "heap",
          "graphs", "backtracking", "dp", "intervals", "greedy", "bits"]
THEMES = ["dock", "market", "forest", "city", "farm", "castle", "cave", "space", "lab"]

LAYER = {
    "type": "object",
    "properties": {
        "kind": {"type": "string", "enum": ["array", "string", "bars", "grid", "map", "set", "stack", "queue", "heap",
                                             "list", "tree", "graph", "intervals", "values"]},
        "var": {"type": "string"},
        "label": {"type": "string"},
        "style": {"type": "string", "enum": ["crates", "tiles", "letters"]},
        "palette": {"type": "string", "enum": ["islands", "oranges", "maze", "dp", "board", "bool"]},
        "pointers": {"type": "array", "items": {"type": "string"}},
        "cell_pointers": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
        "window": {"type": "array", "items": {"type": "string"}},
        "vars": {"type": "array", "items": {"type": "string"}},
        "heads": {"type": "array", "items": {"type": "string"}},
        "lookup": {"type": "array", "items": {"type": "string"}},
        "edges": {"type": "string"},
        "adj": {"type": "string"},
        "n": {"type": "string"},
        "state": {"type": "string"},
        "directed": {"type": "boolean"},
        "reverse": {"type": "boolean"},
    },
    "required": ["kind", "label"],
    "additionalProperties": False,
}

SCHEMA = {
    "type": "object",
    "properties": {
        "world": {"type": "string", "enum": WORLDS},
        "theme": {"type": "string", "enum": THEMES},
        "story_title": {"type": "string"},
        "story_text": {"type": "string"},
        "story_goal": {"type": "string"},
        "method": {"type": "string"},
        "ret": {"type": "string"},
        "params": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
        "output": {"type": "string"},
        "compare": {"type": "string", "enum": ["exact", "unordered", "unordered-deep", "float"]},
        "tests": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"args_json": {"type": "string"}, "expected_json": {"type": "string"}},
                "required": ["args_json", "expected_json"],
                "additionalProperties": False,
            },
        },
        "visual_test": {"type": "integer"},
        "layers": {"type": "array", "items": LAYER},
        "reference": {"type": "string"},
        "hints": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["world", "theme", "story_title", "story_text", "story_goal", "method", "ret", "params", "output",
                 "compare", "tests", "visual_test", "layers", "reference", "hints"],
    "additionalProperties": False,
}

GUIDE = """You write "situation files" for PixelTrace, a site where a user's C++ solution to a classic
interview problem is traced line by line with gdb and replayed as a pixel-art scene.

Write ONLY original text. Never reproduce or paraphrase a published problem statement; invent a small
world (a dock, market, orchard, rail yard, castle...) where the data structures are physical things,
and state the task in that world. Keep story_text to 2-3 sentences and story_goal to one sentence.

Spec: use the standard LeetCode C++ signature for the method (class Solution, `method`, `ret`, and
`params` as [type, name] pairs, e.g. ["vector<int>&", "nums"]). Supported parameter types: int, long long,
double, bool, char, string, ListNode*, TreeNode*, vector<...> of those, pair<...>. If the original
signature uses something else (Node*, design classes, interactive APIs), adapt to these types and say so
in hints. output is "return", or "param:N" for void methods that modify parameter N in place.
compare: "unordered" when any order of the top-level list is accepted, "unordered-deep" when inner lists
may also be in any order.

Tests: 4-6 tests. args_json is a JSON array with one entry per parameter; ListNode* is a JSON list of
values, TreeNode* is a LeetCode level-order list with null; char is a 1-char string. expected_json is the
correct output. Include edge cases. visual_test is the index of a small, illustrative test (array length
<= 12, grid <= 6x6, tree <= 15 nodes) because the scene replays every line of it.

reference: a correct, readable C++17 solution (no main, no #include needed; bits/stdc++.h, ListNode and
TreeNode are provided). Prefer index-based loops and named locals, because the scene maps variable names:
the tracer captures locals of every function in the Solution class, its member fields, and arguments.

layers: which variables become which sprites. Every name you reference must exist in the reference.
- array/string/bars: var = a vector or string; pointers = int index variables walking on it; window = [lo, hi]
  inclusive index variables for a spotlight; style "tiles" for result/DP rows, "letters" for strings.
- grid: var = vector<vector<...>>; palette islands ('1'/'0'), oranges (0/1/2), maze (0/1), dp (numbers),
  board (chars), bool; cell_pointers = [[rowVar, colVar]].
- map/set: var = map/unordered_map/set; lookup = variables whose value is a key being looked up.
- stack/queue/heap: var = std::stack/queue/deque/priority_queue.
- list: vars = ListNode* variables (heads = the input list parameters).
- tree: var = the TreeNode* root parameter; pointers = TreeNode* variables to show as characters.
- graph: edges = edge-list parameter and n = node-count parameter (reverse=true if [a,b] means b->a), or
  adj = adjacency vector<vector<int>>; state = vector<int>/vector<bool> per node; pointers = int node vars.
- intervals: vars = vector<vector<int>> interval lists (input first, result second); pointers = [index var].
- values: vars = scalar variables shown as signposts (sums, best-so-far, counters).
Use 1-4 layers. Recursion gets a call-stack row automatically.
"""


def example_block() -> str:
    picks = ["two-sum-ii-input-array-is-sorted", "number-of-islands", "reverse-linked-list"]
    out = []
    for slug in picks:
        f = OUT / f"{slug}.json"
        if f.exists():
            p = json.loads(f.read_text())
            out.append(json.dumps({k: p[k] for k in ("title", "story", "spec", "compare", "tests", "visualTest", "scene", "reference")}))
    return "Examples of finished situation files (different JSON shape from your output, same content):\n" + "\n".join(out)


def build_params(row: dict) -> dict:
    user = (
        f"Problem: LeetCode {row['id']} \"{row['title']}\" ({row['difficulty']}), tags: {row['tags']}.\n"
        "Write its situation file."
    )
    return {
        "model": MODEL,
        "max_tokens": 16000,
        "system": [
            {"type": "text", "text": GUIDE},
            {"type": "text", "text": example_block(), "cache_control": {"type": "ephemeral"}},
        ],
        "messages": [{"role": "user", "content": user}],
        "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
    }


def to_problem(row: dict, d: dict) -> dict:
    layers = []
    for layer in d["layers"]:
        layer = {k: v for k, v in layer.items() if v not in (None, [], "")}
        if "cell_pointers" in layer:
            layer["pointers"] = layer.pop("cell_pointers")
        layers.append(layer)
    tests = [{"args": json.loads(t["args_json"]), "expected": json.loads(t["expected_json"])} for t in d["tests"]]
    spec = {"method": d["method"], "ret": d["ret"], "params": d["params"]}
    if d["output"] != "return":
        spec["output"] = d["output"]
    return {
        "id": int(row["id"]), "slug": row["slug"], "title": row["title"], "difficulty": row["difficulty"],
        "world": d["world"], "tags": [t for t in row["tags"].split(";") if t],
        "story": {"title": d["story_title"], "text": d["story_text"], "goal": d["story_goal"]},
        "spec": spec, "compare": d["compare"], "tests": tests,
        "visualTest": max(0, min(d["visual_test"], len(tests) - 1)),
        "scene": {"theme": d["theme"], "layers": layers}, "reference": d["reference"], "hints": d["hints"],
        "tier": "auto",
    }


def mapped_names(layers: list[dict]) -> set[str]:
    names = set()
    for layer in layers:
        for k in ("var", "edges", "adj", "n", "state"):
            if layer.get(k):
                names.add(layer[k])
        for k in ("pointers", "vars", "window", "lookup"):
            for x in layer.get(k, []):
                names.update(x if isinstance(x, list) else [x])
    return names


def validate(p: dict) -> str | None:
    body = {"code": p["reference"], "spec": {**p["spec"], "output": p["spec"].get("output", "return")},
            "tests": [{"args": t["args"], "expected": t["expected"]} for t in p["tests"]],
            "compare": p["compare"], "trace": p["visualTest"]}
    try:
        r = httpx.post(f"{RUNNER_URL}/run", json=body, timeout=120).json()
    except httpx.HTTPError as e:
        return f"runner unreachable: {e}"
    if r.get("fatal"):
        return r["fatal"]
    if not r["compile"]["ok"]:
        return "compile error: " + r["compile"]["raw"][:600]
    bad = [x for x in r["results"] if not x["passed"]]
    if bad:
        x = bad[0]
        return f"test {x['i']} failed: expected {x['expected']} got {x['output']} {x['error'] or ''}"
    tr = r.get("trace") or {}
    if not tr.get("steps"):
        return f"empty trace: {tr.get('end')}"
    seen = set()
    for step in tr["steps"]:
        for frame in step["stack"]:
            seen.update(frame["vars"].keys())
    missing = mapped_names(p["scene"]["layers"]) - seen
    if missing:
        return f"scene maps variables never seen in the trace: {sorted(missing)}"
    return None


def save(row: dict, msg) -> None:
    if msg.stop_reason == "refusal":
        print(f"  {row['slug']}: refused")
        return
    if msg.stop_reason == "max_tokens":
        print(f"  {row['slug']}: hit max_tokens")
        return
    text = next((b.text for b in msg.content if b.type == "text"), "")
    try:
        p = to_problem(row, json.loads(text))
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        REVIEW.mkdir(parents=True, exist_ok=True)
        (REVIEW / f"{row['slug']}.raw.txt").write_text(text)
        print(f"  {row['slug']}: unparseable ({e})")
        return
    err = validate(p)
    if err:
        REVIEW.mkdir(parents=True, exist_ok=True)
        (REVIEW / f"{row['slug']}.json").write_text(json.dumps({**p, "review_reason": err}, indent=2))
        print(f"  {row['slug']}: review — {err[:120]}")
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{row['slug']}.json").write_text(json.dumps(p, indent=2) + "\n")
        print(f"  {row['slug']}: ok")


def load_rows(path: str, limit: int | None) -> list[dict]:
    with open(path, newline="", encoding="utf8") as fh:
        rows = [r for r in csv.DictReader(fh) if not (OUT / f"{r['slug']}.json").exists()]
    return rows[:limit] if limit else rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("catalog", nargs="?")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--batch", action="store_true", help="submit through the Message Batches API (50% cost)")
    ap.add_argument("--collect", metavar="BATCH_ID", help="fetch a finished batch and validate its drafts")
    args = ap.parse_args()
    client = anthropic.Anthropic()

    if args.collect:
        meta = json.loads((REVIEW / f"batch-{args.collect}.json").read_text())
        while client.messages.batches.retrieve(args.collect).processing_status != "ended":
            print("waiting for batch…")
            time.sleep(60)
        for res in client.messages.batches.results(args.collect):
            row = meta[res.custom_id]
            if res.result.type == "succeeded":
                save(row, res.result.message)
            else:
                print(f"  {row['slug']}: {res.result.type}")
        return

    if not args.catalog:
        ap.error("catalog CSV required")
    rows = load_rows(args.catalog, args.limit)
    print(f"{len(rows)} problems without a situation file")

    if args.batch:
        from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
        from anthropic.types.messages.batch_create_params import Request

        reqs = [Request(custom_id=f"p{r['id']}", params=MessageCreateParamsNonStreaming(**build_params(r))) for r in rows]
        batch = client.messages.batches.create(requests=reqs)
        REVIEW.mkdir(parents=True, exist_ok=True)
        (REVIEW / f"batch-{batch.id}.json").write_text(json.dumps({f"p{r['id']}": r for r in rows}))
        print(f"submitted batch {batch.id}; collect with --collect {batch.id}")
        return

    for row in rows:
        try:
            msg = client.messages.create(**build_params(row))
        except anthropic.RateLimitError:
            time.sleep(30)
            msg = client.messages.create(**build_params(row))
        except anthropic.APIStatusError as e:
            print(f"  {row['slug']}: API error {e.status_code}")
            continue
        save(row, msg)


if __name__ == "__main__":
    sys.exit(main())
