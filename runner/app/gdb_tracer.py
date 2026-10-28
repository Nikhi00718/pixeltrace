"""gdb Python script: stops on every line of solution.cpp and records program state.

Run as: gdb -q -nx -batch -x gdb_tracer.py --args ./prog <test-index>
Env: TRACE_OUT (json path), SRC_LINES (line count of solution.cpp), MAX_STEPS.
"""

import itertools
import json
import os
import re

import gdb  # type: ignore

OUT = os.environ["TRACE_OUT"]
SRC_LINES = int(os.environ.get("SRC_LINES", "200"))
MAX_STEPS = int(os.environ.get("MAX_STEPS", "2500"))
MAX_ITEMS = 80
MAX_DEPTH = 5
MAX_NODES = 300
SRC = "solution.cpp"

events = {"stop": None, "exit": None}


def on_stop(ev):
    events["stop"] = ev


def on_exit(ev):
    events["exit"] = getattr(ev, "exit_code", None)


gdb.events.stop.connect(on_stop)
gdb.events.exited.connect(on_exit)

for cmd in (
    "set pagination off",
    "set confirm off",
    "set breakpoint pending off",
    "set print pretty off",
    "set disable-randomization off",
    "set startup-with-shell off",
):
    try:
        gdb.execute(cmd, to_string=True)
    except gdb.error:
        pass

# ---------------------------------------------------------------- values


def type_name(t):
    try:
        return str(t.strip_typedefs())
    except Exception:
        return str(t)


def is_node_type(t):
    try:
        t = t.strip_typedefs()
        if t.code != gdb.TYPE_CODE_STRUCT:
            return False
        names = {f.name for f in t.fields()}
    except Exception:
        return False
    return "val" in names and ("next" in names or "left" in names or "right" in names)


def register_nodes(ptr, nodes):
    stack = [ptr]
    while stack and len(nodes) < MAX_NODES:
        p = stack.pop()
        try:
            addr = int(p)
        except Exception:
            continue
        if addr == 0:
            continue
        key = hex(addr)
        if key in nodes:
            continue
        try:
            n = p.dereference()
            names = [f.name for f in n.type.strip_typedefs().fields()]
            entry = {"val": conv(n["val"], 1, nodes)}
            for fld in ("next", "left", "right", "random", "prev"):
                if fld in names:
                    c = n[fld]
                    ca = int(c)
                    entry[fld] = hex(ca) if ca else None
                    stack.append(c)
            nodes[key] = entry
        except gdb.MemoryError:
            nodes[key] = {"val": None, "bad": True}
        except Exception:
            nodes[key] = {"val": None, "bad": True}


def gstring(v):
    try:
        return v["_M_dataplus"]["_M_p"].string(length=min(int(v["_M_string_length"]), 2000))
    except Exception:
        pass
    vis = gdb.default_visualizer(v)
    if vis is not None:
        s = vis.to_string()
        if isinstance(s, gdb.LazyString):
            s = s.value()
        if isinstance(s, gdb.Value):
            return s.string()
        return str(s)
    return str(v)


KINDS = [
    ("std::__cxx11::basic_string", "string"),
    ("std::basic_string", "string"),
    ("std::vector", "list"),
    ("std::array", "list"),
    ("std::deque", "deque"),
    ("std::__cxx11::list", "list"),
    ("std::list", "list"),
    ("std::forward_list", "list"),
    ("std::stack", "stack"),
    ("std::queue", "queue"),
    ("std::priority_queue", "heap"),
    ("std::unordered_map", "map"),
    ("std::unordered_multimap", "map"),
    ("std::map", "map"),
    ("std::multimap", "map"),
    ("std::unordered_set", "set"),
    ("std::unordered_multiset", "set"),
    ("std::set", "set"),
    ("std::multiset", "set"),
    ("std::pair", "pair"),
    ("std::tuple", "tuple"),
]


def kind_of(name):
    for prefix, kind in KINDS:
        if name.startswith(prefix + "<") or name == prefix:
            return kind
    return None


def children(v):
    vis = gdb.default_visualizer(v)
    if vis is None or not hasattr(vis, "children"):
        return None, None
    hint = vis.display_hint() if hasattr(vis, "display_hint") else None
    items = list(itertools.islice(vis.children(), MAX_ITEMS * 2 + 1))
    return hint, [c[1] for c in items]


def conv(v, depth=0, nodes=None):
    if not isinstance(v, gdb.Value):
        return v
    try:
        t = v.type
        if t.code in (gdb.TYPE_CODE_REF, getattr(gdb, "TYPE_CODE_RVALUE_REF", -1)):
            v = v.referenced_value()
            t = v.type
        st = t.strip_typedefs()
        code = st.code
        if code == gdb.TYPE_CODE_BOOL:
            return bool(v)
        if code == gdb.TYPE_CODE_INT:
            n = int(v)
            if st.sizeof == 1 and "char" in type_name(st):
                return {"$c": chr(n & 0xFF)}
            return n
        if code == gdb.TYPE_CODE_CHAR:
            return {"$c": chr(int(v) & 0xFF)}
        if code == gdb.TYPE_CODE_FLT:
            f = float(v)
            return f if f == f and abs(f) != float("inf") else None
        if code == gdb.TYPE_CODE_ENUM:
            return int(v)
        if code == gdb.TYPE_CODE_PTR:
            addr = int(v)
            if addr == 0:
                return None
            target = st.target()
            if is_node_type(target) and nodes is not None:
                register_nodes(v, nodes)
                return {"$p": hex(addr)}
            return {"$p": hex(addr), "raw": True}
        if depth >= MAX_DEPTH:
            return "…"
        if code == gdb.TYPE_CODE_ARRAY:
            lo, hi = st.range()
            return [conv(v[i], depth + 1, nodes) for i in range(lo, min(hi, lo + MAX_ITEMS - 1) + 1)]
        if code in (gdb.TYPE_CODE_STRUCT, gdb.TYPE_CODE_UNION):
            name = type_name(st)
            kind = kind_of(name)
            if kind == "string":
                return gstring(v)
            if kind == "pair":
                return [conv(v["first"], depth + 1, nodes), conv(v["second"], depth + 1, nodes)]
            if kind is not None:
                hint, items = children(v)
                if items is None:
                    return {"$t": kind, "items": []}
                if hint == "map" or kind == "map":
                    pairs = [
                        [conv(items[i], depth + 1, nodes), conv(items[i + 1], depth + 1, nodes)]
                        for i in range(0, len(items) - 1, 2)
                    ][:MAX_ITEMS]
                    return {"$t": "map", "items": pairs}
                vals = [conv(x, depth + 1, nodes) for x in items[:MAX_ITEMS]]
                if kind == "list":
                    return vals
                if kind == "tuple":
                    return vals
                return {"$t": kind, "items": vals}
            if is_node_type(st):
                return {"$s": name, "val": conv(v["val"], depth + 1, nodes)}
            out = {"$s": name}
            for f in st.fields():
                if f.artificial or not f.name or f.name.startswith("_vptr"):
                    continue
                if getattr(f, "is_base_class", False):
                    continue
                try:
                    out[f.name] = conv(v[f.name], depth + 1, nodes)
                except Exception:
                    pass
            return out
        return str(v)
    except gdb.MemoryError:
        return {"$err": "bad memory"}
    except Exception as e:  # noqa: BLE001
        return {"$err": str(e)[:60]}


# ---------------------------------------------------------------- frames


def in_src(frame):
    try:
        sal = frame.find_sal()
        return sal.symtab is not None and sal.symtab.filename.endswith(SRC)
    except Exception:
        return False


def fn_name(frame):
    try:
        f = frame.function()
        name = f.name if f else frame.name()
    except Exception:
        name = frame.name() or "?"
    name = (name or "?").split("(")[0]
    return re.sub(r"^Solution::", "", name)


def scalar(x):
    return x is None or isinstance(x, (int, float, bool, str)) or (isinstance(x, dict) and "$c" in x)


def frame_vars(frame, line, nodes, full, seen_addr, decl_ready):
    out = {}
    try:
        block = frame.block()
    except RuntimeError:
        return out
    while block is not None:
        for sym in block:
            if not (sym.is_variable or sym.is_argument):
                continue
            if sym.name in out or sym.name.startswith("__"):
                continue
            # gdb stops before a line runs, so a local declared on this line is uninitialised
            # until the line has run once in this call (one-line loops revisit it)
            if not sym.is_argument and (sym.line > line or (sym.line == line and not decl_ready)):
                continue
            try:
                val = sym.value(frame)
            except Exception:
                continue
            if sym.name == "this":
                try:
                    obj = val.dereference()
                    for f in obj.type.strip_typedefs().fields():
                        if f.name and not f.artificial and f.name not in out:
                            out[f.name] = conv(obj[f.name], 0, nodes)
                except Exception:
                    pass
                continue
            addr = None
            try:
                if val.type.code == gdb.TYPE_CODE_REF:
                    addr = int(val.referenced_value().address)
            except Exception:
                addr = None
            if addr is not None and addr in seen_addr:
                out[sym.name] = {"$alias": seen_addr[addr]}
                continue
            c = conv(val, 0, nodes)
            if not full and not scalar(c):
                continue
            out[sym.name] = c
            try:
                a = addr if addr is not None else int(val.address)
                seen_addr.setdefault(a, sym.name)
            except Exception:
                pass
        if block.function is not None:
            break
        block = block.superblock
    return out


# Per call (depth, frame base): pcs already stopped at, lines already finished, and the last line.
calls = {}
prev_depth = [0]


def frame_key(frame, depth):
    try:
        return (depth, int(frame.read_register("rbp")))
    except Exception:
        return (depth, 0)


def snapshot():
    try:
        frame = gdb.newest_frame()
    except gdb.error:
        return None
    frames = []
    while frame is not None:
        if in_src(frame):
            frames.append(frame)
        try:
            frame = frame.older()
        except gdb.error:
            break
    if not frames:
        return None
    frames.reverse()  # outermost first
    nodes = {}
    seen_addr = {}
    stack = []
    last = len(frames) - 1
    for i, f in enumerate(frames):
        line = f.find_sal().line
        full = i == 0 or i == last
        ready = False
        if i == last:
            key = frame_key(f, i)
            if len(frames) > prev_depth[0] or key not in calls:
                calls[key] = {"pcs": set(), "done": set(), "last": None}
            c = calls[key]
            pc = f.pc()
            if c["last"] is not None and c["last"] != line:
                c["done"].add(c["last"])
            # a declaration on this line has fully run once we left the line, or looped back to a pc
            ready = line in c["done"] or pc in c["pcs"]
            c["pcs"].add(pc)
            c["last"] = line
        stack.append({"fn": fn_name(f), "line": line, "vars": frame_vars(f, line, nodes, full, seen_addr, ready)})
    prev_depth[0] = len(frames)
    return {"line": stack[-1]["line"], "fn": stack[-1]["fn"], "stack": stack, "nodes": nodes}


# ---------------------------------------------------------------- main loop


JUMP_RE = re.compile(r"(?<![a-z])j[a-z]+\s+(0x[0-9a-f]+)")


def is_entry(pc):
    """Function entry points: arguments are not stored yet before the prologue runs."""
    try:
        blk = gdb.block_for_pc(pc)
        while blk is not None and blk.function is None:
            blk = blk.superblock
        return blk is not None and blk.start == pc
    except RuntimeError:
        return False


def set_breakpoints():
    """Break on every line-table address of the solution, plus the back-edge target of any loop that
    lives inside a single line (gcc gives those no rows of their own). Needs a non-PIE binary and a
    started inferior (for the disassembler)."""
    table = None
    for n in range(1, SRC_LINES + 1):
        try:
            for sal in gdb.decode_line(f"{SRC}:{n}")[1] or []:
                if sal.symtab is not None and sal.symtab.filename.endswith(SRC):
                    table = sal.symtab.linetable()
                    break
        except gdb.error:
            continue
        if table is not None:
            break
    if table is None:
        for n in range(1, SRC_LINES + 1):
            try:
                gdb.execute(f"break {SRC}:{n}", to_string=True)
            except gdb.error:
                pass
        return
    rows = sorted({(e.pc, e.line) for e in table if e.pc and 0 < e.line <= SRC_LINES})
    pcs = set()
    arch = gdb.selected_inferior().architecture()
    first = {}  # (function start, line) -> lowest pc; later rows of a line are cleanup/epilogue paths
    for pc, line in rows:
        try:
            blk = gdb.block_for_pc(pc)
            while blk is not None and blk.function is None:
                blk = blk.superblock
            fn = blk.start if blk is not None else 0
        except RuntimeError:
            fn = 0
        first.setdefault((fn, line), pc)
    keep = set(first.values())
    for k, (pc, line) in enumerate(rows):
        if is_entry(pc):
            continue
        if pc in keep:
            pcs.add(pc)
        end = rows[k + 1][0] if k + 1 < len(rows) else pc
        if end - pc <= 4 or end - pc > 600:
            continue
        try:
            for insn in arch.disassemble(pc, end - 1):
                m = JUMP_RE.search(insn["asm"])
                if m:
                    target = int(m.group(1), 16)
                    if pc <= target < insn["addr"]:
                        pcs.add(target)
        except gdb.error:
            pass
    for pc in sorted(pcs):
        try:
            gdb.execute(f"break *{pc:#x}", to_string=True)
        except gdb.error:
            pass


def main():
    steps = []
    end = {"kind": "exit", "code": None}
    truncated = False
    try:
        gdb.execute("starti", to_string=True)
        set_breakpoints()
        events["stop"] = None
        gdb.execute("continue", to_string=True)
    except gdb.error as e:
        end = {"kind": "error", "message": str(e)}

    while True:
        if events["exit"] is not None or gdb.selected_inferior().pid == 0:
            end = {"kind": "exit", "code": events["exit"]}
            break
        ev = events["stop"]
        snap = snapshot()
        if isinstance(ev, gdb.SignalEvent):
            end = {"kind": "signal", "signal": ev.stop_signal}
            if snap:
                snap["error"] = ev.stop_signal
                steps.append(snap)
            break
        if snap:
            if not steps or steps[-1]["line"] != snap["line"] or steps[-1]["stack"] != snap["stack"]:
                steps.append(snap)
        if len(steps) >= MAX_STEPS:
            truncated = True
            end = {"kind": "limit"}
            break
        events["stop"] = None
        try:
            gdb.execute("continue", to_string=True)
        except gdb.error as e:
            end = {"kind": "error", "message": str(e)}
            break

    with open(OUT, "w") as fh:
        json.dump({"steps": steps, "end": end, "truncated": truncated}, fh, separators=(",", ":"))
    try:
        gdb.execute("kill", to_string=True)
    except gdb.error:
        pass


main()
