# PixelTrace

Write C++ for classic interview problems and watch every line play out as a pixel-art scene.
Arrays are crates on a dock, stacks are towers, linked lists are trains, trees grow fruit,
graphs are towns on a map, recursion is a row of doors.

```
Editor (C++) ─► /api/run (Next.js) ─► runner (FastAPI, Docker)
                                       g++ -O0 -g -D_GLIBCXX_ASSERTIONS
                                       gdb + Python: stop on every line of solution.cpp,
                                       dump locals / call stack / reachable ListNode+TreeNode
                                    ◄─ { compile, results[], trace{steps[]} }
Scene engine (canvas) ◄─ trace + the problem's scene definition
```

## Layout

| Path | What it is |
| --- | --- |
| `runner/` | C++ runner: harness generator, gdb tracer, FastAPI service, Dockerfile |
| `runner/cpp/prelude.h` | LeetCode environment: `bits/stdc++.h`, `ListNode`, `TreeNode`, JSON output |
| `runner/app/gdb_tracer.py` | Runs inside gdb; one snapshot per executed line of the user's code |
| `web/` | Next.js app (editor, player, scene engine) |
| `web/src/scene/` | `layers.ts` (variable → sprite mapping per data structure), `scene.ts` (tweening renderer), `draw.ts` (sprites, themes) |
| `web/data/problems/*.json` | One situation file per problem (story, scene mapping, tests, reference) |
| `scripts/problems_src.py` | Source of the hand-crafted situation files |
| `scripts/build_problems.py` | Compiles every reference, fills/checks expected outputs, writes the JSON |
| `scripts/generate.py` | Drafts situation files for the rest of the catalog with Claude, validates them on the runner |
| `scripts/make_samples.py` | Sample traces for `/playground` |

## Run it locally

```bash
docker compose up --build -d
```

```bash
npm --prefix web install
```

```bash
npm --prefix web run dev
```

Open http://localhost:3000. The web app finds the runner at `RUNNER_URL` (default `http://127.0.0.1:8765`).
`/playground` replays any trace JSON with any scene definition — use it to author new scenes.

## Adding problems

Hand-crafted: add an entry to `scripts/problems_src.py`, then on Linux/WSL (needs g++):

```bash
python3 scripts/build_problems.py <slug>
```

Generated: put metadata (no statements) in a CSV like `scripts/catalog.example.csv`, start the runner, and:

```bash
uv run --with anthropic --with httpx scripts/generate.py catalog.csv --limit 20
```

`--batch` submits through the Message Batches API at half price; `--collect <batch_id>` fetches and validates.
A draft is published as tier `auto` only if its reference compiles, passes its own tests, and every variable
its scene maps actually appears in the gdb trace; everything else lands in `data/review/` with the reason.

## Scene definition

```json
{ "theme": "dock",
  "layers": [
    { "kind": "array", "var": "numbers", "pointers": ["l", "r"], "window": ["l", "r"] },
    { "kind": "values", "vars": ["target", "s"] } ] }
```

Kinds: `array` / `string` / `bars`, `grid` (palettes `islands`, `oranges`, `maze`, `dp`, `board`, `bool`),
`map` / `set`, `stack`, `queue`, `heap`, `list`, `tree`, `graph`, `intervals`, `values`, `calls`, `row`
(side by side), `auto`. Themes: `dock`, `market`, `forest`, `city`, `farm`, `castle`, `cave`, `space`, `lab`.

## Limits

- Design problems (`LRUCache` style classes) and interactive problems are not supported by the harness yet.
- Traces stop after 2,500 steps; use a small test to watch.
- The runner isolates submissions with rlimits inside one container. For a public deployment, run each
  submission in its own sandbox (nsjail, gVisor, Firecracker) and put `RUNNER_TOKEN` on the API.
- Problem titles and numbers refer to LeetCode; stories, tests and solutions here are original.
