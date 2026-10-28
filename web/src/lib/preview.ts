import type { Problem, Trace, TraceNode, V } from "./types";

/** A one-step trace built from a test's inputs, so the scene shows before any code runs. */
export function previewTrace(problem: Problem, testIndex: number): Trace {
  const test = problem.tests[testIndex] ?? problem.tests[0];
  const nodes: Record<string, TraceNode> = {};
  let addr = 0x1000;
  const newAddr = () => "0x" + (addr += 0x20).toString(16);

  const conv = (type: string, v: V): V => {
    const t = type.replace(/const\s+|&/g, "").replace(/\s+/g, "");
    if (t === "char") return { $c: v };
    if (t === "ListNode*") {
      const vals = (v ?? []) as number[];
      const addrs = vals.map(() => newAddr());
      vals.forEach((x, i) => (nodes[addrs[i]] = { val: x, next: addrs[i + 1] ?? null }));
      return addrs.length ? { $p: addrs[0] } : null;
    }
    if (t === "TreeNode*") {
      const vals = (v ?? []) as (number | null)[];
      if (!vals.length || vals[0] === null) return null;
      const root = newAddr();
      nodes[root] = { val: vals[0], left: null, right: null };
      const q = [root];
      let i = 1;
      while (q.length && i < vals.length) {
        const cur = q.shift()!;
        for (const side of ["left", "right"] as const) {
          if (i < vals.length && vals[i] !== null) {
            const a = newAddr();
            nodes[a] = { val: vals[i], left: null, right: null };
            nodes[cur][side] = a;
            q.push(a);
          }
          i++;
        }
      }
      return { $p: root };
    }
    const m = /^vector<(.+)>$/.exec(t);
    if (m && Array.isArray(v)) return v.map((x) => conv(m[1], x));
    return v;
  };

  const vars: Record<string, V> = {};
  problem.spec.params.forEach(([type, name], i) => (vars[name] = conv(type, test?.args[i])));
  return {
    steps: [{ line: 0, fn: problem.spec.method, stack: [{ fn: problem.spec.method, line: 0, vars }], nodes }],
    end: { kind: "preview" },
    truncated: false,
  };
}
