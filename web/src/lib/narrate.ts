import type { Trace, TraceFrame, TraceStep, V } from "./types";
import { isAlias, isPtr, isTyped, listOf, mapOf, pretty, sameValue, scalar, show } from "./values";

/** Short, plain-English captions for what changed between step i-1 and step i. */
export function narrate(trace: Trace, i: number): string[] {
  const cur = trace.steps[i];
  if (!cur) return [];
  if (trace.end.kind === "preview") return [];
  const prev = trace.steps[i - 1];
  const top = cur.stack[cur.stack.length - 1];

  if (cur.error) {
    const why = cur.error === "SIGSEGV" ? "a null or dangling pointer was used" : cur.error === "SIGABRT" ? "an index went out of range" : cur.error;
    return [`💥 Crash on line ${cur.line}: ${why}.`];
  }
  if (!prev) return [`▶ ${top.fn}(${argSummary(top, cur)}) starts.`];

  const out: string[] = [];
  if (cur.stack.length > prev.stack.length) {
    out.push(`📞 Calls ${top.fn}(${argSummary(top, cur)}) — depth ${cur.stack.length}.`);
  } else if (cur.stack.length < prev.stack.length) {
    const left = prev.stack[prev.stack.length - 1];
    out.push(`↩ ${left.fn} returns; back in ${top.fn}.`);
  }

  // Compare frames that exist in both steps at the same depth.
  const depth = Math.min(cur.stack.length, prev.stack.length);
  for (let d = depth - 1; d >= 0 && out.length < 4; d--) {
    const a = prev.stack[d];
    const b = cur.stack[d];
    if (a.fn !== b.fn) continue;
    for (const [name, v] of Object.entries(b.vars)) {
      if (out.length >= 4) break;
      if (isAlias(v)) continue;
      const before = a.vars[name];
      if (before === undefined) {
        if (d === cur.stack.length - 1) out.push(`✨ New ${name} = ${short(v, cur)}.`);
        continue;
      }
      if (isAlias(before) || sameValue(before, v)) continue;
      const msg = describeChange(name, before, v, prev, cur);
      if (msg) out.push(msg);
    }
  }

  // Linked structure edits (node.next / left / right rewired).
  for (const [addr, node] of Object.entries(cur.nodes)) {
    if (out.length >= 4) break;
    const old = prev.nodes[addr];
    if (!old) continue;
    for (const f of ["next", "left", "right"] as const) {
      if (f in node && node[f] !== old[f]) {
        const target = node[f] ? `node ${show(cur.nodes[node[f]!]?.val)}` : "null";
        out.push(`🔗 node ${show(node.val)}.${f} now points to ${target}.`);
      }
    }
  }

  if (!out.length) out.push(prev.line === cur.line ? `↻ Line ${cur.line} runs again.` : `→ Line ${cur.line}.`);
  return out.slice(0, 4);
}

function short(v: V, step: TraceStep): string {
  if (isPtr(v)) return step.nodes[v.$p] ? `→ node ${show(step.nodes[v.$p].val)}` : "pointer";
  const p = pretty(v);
  return p.length > 40 ? p.slice(0, 39) + "…" : p;
}

function argSummary(frame: TraceFrame, step: TraceStep): string {
  return Object.entries(frame.vars)
    .filter(([, v]) => scalar(v) !== undefined || isPtr(v) || v === null)
    .slice(0, 3)
    .map(([k, v]) => `${k}=${isPtr(v) ? show(step.nodes[v.$p]?.val) : show(v, 6)}`)
    .join(", ");
}

function describeChange(name: string, a: V, b: V, prev: TraceStep, cur: TraceStep): string | null {
  // scalars
  if (scalar(a) !== undefined && scalar(b) !== undefined) {
    const na = scalar(a);
    const nb = scalar(b);
    if (typeof na === "number" && typeof nb === "number") {
      if (nb === na + 1) return `➕ ${name}++ → ${show(nb)}.`;
      if (nb === na - 1) return `➖ ${name}-- → ${show(nb)}.`;
    }
    return `✏ ${name}: ${show(a)} → ${show(b)}.`;
  }
  // pointers
  if ((isPtr(a) || a === null) && (isPtr(b) || b === null)) {
    const where = b === null ? "null" : `node ${show(cur.nodes[b.$p]?.val)}`;
    return `👣 ${name} moves to ${where}.`;
  }
  // maps / sets
  const ma = mapOf(a);
  const mb = mapOf(b);
  if (ma && mb) {
    const ka = new Map(ma.map(([k, v]) => [JSON.stringify(k), v]));
    for (const [k, v] of mb) {
      const kk = JSON.stringify(k);
      if (!ka.has(kk)) return isTyped(b, "set") ? `🗄 ${pretty(k)} goes into ${name}.` : `🗄 ${name}[${pretty(k)}] = ${pretty(v)}.`;
      if (!sameValue(ka.get(kk), v)) return `🗄 ${name}[${pretty(k)}]: ${pretty(ka.get(kk))} → ${pretty(v)}.`;
    }
    if (mb.length < ma.length) return `🗑 ${name} drops a key (${mb.length} left).`;
    return null;
  }
  // sequences
  const la = listOf(a);
  const lb = listOf(b);
  if (la && lb) {
    const label = (x: V) => (isPtr(x) ? show(cur.nodes[x.$p]?.val ?? prev.nodes[x.$p]?.val) : pretty(x));
    if (lb.length === la.length + 1 && la.every((x, k) => sameValue(x, lb[k]))) {
      return isTyped(b, "queue") ? `🚶 ${label(lb[lb.length - 1])} joins the back of ${name}.` : `⬆ push ${label(lb[lb.length - 1])} onto ${name}.`;
    }
    if (lb.length === la.length - 1 && lb.every((x, k) => sameValue(x, la[k]))) return `⬇ pop ${label(la[la.length - 1])} off ${name}.`;
    if (lb.length === la.length - 1 && lb.every((x, k) => sameValue(x, la[k + 1]))) return `🚪 ${label(la[0])} leaves the front of ${name}.`;
    if (isTyped(b, "heap") && lb.length !== la.length) return lb.length > la.length ? `🔺 ${name} grows to ${lb.length}.` : `🔻 ${name} top removed (${lb.length} left).`;
    if (la.length === lb.length) {
      const diff: number[] = [];
      la.forEach((x, k) => !sameValue(x, lb[k]) && diff.push(k));
      if (diff.length === 2 && sameValue(la[diff[0]], lb[diff[1]]) && sameValue(la[diff[1]], lb[diff[0]])) {
        return `🔄 swap ${name}[${diff[0]}] ↔ ${name}[${diff[1]}].`;
      }
      if (diff.length === 1) {
        const k = diff[0];
        const inner = describeChange(`${name}[${k}]`, la[k], lb[k], prev, cur);
        return inner ?? `✏ ${name}[${k}] changes.`;
      }
      if (diff.length > 1) return `✏ ${diff.length} cells of ${name} change.`;
    }
    return `📦 ${name} now has ${lb.length} item${lb.length === 1 ? "" : "s"}.`;
  }
  return `✏ ${name} changes.`;
}

/** Steps whose top frame is on the given line, for "jump to when this line runs". */
export function stepsOnLine(trace: Trace, line: number): number[] {
  const out: number[] = [];
  trace.steps.forEach((s, i) => s.line === line && out.push(i));
  return out;
}

export function lineHits(trace: Trace): Map<number, number> {
  const m = new Map<number, number>();
  for (const s of trace.steps) m.set(s.line, (m.get(s.line) ?? 0) + 1);
  return m;
}

