import type { LayerDef, Trace, TraceStep, V } from "@/lib/types";
import { asInt, isPtr, isTyped, listOf, mapOf, pretty, resolve, scalar, show } from "@/lib/values";

export interface Ent {
  id: string;
  kind: string;
  x: number;
  y: number;
  w?: number;
  h?: number;
  text?: string;
  sub?: string;
  color?: string;
  z?: number;
  glow?: number;
  from?: string;
  to?: string;
  fall?: boolean;
  align?: "left" | "center";
  directed?: boolean;
  /** stacked name tags go under the feet instead of above the head */
  below?: boolean;
  /** hover text: which variable this sprite is and its value */
  tip?: string;
}

export interface LayerCtx {
  trace: Trace;
  x: number;
  y: number;
  width: number;
  color: (name: string) => string;
}

export interface Layer {
  height: number;
  build(i: number): Ent[];
}

type Maker = (def: LayerDef, ctx: LayerCtx) => Layer;

const LABEL_H = 11;
const clamp = (v: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, v));
const key = (v: V) => JSON.stringify(v);

function header(def: LayerDef, ctx: LayerCtx, fallback: string): Ent {
  return {
    id: `hdr:${def.kind}:${def.var ?? fallback}:${ctx.y}`,
    kind: "label",
    x: ctx.x + 3,
    y: ctx.y + 6,
    text: (def.label ?? fallback).toUpperCase(),
    align: "left",
    z: 9,
  };
}

function compact(v: V, max = 8, step?: TraceStep): string {
  if (step && isPtr(v) && step.nodes[v.$p]) return show(step.nodes[v.$p].val, max);
  const l = listOf(v);
  if (l && !isTyped(v, "map")) {
    const s = l.map((x) => (step && isPtr(x) && step.nodes[x.$p] ? show(step.nodes[x.$p].val, 4) : show(x, 4))).join(",");
    return s.length > max ? s.slice(0, max - 1) + "…" : s;
  }
  return show(v, max);
}

/** Stable sprite ids across steps so moved values glide instead of popping. */
export function trackIds(seqs: (V[] | null)[], mode: "match" | "stack" | "queue", prefix: string): (string[] | null)[] {
  let counter = 0;
  let prevKeys: string[] | null = null;
  let prevIds: string[] = [];
  const fresh = () => `${prefix}#${counter++}`;
  return seqs.map((seq) => {
    if (!seq) {
      prevKeys = null;
      return null;
    }
    const keys = seq.map(key);
    let ids: string[];
    if (!prevKeys) {
      ids = keys.map(fresh);
    } else if (mode === "stack") {
      let m = 0;
      while (m < keys.length && m < prevKeys.length && keys[m] === prevKeys[m]) m++;
      ids = keys.map((_, i) => (i < m ? prevIds[i] : fresh()));
    } else if (mode === "queue") {
      let k = 0;
      const pk = prevKeys;
      for (; k <= pk.length; k++) {
        const rest = pk.slice(k);
        if (rest.length <= keys.length && rest.every((x, j) => x === keys[j])) break;
      }
      const kept = prevIds.slice(k);
      ids = keys.map((_, i) => (i < kept.length ? kept[i] : fresh()));
    } else {
      ids = new Array(keys.length);
      const pool = new Map<string, string[]>();
      const pk = prevKeys;
      for (let i = 0; i < pk.length; i++) {
        if (i < keys.length && keys[i] === pk[i]) ids[i] = prevIds[i];
        else {
          const arr = pool.get(pk[i]) ?? [];
          arr.push(prevIds[i]);
          pool.set(pk[i], arr);
        }
      }
      for (let i = 0; i < keys.length; i++) {
        if (ids[i]) continue;
        const arr = pool.get(keys[i]);
        ids[i] = arr && arr.length ? arr.shift()! : fresh();
      }
    }
    prevKeys = keys;
    prevIds = ids;
    return ids;
  });
}

function pointerHeroes(
  names: string[],
  step: TraceStep,
  ctx: LayerCtx,
  place: (name: string, value: number) => { x: number; y: number; fall?: boolean } | null,
  idPrefix: string,
): Ent[] {
  const out: Ent[] = [];
  const stackCount = new Map<string, number>();
  for (const name of names) {
    const v = asInt(resolve(step, name, "top"));
    if (v === null) continue;
    const p = place(name, v);
    if (!p) continue;
    const slot = `${Math.round(p.x)}:${Math.round(p.y)}`;
    const n = stackCount.get(slot) ?? 0;
    stackCount.set(slot, n + 1);
    out.push({
      id: `${idPrefix}:ptr:${name}`,
      kind: "hero",
      x: p.x + n * 6 - (n ? 3 : 0),
      y: p.y,
      text: name,
      sub: String(v),
      color: ctx.color(name),
      fall: p.fall,
      tip: `${name} = ${v}${p.fall ? " (out of range!)" : ""}`,
      z: 8 + n * 0.01,
      h: n,
    });
  }
  return out;
}

// ---------------------------------------------------------------- array / string / bars

const arrayLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const name = def.var ?? "";
  const from = def.from ?? "top";
  const style = def.style ?? "crates";
  const seqs = steps.map((s) => {
    const l = listOf(resolve(s, name, from));
    return l ? l.slice(0, 64) : null;
  });
  const ids = trackIds(seqs, "match", `a:${name}`);
  const maxLen = Math.max(1, ...seqs.map((s) => (s ? s.length : 0)));
  const cs = clamp(Math.floor((ctx.width - 16) / maxLen), 8, style === "bars" ? 20 : 24);
  const pointers = (def.pointers ?? []) as string[];
  let maxVal = 1;
  if (style === "bars") for (const s of seqs) for (const v of s ?? []) maxVal = Math.max(maxVal, asInt(v) ?? 0);
  const barH = 56;
  const bodyH = style === "bars" ? barH + 10 : cs;
  const ptrH = pointers.length ? (pointers.length > 1 ? 40 : 30) : 4;
  const height = LABEL_H + bodyH + 8 + ptrH;
  const x0 = ctx.x + Math.max(8, Math.floor((ctx.width - cs * maxLen) / 2));
  const bodyY = ctx.y + LABEL_H + 2;

  // Water for trapping-rain style scenes: trapped level per index, revealed as pointers sweep.
  let level: number[] | null = null;
  if (def.water) {
    const first = seqs.find((s) => s && s.length) ?? [];
    const h = first.map((v) => asInt(v) ?? 0);
    const lm: number[] = [];
    const rm: number[] = [];
    h.forEach((v, i) => (lm[i] = Math.max(v, i ? lm[i - 1] : 0)));
    for (let i = h.length - 1; i >= 0; i--) rm[i] = Math.max(h[i], i < h.length - 1 ? rm[i + 1] : 0);
    level = h.map((v, i) => Math.min(lm[i], rm[i]) - v);
  }

  return {
    height,
    build(i) {
      const step = steps[i];
      const seq = seqs[i];
      const out: Ent[] = [header(def, ctx, name)];
      if (!seq) return out;
      const sid = ids[i]!;
      const ground = bodyY + bodyH;
      seq.forEach((v, k) => {
        const x = x0 + k * cs;
        const label = show(v, 5);
        const tip = `${name}[${k}] = ${pretty(v)}`;
        if (style === "bars") {
          const hv = Math.round(((asInt(v) ?? 0) / maxVal) * barH);
          out.push({ id: sid[k], kind: "bar", x: x + 1, y: ground, w: cs - 2, h: hv, text: label, z: 5, tip });
        } else if (style === "letters" || style === "tiles") {
          out.push({ id: sid[k], kind: "tile", x, y: bodyY, w: cs - 1, h: cs, text: label, color: style === "letters" ? "#f5ebd7" : "#dfe7fd", z: 5, tip });
        } else {
          out.push({ id: sid[k], kind: "crate", x, y: bodyY, w: cs - 1, h: cs, text: label, z: 5, tip });
        }
        if (cs >= 12) out.push({ id: `${name}:idx:${k}`, kind: "tiny", x: x + cs / 2, y: ground + 3, text: String(k), z: 4 });
      });
      if (level && def.water) {
        const [ln, rn] = def.water as [string, string];
        const l = asInt(resolve(step, ln));
        const r = rn ? asInt(resolve(step, rn)) : null;
        level.forEach((lv, k) => {
          const done = l !== null && (k < l || (r !== null && k > r));
          if (!done || lv <= 0) return;
          out.push({ id: `${name}:water:${k}`, kind: "water", x: x0 + k * cs, y: ground - Math.round(((asInt(seq[k]) ?? 0) / maxVal) * barH), w: cs, h: Math.round((lv / maxVal) * barH), z: 4 });
        });
      }
      if (def.window) {
        const [a, b] = def.window;
        const lo = asInt(resolve(step, a));
        let hi = asInt(resolve(step, b));
        if (hi !== null && def.windowExclusive) hi -= 1;
        if (lo !== null && hi !== null && hi >= lo && lo < seq.length) {
          const top = style === "bars" ? bodyY : bodyY - 2;
          out.push({ id: `${name}:win`, kind: "spot", x: x0 + lo * cs - 1, y: top, w: (Math.min(hi, seq.length - 1) - lo + 1) * cs + 1, h: bodyH + 4, z: 6 });
        }
      }
      const feet = ground + 26;
      out.push(
        ...pointerHeroes(pointers, step, ctx, (_n, v) => {
          const inRange = v >= 0 && v <= seq.length;
          const vv = clamp(v, -1, seq.length);
          return { x: x0 + vv * cs + cs / 2, y: feet, fall: !inRange };
        }, `arr:${name}`).map((e) => ({ ...e, below: true })),
      );
      return out;
    },
  };
};

// ---------------------------------------------------------------- grid

const PALETTES: Record<string, (v: V, max: number) => [string, string, string?]> = {
  islands: (v) => {
    const s = String(scalar(v));
    if (s === "1") return ["#5a9e4b", ""];
    if (s === "0") return ["#3a7bd5", ""];
    return ["#e9d8a6", ""];
  },
  oranges: (v) => {
    const n = asInt(v);
    if (n === 1) return ["#f7a325", "o"];
    if (n === 2) return ["#6b8e23", "x"];
    return ["#cfd8dc", ""];
  },
  maze: (v) => (asInt(v) === 1 ? ["#4a4458", ""] : ["#e8e1d0", ""]),
  dp: (v, max) => {
    const n = asInt(v);
    if (n === null) return ["#eeeeee", show(v, 4)];
    const k = max > 0 ? clamp(n / max, 0, 1) : 0;
    const g = Math.round(248 - k * 90);
    const b = Math.round(225 - k * 130);
    return [`rgb(255,${g},${b})`, show(v, 4)];
  },
  board: (v) => {
    const s = String(scalar(v) ?? "");
    if (s === "." || s === "") return ["#f5ebd7", ""];
    if (s === "#") return ["#e9d8a6", ""];
    return ["#f5ebd7", s];
  },
  bool: (v) => (scalar(v) ? ["#ffd166", ""] : ["#e8e1d0", ""]),
};

const gridLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const name = def.var ?? "";
  const from = def.from ?? "outer";
  const grids = steps.map((s) => {
    const rows = listOf(resolve(s, name, from));
    if (!rows) return null;
    const g = rows.slice(0, 30).map((r) => (listOf(r) ?? [r]).slice(0, 40));
    return g;
  });
  const rows = Math.max(1, ...grids.map((g) => (g ? g.length : 0)));
  const cols = Math.max(1, ...grids.map((g) => (g ? Math.max(0, ...g.map((r) => r.length)) : 0)));
  const cs = clamp(Math.min(Math.floor((ctx.width - 16) / cols), Math.floor(170 / rows)), 6, 18);
  let max = 0;
  for (const g of grids) for (const r of g ?? []) for (const v of r) max = Math.max(max, asInt(v) ?? 0);
  const pal = PALETTES[def.palette ?? "dp"] ?? PALETTES.dp;
  const x0 = ctx.x + Math.floor((ctx.width - cols * cs) / 2);
  const y0 = ctx.y + LABEL_H + 2;
  const pairs = (def.pointers ?? []).filter(Array.isArray) as [string, string][];
  return {
    height: LABEL_H + rows * cs + 6,
    build(i) {
      const g = grids[i];
      const out: Ent[] = [header(def, ctx, name)];
      if (!g) return out;
      g.forEach((row, r) =>
        row.forEach((v, c) => {
          const [fill, label] = pal(v, max);
          out.push({ id: `${name}:${r}:${c}`, kind: "tile", x: x0 + c * cs, y: y0 + r * cs, w: cs, h: cs, color: fill, text: cs >= 9 ? label : "", z: 5, tip: `${name}[${r}][${c}] = ${pretty(v)}` });
        }),
      );
      const step = steps[i];
      pairs.forEach(([rn, cn]) => {
        const r = asInt(resolve(step, rn));
        const c = asInt(resolve(step, cn));
        if (r === null || c === null) return;
        const fall = r < 0 || c < 0 || r >= g.length || c >= (g[0]?.length ?? 0);
        const rr = clamp(r, -1, g.length);
        const cc = clamp(c, -1, g[0]?.length ?? 0);
        out.push({
          id: `${name}:ptr:${rn}${cn}`,
          kind: "hero",
          x: x0 + cc * cs + cs / 2,
          y: y0 + rr * cs + cs - 1,
          text: `${rn},${cn}`,
          sub: `${r},${c}`,
          tip: `${rn} = ${r}, ${cn} = ${c}${fall ? " (off the map!)" : ""}`,
          color: ctx.color(rn),
          fall,
          z: 8,
        });
      });
      return out;
    },
  };
};

// ---------------------------------------------------------------- map / set

const mapLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const name = def.var ?? "";
  const from = def.from ?? "top";
  const maps = steps.map((s) => mapOf(resolve(s, name, from)));
  const order: string[] = [];
  const seen = new Set<string>();
  for (const m of maps) for (const [k] of m ?? []) {
    const kk = key(k);
    if (!seen.has(kk) && order.length < 60) {
      seen.add(kk);
      order.push(kk);
    }
  }
  const lw = 30;
  const lh = 24;
  const perRow = Math.max(1, Math.floor((ctx.width - 12) / (lw + 3)));
  const rows = Math.max(1, Math.ceil(order.length / perRow));
  const lookups = (def.lookup ?? []) as string[];
  const x0 = ctx.x + 6;
  const y0 = ctx.y + LABEL_H + 2;
  return {
    height: LABEL_H + rows * (lh + 3) + 4,
    build(i) {
      const m = maps[i];
      const out: Ent[] = [header(def, ctx, name)];
      if (!m) return out;
      const step = steps[i];
      const look = new Set(lookups.map((n) => key(resolve(step, n))).filter((x) => x !== undefined));
      if (!m.length) out.push({ id: `${name}:empty`, kind: "tiny", x: x0 + 20, y: y0 + 10, text: "(empty)", z: 5 });
      for (const [k, v] of m) {
        const kk = key(k);
        const idx = order.indexOf(kk);
        if (idx < 0) continue;
        out.push({
          id: `${name}:k:${kk}`,
          kind: "locker",
          x: x0 + (idx % perRow) * (lw + 3),
          y: y0 + Math.floor(idx / perRow) * (lh + 3),
          w: lw,
          h: lh,
          text: show(k, 6),
          sub: v === undefined ? "" : compact(v, 6, step),
          glow: look.has(kk) ? 1 : 0,
          z: 5,
          tip: v === undefined ? `${name} contains ${pretty(k)}` : `${name}[${pretty(k)}] = ${pretty(v)}`,
        });
      }
      return out;
    },
  };
};

// ---------------------------------------------------------------- stack / queue / heap

const stackLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const name = def.var ?? "";
  const from = def.from ?? "top";
  const seqs = steps.map((s) => listOf(resolve(s, name, from)));
  const ids = trackIds(seqs, "stack", `s:${name}`);
  const cap = 12;
  const maxSize = clamp(Math.max(1, ...seqs.map((s) => (s ? s.length : 0))), 1, cap);
  const bh = 11;
  const bw = Math.min(46, ctx.width - 30);
  const x0 = ctx.x + Math.floor((ctx.width - bw) / 2);
  const bottom = ctx.y + LABEL_H + maxSize * bh + 4;
  return {
    height: LABEL_H + maxSize * bh + 10,
    build(i) {
      const seq = seqs[i];
      const out: Ent[] = [header(def, ctx, name)];
      out.push({ id: `${name}:base`, kind: "ground", x: x0 - 6, y: bottom, w: bw + 12, h: 2, z: 4 });
      if (!seq) return out;
      const sid = ids[i]!;
      const startIdx = Math.max(0, seq.length - cap);
      for (let k = startIdx; k < seq.length; k++) {
        const level = k - startIdx;
        out.push({ id: sid[k], kind: "block", x: x0, y: bottom - (level + 1) * bh, w: bw, h: bh, text: compact(seq[k], 7, steps[i]), color: def.color, z: 5, tip: `${name} ${k === seq.length - 1 ? "top" : `#${k}`}: ${pretty(seq[k])}` });
      }
      if (seq.length) out.push({ id: `${name}:top`, kind: "tiny", x: x0 - 12, y: bottom - (seq.length - startIdx) * bh + 5, text: "top", z: 6 });
      if (startIdx > 0) out.push({ id: `${name}:more`, kind: "tiny", x: x0 + bw + 12, y: bottom - 4, text: `+${startIdx}`, z: 6 });
      return out;
    },
  };
};

const queueLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const name = def.var ?? "";
  const from = def.from ?? "top";
  const seqs = steps.map((s) => listOf(resolve(s, name, from)));
  const ids = trackIds(seqs, "queue", `q:${name}`);
  const gap = 18;
  const cap = Math.max(3, Math.floor((ctx.width - 40) / gap));
  const x0 = ctx.x + 26;
  const y0 = ctx.y + LABEL_H + 10;
  return {
    height: LABEL_H + 34,
    build(i) {
      const seq = seqs[i];
      const out: Ent[] = [header(def, ctx, name)];
      out.push({ id: `${name}:gate`, kind: "gate", x: ctx.x + 8, y: y0 - 4, z: 4 });
      if (!seq) return out;
      const sid = ids[i]!;
      seq.slice(0, cap).forEach((v, k) => {
        out.push({ id: sid[k], kind: "person", x: x0 + k * gap, y: y0, text: compact(v, 5, steps[i]), z: 5, tip: `${name} ${k === 0 ? "front" : `#${k}`}: ${pretty(v)}` });
      });
      if (seq.length > cap) out.push({ id: `${name}:more`, kind: "tiny", x: x0 + cap * gap + 4, y: y0 + 6, text: `+${seq.length - cap}`, z: 6 });
      return out;
    },
  };
};

const heapLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const name = def.var ?? "";
  const from = def.from ?? "top";
  const seqs = steps.map((s) => {
    const l = listOf(resolve(s, name, from));
    return l ? l.slice(0, 31) : null;
  });
  const ids = trackIds(seqs, "match", `h:${name}`);
  const maxN = Math.max(1, ...seqs.map((s) => (s ? s.length : 0)));
  const levels = Math.max(1, Math.ceil(Math.log2(maxN + 1)));
  const dy = 22;
  const y0 = ctx.y + LABEL_H + 10;
  const pos = (k: number) => {
    const d = Math.floor(Math.log2(k + 1));
    const idx = k - (2 ** d - 1);
    const span = ctx.width - 20;
    return { x: ctx.x + 10 + ((idx + 0.5) * span) / 2 ** d, y: y0 + d * dy };
  };
  return {
    height: LABEL_H + levels * dy + 6,
    build(i) {
      const seq = seqs[i];
      const out: Ent[] = [header(def, ctx, name)];
      if (!seq) return out;
      const sid = ids[i]!;
      seq.forEach((v, k) => {
        const p = pos(k);
        out.push({ id: sid[k], kind: "fruit", x: p.x, y: p.y, w: 7, text: compact(v, 4, steps[i]), color: def.color ?? "#e9a23b", z: 5, tip: `${name} heap[${k}] = ${pretty(v)}${k === 0 ? " (top)" : ""}` });
        if (k > 0) {
          const pp = pos(Math.floor((k - 1) / 2));
          out.push({ id: `${name}:he:${k}`, kind: "segment", x: pp.x, y: pp.y + 5, w: p.x, h: p.y - 5, z: 2 });
        }
      });
      return out;
    },
  };
};

// ---------------------------------------------------------------- linked list

const listLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const names = (def.vars ?? def.pointers ?? []) as string[];
  const heads = (def.heads ?? names) as string[];
  const pos = new Map<string, { row: number; col: number }>();
  const rowLen: number[] = [];
  let extraRow = -1;

  const walk = (step: TraceStep, addr: string | null): string[] => {
    const outA: string[] = [];
    const seen = new Set<string>();
    let a = addr;
    while (a && step.nodes[a] && !seen.has(a) && outA.length < 40) {
      seen.add(a);
      outA.push(a);
      a = step.nodes[a].next ?? null;
    }
    return outA;
  };
  steps.forEach((step, si) => {
    const startNames = si === 0 ? heads : names;
    for (const n of startNames) {
      const v = resolve(step, n, "top");
      if (!isPtr(v)) continue;
      const chain = walk(step, v.$p);
      const fresh = chain.filter((a) => !pos.has(a));
      if (!fresh.length) continue;
      let row: number;
      if (si === 0) {
        row = rowLen.length;
        rowLen.push(0);
      } else {
        if (extraRow < 0) {
          extraRow = rowLen.length;
          rowLen.push(0);
        }
        row = extraRow;
      }
      for (const a of fresh) pos.set(a, { row, col: rowLen[row]++ });
    }
    for (const a of Object.keys(step.nodes)) {
      if (pos.has(a) || !("next" in step.nodes[a])) continue;
      if (extraRow < 0) {
        extraRow = rowLen.length;
        rowLen.push(0);
      }
      pos.set(a, { row: extraRow, col: rowLen[extraRow]++ });
    }
  });
  const rows = Math.max(1, Math.min(4, rowLen.length));
  const maxCols = Math.max(1, ...rowLen);
  const cw = clamp(Math.floor((ctx.width - 44) / maxCols), 14, 34);
  const carW = cw - 8;
  const rowH = 46;
  const x0 = ctx.x + 8;
  const y0 = ctx.y + LABEL_H + 30;
  const nullX = ctx.x + ctx.width - 16;
  return {
    height: LABEL_H + rows * rowH + 6,
    build(i) {
      const step = steps[i];
      const out: Ent[] = [header(def, ctx, def.label ?? "train")];
      for (const [a, node] of Object.entries(step.nodes)) {
        const p = pos.get(a);
        if (!p || p.row >= rows) continue;
        out.push({ id: `node:${a}`, kind: "car", x: x0 + p.col * cw, y: y0 + p.row * rowH, w: carW, h: 13, text: show(node.val, 4), z: 5, tip: `ListNode val=${pretty(node.val)} next=${node.next ? show(step.nodes[node.next]?.val) : "null"}` });
        if (node.next && pos.has(node.next)) out.push({ id: `next:${a}`, kind: "arrow", x: 0, y: 0, from: `node:${a}`, to: `node:${node.next}`, z: 3 });
      }
      out.push({ id: "list:null", kind: "nullpad", x: nullX, y: y0 + 6, z: 2 });
      const count = new Map<string, number>();
      for (const n of names) {
        const v = resolve(step, n, "top");
        if (v === undefined) continue;
        let x: number;
        let y: number;
        let slot: string;
        if (isPtr(v) && pos.has(v.$p)) {
          const p = pos.get(v.$p)!;
          x = x0 + p.col * cw + carW / 2;
          y = y0 + p.row * rowH - 1;
          slot = v.$p;
        } else if (v === null) {
          x = nullX + 4;
          y = y0 - 1;
          slot = "null";
        } else continue;
        const k = count.get(slot) ?? 0;
        count.set(slot, k + 1);
        out.push({ id: `list:ptr:${n}`, kind: "hero", x: x + k * 7 - (k ? 3 : 0), y, text: n, color: ctx.color(n), z: 8, h: k, sub: "", tip: `${n} → ${slot === "null" ? "nullptr" : `node ${show(step.nodes[slot]?.val)}`}` });
      }
      return out;
    },
  };
};

// ---------------------------------------------------------------- tree

const treeLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const rootName = def.var ?? "root";
  const from = def.from ?? "outer";
  const pointers = (def.pointers ?? []) as string[];
  const owned = new Set<string>(); // nodes that have hung from this tree's root at some point
  const layouts = steps.map((step) => {
    const root = resolve(step, rootName, from);
    const place = new Map<string, { ord: number; depth: number }>();
    let ord = 0;
    const seen = new Set<string>();
    const visit = (a: string | null | undefined, d: number) => {
      if (!a || seen.has(a) || !step.nodes[a] || d > 6 || place.size > 63) return;
      seen.add(a);
      visit(step.nodes[a].left, d + 1);
      place.set(a, { ord: ord++, depth: d });
      visit(step.nodes[a].right, d + 1);
    };
    if (isPtr(root)) visit(root.$p, 0);
    for (const a of place.keys()) owned.add(a);
    // detached nodes of this tree only, so a second tree on screen doesn't show up here
    const loose = Object.keys(step.nodes).filter((a) => owned.has(a) && !place.has(a));
    return { place, loose, n: ord };
  });
  const maxN = Math.max(1, ...layouts.map((l) => l.n));
  const maxDepth = Math.max(0, ...layouts.map((l) => Math.max(0, ...[...l.place.values()].map((p) => p.depth))));
  const hasLoose = layouts.some((l) => l.loose.length > 0);
  const dx = clamp((ctx.width - 24) / maxN, 10, 30);
  const dy = 26;
  const r = clamp(Math.floor(dx / 2) - 1, 4, 7);
  const x0 = ctx.x + Math.max(12, (ctx.width - dx * maxN) / 2);
  const y0 = ctx.y + LABEL_H + 12;
  const rowsN = maxDepth + 1 + (hasLoose ? 1 : 0);
  return {
    height: LABEL_H + rowsN * dy + 8,
    build(i) {
      const step = steps[i];
      const { place, loose } = layouts[i];
      const out: Ent[] = [header(def, ctx, def.label ?? "tree")];
      const xy = new Map<string, { x: number; y: number }>();
      for (const [a, p] of place) xy.set(a, { x: x0 + p.ord * dx + dx / 2, y: y0 + p.depth * dy });
      loose.slice(0, 20).forEach((a, k) => xy.set(a, { x: x0 + k * 18 + 8, y: y0 + (maxDepth + 1) * dy }));
      for (const [a, p] of xy) {
        const node = step.nodes[a];
        out.push({ id: `tnode:${a}`, kind: "fruit", x: p.x, y: p.y, w: r, text: show(node.val, 3), z: 5, tip: `TreeNode val=${pretty(node.val)}` });
        for (const side of ["left", "right"] as const) {
          const ch = node[side];
          if (ch && xy.has(ch)) out.push({ id: `tedge:${a}:${side}`, kind: "edge", x: 0, y: 0, from: `tnode:${a}`, to: `tnode:${ch}`, z: 2 });
        }
      }
      const count = new Map<string, number>();
      for (const n of pointers) {
        const v = resolve(step, n, "top");
        if (!isPtr(v) || !xy.has(v.$p)) continue;
        const p = xy.get(v.$p)!;
        const k = count.get(v.$p) ?? 0;
        count.set(v.$p, k + 1);
        out.push({ id: `tree:ptr:${n}`, kind: "hero", x: p.x - r - 5 - k * 8, y: p.y + 6, text: n, color: ctx.color(n), z: 8, h: k, sub: "", tip: `${n} → node ${show(step.nodes[v.$p]?.val)}` });
      }
      return out;
    },
  };
};

// ---------------------------------------------------------------- graph

const graphLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  let n = 0;
  let edges: [number, number][] = [];
  for (const step of steps) {
    if (def.adj) {
      const adj = listOf(resolve(step, def.adj, "outer"));
      if (adj && adj.length) {
        n = adj.length;
        edges = [];
        adj.forEach((nb, u) => (listOf(nb) ?? []).forEach((w) => edges.push([u, asInt(w) ?? 0])));
        if (edges.length) break;
      }
    } else if (def.edges) {
      const es = listOf(resolve(step, def.edges, "outer"));
      const nn = def.n ? asInt(resolve(step, def.n, "outer")) : null;
      if (es) {
        edges = es.map((e) => {
          const l = listOf(e) ?? [];
          const a = asInt(l[0]) ?? 0;
          const b = asInt(l[1]) ?? 0;
          return def.reverse ? [b, a] : [a, b];
        });
        n = nn ?? Math.max(0, ...edges.flat()) + 1;
        break;
      }
    }
  }
  n = Math.min(n, 30);
  const R = Math.min(ctx.width / 2 - 20, 62);
  const cx = ctx.x + ctx.width / 2;
  const cy = ctx.y + LABEL_H + R + 12;
  const P = (k: number) => ({ x: cx + R * Math.cos((2 * Math.PI * k) / Math.max(1, n) - Math.PI / 2), y: cy + R * Math.sin((2 * Math.PI * k) / Math.max(1, n) - Math.PI / 2) });
  const stateColors = ["#c8c8d0", "#ffd166", "#06d6a0", "#118ab2", "#ef476f"];
  return {
    height: LABEL_H + 2 * R + 28,
    build(i) {
      const step = steps[i];
      const out: Ent[] = [header(def, ctx, def.label ?? "map")];
      const state = def.state ? listOf(resolve(step, def.state, "top")) : null;
      const seenE = new Set<string>();
      for (const [a, b] of edges) {
        if (a >= n || b >= n) continue;
        const k = def.directed ? `${a}>${b}` : `${Math.min(a, b)}-${Math.max(a, b)}`;
        if (seenE.has(k)) continue;
        seenE.add(k);
        out.push({ id: `g:e:${k}`, kind: "edge", x: 0, y: 0, from: `g:n:${a}`, to: `g:n:${b}`, directed: !!def.directed, z: 2 });
      }
      for (let k = 0; k < n; k++) {
        const p = P(k);
        const sv = state ? state[k] : undefined;
        const si = sv === undefined ? 0 : typeof scalar(sv) === "boolean" ? (scalar(sv) ? 2 : 0) : clamp(asInt(sv) ?? 0, 0, 4);
        out.push({ id: `g:n:${k}`, kind: "town", x: p.x, y: p.y, text: String(k), sub: sv === undefined ? "" : show(sv, 3), color: stateColors[si], z: 5, tip: `node ${k}${sv === undefined ? "" : `, ${def.state} = ${pretty(sv)}`}` });
      }
      out.push(
        ...pointerHeroes((def.pointers ?? []) as string[], step, ctx, (_nm, v) => {
          if (v < 0 || v >= n) return null;
          const p = P(v);
          return { x: p.x + 10, y: p.y + 4 };
        }, "graph"),
      );
      return out;
    },
  };
};

// ---------------------------------------------------------------- intervals

const intervalsLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const names = (def.vars ?? [def.var ?? "intervals"]) as string[];
  let lo = Infinity;
  let hi = -Infinity;
  const data = steps.map((s) =>
    names.map((nm) => {
      const l = listOf(resolve(s, nm, "top"));
      if (!l) return null;
      return l.slice(0, 30).map((iv) => {
        const p = listOf(iv) ?? [];
        const a = asInt(p[0]) ?? 0;
        const b = asInt(p[1]) ?? 0;
        lo = Math.min(lo, a);
        hi = Math.max(hi, b);
        return [a, b] as [number, number];
      });
    }),
  );
  if (!Number.isFinite(lo)) {
    lo = 0;
    hi = 10;
  }
  const span = Math.max(1, hi - lo);
  const x0 = ctx.x + 60;
  const wpx = ctx.width - 72;
  const X = (v: number) => x0 + ((v - lo) / span) * wpx;
  const lanes = 3;
  const rowH = lanes * 9 + 8;
  return {
    height: LABEL_H + names.length * rowH + 12,
    build(i) {
      const step = steps[i];
      const out: Ent[] = [header(def, ctx, def.label ?? "calendar")];
      const ptr = def.pointers?.length ? asInt(resolve(step, def.pointers[0] as string)) : null;
      names.forEach((nm, row) => {
        const y = ctx.y + LABEL_H + row * rowH + 4;
        out.push({ id: `iv:lbl:${nm}`, kind: "label", x: ctx.x + 4, y: y + 8, text: nm, align: "left", z: 9 });
        const ivs = data[i][row];
        if (!ivs) return;
        const laneEnd: number[] = [];
        ivs.forEach(([a, b], k) => {
          let lane = laneEnd.findIndex((e) => e < a);
          if (lane < 0) lane = laneEnd.length < lanes ? laneEnd.length : k % lanes;
          laneEnd[lane] = b;
          out.push({ id: `iv:${nm}:${k}`, kind: "span", x: X(a), y: y + lane * 9, w: Math.max(3, X(b) - X(a)), h: 7, text: `${a}-${b}`, glow: row === 0 && ptr === k ? 1 : 0, color: row === 0 ? "#8ecae6" : "#90be6d", z: 5, tip: `${nm}[${k}] = [${a}, ${b}]` });
        });
      });
      const axisY = ctx.y + LABEL_H + names.length * rowH + 4;
      out.push({ id: "iv:axis", kind: "ground", x: x0, y: axisY, w: wpx, h: 1, z: 2 });
      const ticks = 6;
      for (let t = 0; t <= ticks; t++) {
        const v = Math.round(lo + (span * t) / ticks);
        out.push({ id: `iv:tick:${t}`, kind: "tiny", x: X(v), y: axisY + 5, text: String(v), z: 3 });
      }
      return out;
    },
  };
};

// ---------------------------------------------------------------- signs and call stack

const valuesLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const names = (def.vars ?? []) as string[];
  const w = 58;
  const perRow = Math.max(1, Math.floor((ctx.width - 8) / (w + 4)));
  const rows = Math.max(1, Math.ceil(names.length / perRow));
  return {
    height: rows * 24 + 4,
    build(i) {
      const step = steps[i];
      return names.map((nm, k) => {
        const v = resolve(step, nm, def.from ?? "top");
        return {
          id: `sign:${nm}`,
          kind: "sign",
          x: ctx.x + 4 + (k % perRow) * (w + 4),
          y: ctx.y + 2 + Math.floor(k / perRow) * 24,
          w,
          text: nm,
          sub: compact(v, 8, step),
          z: 6,
          tip: `${nm} = ${pretty(v)}`,
        };
      });
    },
  };
};

const callsLayer: Maker = (def, ctx) => {
  const steps = ctx.trace.steps;
  const dw = 58;
  const maxShow = Math.max(2, Math.floor((ctx.width - 8) / (dw + 3)));
  return {
    height: LABEL_H + 30,
    build(i) {
      const step = steps[i];
      const out: Ent[] = [header(def, ctx, "call stack")];
      const frames = step.stack;
      const start = Math.max(0, frames.length - maxShow);
      for (let d = start; d < frames.length; d++) {
        const f = frames[d];
        const args = Object.entries(f.vars)
          .filter(([, v]) => scalar(v) !== undefined || (isPtr(v) && step.nodes[v.$p]))
          .slice(0, 2)
          .map(([k, v]) => `${k}=${isPtr(v) ? show(step.nodes[v.$p].val, 3) : show(v, 3)}`)
          .join(" ");
        out.push({ id: `call:${d}`, kind: "door", x: ctx.x + 4 + (d - start) * (dw + 3), y: ctx.y + LABEL_H + 2, w: dw, h: 26, text: f.fn, sub: args, glow: d === frames.length - 1 ? 1 : 0, z: 5, tip: `${f.fn}(${args}) at line ${f.line}${d === frames.length - 1 ? " (running)" : " (waiting)"}` });
      }
      if (start > 0) out.push({ id: "call:more", kind: "tiny", x: ctx.x + ctx.width - 12, y: ctx.y + 6, text: `+${start}`, z: 6 });
      return out;
    },
  };
};

const rowLayer: Maker = (def, ctx) => {
  const kids = def.children ?? [];
  const weights = kids.map((k) => (k.weight as number) ?? 1);
  const total = weights.reduce((a, b) => a + b, 0) || 1;
  let x = ctx.x;
  const made = kids.map((k, idx) => {
    const w = Math.floor((ctx.width * weights[idx]) / total);
    const layer = makeLayer(k, { ...ctx, x, width: w });
    x += w;
    return layer;
  });
  return {
    height: Math.max(0, ...made.map((m) => m.height)),
    build: (i) => made.flatMap((m) => m.build(i)),
  };
};

// ---------------------------------------------------------------- auto

const PTR_NAMES = new Set(["i", "j", "k", "l", "r", "lo", "hi", "left", "right", "mid", "start", "end", "slow", "fast", "p1", "p2", "read", "write", "idx", "low", "high"]);

export function autoDefs(trace: Trace): LayerDef[] {
  const kinds = new Map<string, string>();
  const order: string[] = [];
  for (const step of trace.steps) {
    step.stack.forEach((frame) => {
      for (const [nm, v] of Object.entries(frame.vars)) {
        if (kinds.has(nm) || v === undefined) continue;
        let kind: string | null = null;
        if (v === null) continue;
        if (isPtr(v)) {
          const node = step.nodes[v.$p];
          if (!node) continue;
          kind = "next" in node ? "listptr" : "treeptr";
        } else if (typeof v === "string") kind = v.length > 1 ? "string" : "value";
        else if (Array.isArray(v)) kind = v.length && listOf(v[0]) && typeof v[0] !== "string" ? "grid" : "array";
        else if (isTyped(v, "map") || isTyped(v, "set")) kind = "map";
        else if (isTyped(v, "stack")) kind = "stack";
        else if (isTyped(v, "queue") || isTyped(v, "deque")) kind = "queue";
        else if (isTyped(v, "heap")) kind = "heap";
        else if (scalar(v) !== undefined) kind = "value";
        if (kind) {
          kinds.set(nm, kind);
          order.push(nm);
        }
      }
    });
  }
  const defs: LayerDef[] = [];
  const by = (k: string) => order.filter((n) => kinds.get(n) === k);
  const ptrs = by("value").filter((n) => PTR_NAMES.has(n));
  const arrays = [...by("array"), ...by("string")];
  arrays.forEach((nm, idx) => defs.push({ kind: "array", var: nm, style: kinds.get(nm) === "string" ? "letters" : "crates", pointers: idx === 0 ? ptrs : [] }));
  by("grid").forEach((nm) => defs.push({ kind: "grid", var: nm, palette: "dp" }));
  by("map").forEach((nm) => defs.push({ kind: "map", var: nm }));
  by("stack").forEach((nm) => defs.push({ kind: "stack", var: nm }));
  by("queue").forEach((nm) => defs.push({ kind: "queue", var: nm }));
  by("heap").forEach((nm) => defs.push({ kind: "heap", var: nm }));
  if (by("listptr").length) defs.push({ kind: "list", vars: by("listptr") });
  if (by("treeptr").length) defs.push({ kind: "tree", var: by("treeptr")[0], pointers: by("treeptr") });
  const signs = by("value").filter((n) => !(arrays.length && ptrs.includes(n)));
  if (signs.length) defs.push({ kind: "values", vars: signs.slice(0, 16) });
  return defs;
}

const MAKERS: Record<string, Maker> = {
  array: arrayLayer,
  string: (d, c) => arrayLayer({ ...d, style: d.style ?? "letters" }, c),
  bars: (d, c) => arrayLayer({ ...d, style: "bars" }, c),
  grid: gridLayer,
  map: mapLayer,
  set: mapLayer,
  stack: stackLayer,
  queue: queueLayer,
  heap: heapLayer,
  list: listLayer,
  tree: treeLayer,
  graph: graphLayer,
  intervals: intervalsLayer,
  values: valuesLayer,
  calls: callsLayer,
  row: rowLayer,
};

export function makeLayer(def: LayerDef, ctx: LayerCtx): Layer {
  if (def.kind === "auto") {
    const defs = autoDefs(ctx.trace);
    let y = ctx.y;
    const made = defs.map((d) => {
      const l = makeLayer(d, { ...ctx, y });
      y += l.height + 4;
      return l;
    });
    return { height: y - ctx.y, build: (i) => made.flatMap((m) => m.build(i)) };
  }
  const maker = MAKERS[def.kind];
  if (!maker) return { height: 0, build: () => [] };
  return maker(def, ctx);
}

export function usesRecursion(trace: Trace): boolean {
  return trace.steps.some((s) => s.stack.length > 1);
}
