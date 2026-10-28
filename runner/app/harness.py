"""Builds main.cpp: turns JSON test arguments into C++ literals and calls Solution."""

from __future__ import annotations

import json
import re

INT_TYPES = {
    "int", "long", "long long", "unsigned", "unsigned int", "size_t",
    "unsigned long", "unsigned long long", "int64_t", "uint32_t", "uint64_t", "short",
}
FLOAT_TYPES = {"double", "float", "long double"}


class SpecError(ValueError):
    pass


def norm_type(t: str) -> str:
    t = t.replace("const ", "").replace("&", "").strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\s*([<>,*])\s*", r"\1", t)
    return t.replace(">>", "> >").replace("> >", ">>")


def split_template(t: str) -> tuple[str, list[str]]:
    """'vector<pair<int,int>>' -> ('vector', ['pair<int,int>'])."""
    i = t.find("<")
    if i < 0:
        return t, []
    head, body = t[:i], t[i + 1:-1]
    args, depth, cur = [], 0, ""
    for ch in body:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        if ch == "," and depth == 0:
            args.append(cur)
            cur = ""
        else:
            cur += ch
    args.append(cur)
    return head, [a.strip() for a in args]


def c_string(s: str) -> str:
    out = []
    for ch in s:
        if ch in '"\\':
            out.append("\\" + ch)
        elif ch == "\n":
            out.append("\\n")
        elif ord(ch) < 0x20 or ord(ch) > 0x7E:
            out.append("\\x%02x" % (ord(ch) & 0xFF))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def c_char(c: str) -> str:
    if len(c) != 1:
        raise SpecError(f"expected a single character, got {c!r}")
    if c in "'\\":
        return "'\\" + c + "'"
    return "'" + c + "'"


def literal(t: str, v) -> str:
    t = norm_type(t)
    if t in INT_TYPES:
        if isinstance(v, bool) or not isinstance(v, int):
            raise SpecError(f"expected an integer for {t}, got {v!r}")
        if t in ("long long", "int64_t", "long") or abs(v) > 2**31:
            return f"{v}LL"
        return str(v)
    if t in FLOAT_TYPES:
        return repr(float(v))
    if t == "bool":
        return "true" if v else "false"
    if t == "char":
        return c_char(v)
    if t == "string":
        if not isinstance(v, str):
            raise SpecError(f"expected a string, got {v!r}")
        return f"string({c_string(v)})"
    if t == "ListNode*":
        return f"pt_io::mkList({literal('vector<int>', v or [])})"
    if t == "TreeNode*":
        vals = ["pt_io::NUL" if x is None else str(int(x)) for x in (v or [])]
        return "pt_io::mkTree({" + ",".join(vals) + "})"
    head, args = split_template(t)
    if head == "vector" and args:
        if not isinstance(v, list):
            raise SpecError(f"expected a list for {t}, got {v!r}")
        return f"{t}{{" + ",".join(literal(args[0], x) for x in v) + "}"
    if head == "pair" and len(args) == 2:
        return f"{t}{{{literal(args[0], v[0])},{literal(args[1], v[1])}}}"
    raise SpecError(f"unsupported parameter type: {t}")


def build_main(spec: dict, tests: list[dict]) -> str:
    method = spec["method"]
    params = spec["params"]
    output = spec.get("output", "return")
    ret = norm_type(spec.get("ret", "void"))
    if not re.fullmatch(r"[A-Za-z_]\w*", method):
        raise SpecError("bad method name")

    cases = []
    for i, test in enumerate(tests):
        args = test["args"]
        if len(args) != len(params):
            raise SpecError(f"test {i}: expected {len(params)} args, got {len(args)}")
        lines = []
        for k, ((ptype, _pname), val) in enumerate(zip(params, args)):
            lines.append(f"    {norm_type(ptype)} a{k} = {literal(ptype, val)};")
        call = f"sol.{method}({', '.join(f'a{k}' for k in range(len(params)))})"
        if output == "return":
            if ret == "void":
                raise SpecError("void method needs output: param:N")
            lines.append(f"    auto r = {call};")
            lines.append("    pt_io::emit(r);")
        else:
            m = re.fullmatch(r"param:(\d+)", output)
            if not m or int(m.group(1)) >= len(params):
                raise SpecError(f"bad output spec {output!r}")
            lines.append(f"    {call};")
            lines.append(f"    pt_io::emit(a{m.group(1)});")
        cases.append(f"  case {i}: {{\n    Solution sol;\n" + "\n".join(lines) + "\n    break;\n  }")

    return (
        '#include "prelude.h"\n'
        '#include "solution.cpp"\n'
        "int main(int argc, char** argv) {\n"
        "  int t = argc > 1 ? atoi(argv[1]) : 0;\n"
        "  switch (t) {\n" + "\n".join(cases) + "\n  default: return 3;\n  }\n"
        "  return 0;\n}\n"
    )


def starter_code(spec: dict) -> str:
    params = ", ".join(f"{t} {n}" for t, n in spec["params"])
    return (
        "class Solution {\npublic:\n"
        f"    {spec.get('ret', 'void')} {spec['method']}({params}) {{\n        \n    }}\n}};\n"
    )


def parse_result(stdout: str):
    """Return (user_stdout, parsed_result or None)."""
    marker = "\n@@RESULT@@"
    idx = stdout.rfind(marker)
    if idx < 0:
        return stdout, None
    user = stdout[:idx]
    raw = stdout[idx + len(marker):].strip()
    try:
        return user, json.loads(raw)
    except json.JSONDecodeError:
        return user, None
