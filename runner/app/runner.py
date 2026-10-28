"""Compile a C++ solution, run it on tests, and trace one test with gdb."""

from __future__ import annotations

import json
import math
import os
import re
import resource
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from .harness import SpecError, build_main, parse_result

HERE = Path(__file__).resolve().parent
PRELUDE = HERE.parent / "cpp" / "prelude.h"
TRACER = HERE / "gdb_tracer.py"

CXX = os.environ.get("CXX", "g++")
GDB = os.environ.get("GDB", "gdb")
RUN_TIMEOUT = float(os.environ.get("RUN_TIMEOUT", "3"))
TRACE_TIMEOUT = float(os.environ.get("TRACE_TIMEOUT", "25"))
MAX_STEPS = int(os.environ.get("MAX_STEPS", "2500"))
MEM_BYTES = 512 * 1024 * 1024

ERR_RE = re.compile(r"^solution\.cpp:(\d+):(\d+):\s+(error|warning|note):\s+(.*)$")


def _limits():
    resource.setrlimit(resource.RLIMIT_AS, (MEM_BYTES, MEM_BYTES))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024 * 1024, 16 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    os.setsid()


def compile_program(work: Path, code: str, spec: dict, tests: list[dict]) -> dict:
    (work / "prelude.h").write_text(PRELUDE.read_text())
    (work / "solution.cpp").write_text(code)
    (work / "main.cpp").write_text(build_main(spec, tests))
    cmd = [
        CXX, "-std=c++17", "-O0", "-g", "-fno-omit-frame-pointer",
        "-D_GLIBCXX_ASSERTIONS", "-fdiagnostics-color=never",
        "-o", "prog", "main.cpp",
    ]
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=40)
    errors = []
    for line in proc.stderr.splitlines():
        m = ERR_RE.match(line)
        if m and m.group(3) == "error":
            errors.append({"line": int(m.group(1)), "col": int(m.group(2)), "message": m.group(4)})
    raw = proc.stderr
    if len(raw) > 6000:
        raw = raw[:6000] + "\n…"
    return {"ok": proc.returncode == 0, "errors": errors, "raw": raw, "ms": int((time.time() - t0) * 1000)}


def describe_failure(rc: int, stderr: str) -> str | None:
    if rc == 0:
        return None
    if "__n < this->size()" in stderr or "out of range" in stderr or "_GLIBCXX_ASSERTIONS" in stderr:
        return "Index out of range"
    if "Assertion" in stderr:
        return "Assertion failed: " + stderr.strip().splitlines()[-1][:160]
    if rc == -11 or rc == 139:
        return "Segmentation fault (null or invalid pointer)"
    if rc == -6 or rc == 134:
        return "Aborted"
    if rc == -8:
        return "Floating point exception (division by zero?)"
    if rc == -9:
        return "Killed (memory limit?)"
    return f"Exited with code {rc}"


def run_one(work: Path, i: int) -> dict:
    t0 = time.time()
    try:
        proc = subprocess.run(
            ["./prog", str(i)], cwd=work, capture_output=True, text=True,
            timeout=RUN_TIMEOUT, preexec_fn=_limits,
        )
    except subprocess.TimeoutExpired:
        return {"error": "Time limit exceeded", "stdout": "", "ms": int(RUN_TIMEOUT * 1000)}
    ms = int((time.time() - t0) * 1000)
    user_out, result = parse_result(proc.stdout)
    err = describe_failure(proc.returncode, proc.stderr)
    return {
        "output": result,
        "has_output": result is not None or "@@RESULT@@" in proc.stdout,
        "stdout": user_out[-4000:],
        "stderr": proc.stderr[-2000:],
        "error": err,
        "ms": ms,
    }


def _canon(x, deep: bool):
    if isinstance(x, list):
        items = [_canon(e, deep) for e in x] if deep else x
        return sorted(items, key=lambda e: json.dumps(e, sort_keys=True))
    return x


def equal(a, b, mode: str) -> bool:
    if mode == "float":
        try:
            return math.isclose(float(a), float(b), rel_tol=1e-5, abs_tol=1e-5)
        except (TypeError, ValueError):
            return False
    if mode == "unordered":
        return isinstance(a, list) and isinstance(b, list) and _canon(a, False) == _canon(b, False)
    if mode == "unordered-deep":
        if not (isinstance(a, list) and isinstance(b, list)):
            return False
        inner = lambda v: [sorted(e, key=lambda z: json.dumps(z)) if isinstance(e, list) else e for e in v]
        return _canon(inner(a), False) == _canon(inner(b), False)
    return a == b


def trace(work: Path, i: int, src_lines: int) -> dict:
    out = work / "trace.json"
    env = dict(os.environ, TRACE_OUT=str(out), SRC_LINES=str(src_lines), MAX_STEPS=str(MAX_STEPS))
    t0 = time.time()
    try:
        proc = subprocess.run(
            [GDB, "-q", "-nx", "-batch", "-x", str(TRACER), "--args", "./prog", str(i)],
            cwd=work, capture_output=True, text=True, timeout=TRACE_TIMEOUT, env=env,
        )
    except subprocess.TimeoutExpired:
        return {"steps": [], "end": {"kind": "timeout"}, "truncated": True}
    if not out.exists():
        return {"steps": [], "end": {"kind": "error", "message": proc.stderr[-800:]}, "truncated": False}
    data = json.loads(out.read_text())
    data["ms"] = int((time.time() - t0) * 1000)
    return data


def run_request(req: dict) -> dict:
    code: str = req["code"]
    spec: dict = req["spec"]
    tests: list[dict] = req["tests"]
    compare: str = req.get("compare", "exact")
    trace_index = req.get("trace")
    reference: str | None = req.get("reference")

    if len(code) > 40000:
        return {"fatal": "Code too long"}
    if not tests or len(tests) > 40:
        return {"fatal": "Need 1-40 tests"}

    work = Path(tempfile.mkdtemp(prefix="pt-"))
    try:
        try:
            comp = compile_program(work, code, spec, tests)
        except SpecError as e:
            return {"fatal": f"Bad test input: {e}"}
        if not comp["ok"]:
            return {"compile": comp, "results": [], "trace": None}

        expected = [t.get("expected") for t in tests]
        if reference and any("expected" not in t for t in tests):
            ref_dir = work / "ref"
            ref_dir.mkdir()
            rc = compile_program(ref_dir, reference, spec, tests)
            if rc["ok"]:
                for k, t in enumerate(tests):
                    if "expected" not in t:
                        expected[k] = run_one(ref_dir, k).get("output")

        results = []
        for k in range(len(tests)):
            r = run_one(work, k)
            r["i"] = k
            r["expected"] = expected[k]
            r["passed"] = r["error"] is None and r["has_output"] and equal(r["output"], expected[k], compare)
            results.append(r)

        tr = None
        if trace_index is not None and 0 <= int(trace_index) < len(tests):
            tr = trace(work, int(trace_index), code.count("\n") + 1)
            tr["test"] = int(trace_index)
        return {"compile": comp, "results": results, "trace": tr}
    finally:
        shutil.rmtree(work, ignore_errors=True)
