import type { TraceStep, V } from "./types";

export const isChar = (v: V): boolean => !!v && typeof v === "object" && "$c" in v;
export const isPtr = (v: V): boolean => !!v && typeof v === "object" && "$p" in v;
export const isAlias = (v: V): boolean => !!v && typeof v === "object" && "$alias" in v;
export const isTyped = (v: V, t?: string): boolean =>
  !!v && typeof v === "object" && "$t" in v && (t === undefined || v.$t === t);

export function scalar(v: V): number | string | boolean | null | undefined {
  if (v === null || v === undefined) return v;
  if (typeof v === "number" || typeof v === "string" || typeof v === "boolean") return v;
  if (isChar(v)) return v.$c;
  return undefined;
}

export function asInt(v: V): number | null {
  const s = scalar(v);
  if (typeof s === "number" && Number.isFinite(s)) return Math.trunc(s);
  if (typeof s === "boolean") return s ? 1 : 0;
  return null;
}

/** Any sequence-like value as an array (vector, stack, queue, set, string chars). */
export function listOf(v: V): V[] | null {
  if (Array.isArray(v)) return v;
  if (typeof v === "string") return v.split("");
  if (isTyped(v) && v.$t !== "map") return v.items;
  return null;
}

export function mapOf(v: V): [V, V][] | null {
  if (isTyped(v, "map")) return v.items;
  if (isTyped(v, "set")) return v.items.map((k: V) => [k, undefined]);
  return null;
}

export function show(v: V, max = 6): string {
  if (v === null) return "null";
  if (v === undefined) return "—";
  if (typeof v === "boolean") return v ? "T" : "F";
  if (typeof v === "number") {
    if (v === 2147483647) return "INF";
    if (v === -2147483648) return "-INF";
    if (Number.isInteger(v)) {
      const s = String(v);
      if (s.length > max) return v > 0 ? "BIG" : "-BIG";
      return s;
    }
    return v.toFixed(2);
  }
  if (typeof v === "string") return v.length > max ? v.slice(0, max - 1) + "…" : v;
  if (isChar(v)) return v.$c === " " ? "␣" : v.$c;
  if (isPtr(v)) return "*" + String(v.$p).slice(-3);
  if (Array.isArray(v)) return "[" + v.length + "]";
  if (isTyped(v)) return v.$t + "(" + v.items.length + ")";
  if (v && typeof v === "object" && "$err" in v) return "?";
  return "{}";
}

/** Long-form text for the inspector panel. */
export function pretty(v: V, depth = 0): string {
  if (v === null) return "nullptr";
  if (v === undefined) return "—";
  if (typeof v === "string") return JSON.stringify(v);
  if (typeof v !== "object") return String(v);
  if (isChar(v)) return `'${v.$c}'`;
  if (isPtr(v)) return `→${String(v.$p).slice(-4)}`;
  if (isAlias(v)) return `(same as ${v.$alias})`;
  if ("$err" in v) return "<unreadable>";
  if (depth > 3) return "…";
  if (Array.isArray(v)) return "[" + v.map((x) => pretty(x, depth + 1)).join(", ") + "]";
  if (isTyped(v, "map")) return "{" + v.items.map(([k, x]: V[]) => `${pretty(k, depth + 1)}: ${pretty(x, depth + 1)}`).join(", ") + "}";
  if (isTyped(v)) return `${v.$t}[` + v.items.map((x: V) => pretty(x, depth + 1)).join(", ") + "]";
  if ("$s" in v) {
    const fields = Object.entries(v).filter(([k]) => k !== "$s");
    return "{" + fields.map(([k, x]) => `${k}: ${pretty(x, depth + 1)}`).join(", ") + "}";
  }
  return JSON.stringify(v);
}

function findRaw(step: TraceStep, name: string): V {
  for (let i = step.stack.length - 1; i >= 0; i--) {
    const vars = step.stack[i].vars;
    if (name in vars && !isAlias(vars[name])) return vars[name];
  }
  return undefined;
}

/**
 * Resolve a variable by name. "top" searches the innermost frame first (what the
 * running code sees); "outer" prefers the entry method's frame (stable structures).
 */
export function resolve(step: TraceStep | undefined, name: string, pref: "top" | "outer" = "top"): V {
  if (!step) return undefined;
  const order = step.stack.map((_, i) => i);
  if (pref === "top") order.reverse();
  for (const i of order) {
    const vars = step.stack[i].vars;
    if (name in vars) {
      const v = vars[name];
      if (isAlias(v)) return findRaw(step, v.$alias);
      return v;
    }
  }
  return undefined;
}

export function sameValue(a: V, b: V): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}
