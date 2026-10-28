import type { SceneDef, Trace } from "@/lib/types";
import * as D from "./draw";
import { type Ent, makeLayer, usesRecursion } from "./layers";

export const SCENE_W = 320;

/** Turns a trace + scene definition into per-step entity lists. */
export class Scene {
  readonly width = SCENE_W;
  readonly height: number;
  readonly theme: D.Theme;
  private layers: ReturnType<typeof makeLayer>[] = [];
  private colors = new Map<string, string>();

  constructor(readonly trace: Trace, def: SceneDef) {
    this.theme = D.THEMES[def.theme] ?? D.THEMES.dock;
    const color = (name: string) => {
      if (!this.colors.has(name)) this.colors.set(name, D.POINTER_COLORS[this.colors.size % D.POINTER_COLORS.length]);
      return this.colors.get(name)!;
    };
    const defs = [...(def.layers?.length ? def.layers : [{ kind: "auto" }])];
    if (usesRecursion(trace) && !defs.some((d) => d.kind === "calls")) defs.push({ kind: "calls" });
    let y = 18;
    for (const d of defs) {
      const layer = makeLayer(d, { trace, x: 0, y, width: SCENE_W, color });
      this.layers.push(layer);
      y += layer.height + 6;
    }
    this.height = Math.max(120, y + 14);
  }

  get length() {
    return this.trace.steps.length;
  }

  frame(i: number): Ent[] {
    const step = this.trace.steps[i];
    if (!step) return [];
    const ents = this.layers.flatMap((l) => l.build(i));
    const last = i === this.trace.steps.length - 1;
    if (step.error) {
      for (const e of ents) if (e.kind === "hero") e.fall = true;
      const msg = step.error === "SIGSEGV" ? "CRASH! bad pointer" : step.error === "SIGABRT" ? "CRASH! out of range" : `CRASH! ${step.error}`;
      ents.push({ id: "banner", kind: "banner", x: SCENE_W / 2, y: 9, text: `${msg} (line ${step.line})`, color: "#d62828", z: 20 });
    } else if (last && this.trace.end.kind === "limit") {
      ents.push({ id: "banner", kind: "banner", x: SCENE_W / 2, y: 9, text: "STEP LIMIT: infinite loop?", color: "#f77f00", z: 20 });
    } else if (last && this.trace.end.kind === "exit") {
      ents.push({ id: "banner", kind: "banner", x: SCENE_W / 2, y: 9, text: "DONE", color: "#2a9d8f", z: 20 });
    }
    return ents;
  }
}

interface Live {
  ent: Ent;
  fx: number;
  fy: number;
  fa: number;
  x: number;
  y: number;
  a: number;
  ta: number;
  t0: number;
  flash: number;
  dead: boolean;
}

/** Owns the canvas, tweens entities between frames, and draws them. */
export class Renderer {
  private ctx: CanvasRenderingContext2D;
  private live = new Map<string, Live>();
  private scene: Scene | null = null;
  private raf = 0;
  private duration = 320;
  private readonly S = 3;
  private bornStep = 0;
  private hoverId: string | null = null;

  constructor(private canvas: HTMLCanvasElement) {
    this.ctx = canvas.getContext("2d")!;
    this.loop = this.loop.bind(this);
    this.raf = requestAnimationFrame(this.loop);
  }

  setScene(scene: Scene | null) {
    this.scene = scene;
    this.live.clear();
    const w = scene?.width ?? SCENE_W;
    const h = scene?.height ?? 160;
    this.canvas.width = w * this.S;
    this.canvas.height = h * this.S;
  }

  setSpeed(ms: number) {
    this.duration = ms;
  }

  show(i: number, animate: boolean) {
    if (!this.scene) return;
    const now = performance.now();
    const ents = this.scene.frame(i);
    const next = new Set<string>();
    for (const e of ents) {
      next.add(e.id);
      const cur = this.live.get(e.id);
      if (cur && !cur.dead) {
        const changed = cur.ent.text !== e.text || cur.ent.sub !== e.sub || cur.ent.h !== e.h || cur.ent.w !== e.w;
        cur.fx = cur.x;
        cur.fy = cur.y;
        cur.fa = cur.a;
        cur.ta = 1;
        cur.t0 = animate ? now : now - this.duration;
        if (changed && animate && e.kind !== "hero" && e.kind !== "label") cur.flash = now;
        cur.ent = e;
      } else {
        const spawnFromAbove = animate && this.bornStep !== i && !["label", "edge", "arrow", "segment", "ground", "gate", "nullpad", "tiny"].includes(e.kind);
        this.live.set(e.id, {
          ent: e,
          fx: e.x,
          fy: spawnFromAbove ? e.y - 10 : e.y,
          fa: animate ? 0 : 1,
          x: e.x,
          y: e.y,
          a: animate ? 0 : 1,
          ta: 1,
          t0: animate ? now : now - this.duration,
          flash: spawnFromAbove ? now : 0,
          dead: false,
        });
      }
    }
    for (const [id, l] of this.live) {
      if (next.has(id)) continue;
      if (!animate) {
        this.live.delete(id);
        continue;
      }
      l.dead = true;
      l.fx = l.x;
      l.fy = l.y;
      l.fa = l.a;
      l.ta = 0;
      l.t0 = now;
    }
    this.bornStep = i;
  }

  destroy() {
    cancelAnimationFrame(this.raf);
  }

  /** Logical-pixel bounding box of a live entity, or null for non-interactive kinds. */
  private box(l: Live): [number, number, number, number] | null {
    const e = l.ent;
    const w = e.w ?? 0;
    const h = e.h ?? 0;
    switch (e.kind) {
      case "crate": case "tile": case "locker": case "block": case "car": case "span": case "door":
        return [l.x, l.y, w, h];
      case "sign":
        return [l.x, l.y, w, 20];
      case "bar":
        return [l.x, l.y - h - 8, w, h + 8];
      case "hero":
        return [l.x - 5, l.y - 13, 10, 14];
      case "fruit":
        return [l.x - w - 1, l.y - w - 1, 2 * w + 2, 2 * w + 2];
      case "town":
        return [l.x - 8, l.y - 9, 16, 16];
      case "person":
        return [l.x - 3, l.y - 9, 14, 24];
      default:
        return null;
    }
  }

  /** Entity under a logical point (topmost first). */
  hitTest(x: number, y: number): Ent | null {
    const list = [...this.live.values()].filter((l) => !l.dead && l.ent.tip);
    list.sort((a, b) => (b.ent.z ?? 5) - (a.ent.z ?? 5));
    for (const l of list) {
      const b = this.box(l);
      if (b && x >= b[0] && x <= b[0] + b[2] && y >= b[1] && y <= b[1] + b[3]) return l.ent;
    }
    return null;
  }

  setHover(id: string | null) {
    this.hoverId = id;
  }

  get size() {
    return { w: this.scene?.width ?? SCENE_W, h: this.scene?.height ?? 160 };
  }

  private loop(now: number) {
    this.raf = requestAnimationFrame(this.loop);
    const c = this.ctx;
    const scene = this.scene;
    const W = scene?.width ?? SCENE_W;
    const H = scene?.height ?? 160;
    c.setTransform(this.S, 0, 0, this.S, 0, 0);
    c.imageSmoothingEnabled = false;
    D.background(c, scene?.theme ?? D.THEMES.dock, W, H, now);
    if (!scene) return;

    const list: Live[] = [];
    for (const [id, l] of this.live) {
      const k = Math.min(1, (now - l.t0) / this.duration);
      const e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      l.x = l.fx + (l.ent.x - l.fx) * e;
      l.y = l.fy + (l.ent.y - l.fy) * e;
      l.a = l.fa + (l.ta - l.fa) * e;
      if (l.dead && k >= 1) {
        this.live.delete(id);
        continue;
      }
      list.push(l);
    }
    list.sort((a, b) => (a.ent.z ?? 5) - (b.ent.z ?? 5));
    for (const l of list) {
      c.globalAlpha = Math.max(0, Math.min(1, l.a));
      this.draw(l, now);
    }
    c.globalAlpha = 1;
    const hov = this.hoverId ? this.live.get(this.hoverId) : undefined;
    if (hov) {
      const b = this.box(hov);
      if (b) {
        const pulse = Math.floor(now / 200) % 2 ? "#ffffff" : "#ffe066";
        D.rect(c, b[0] - 2, b[1] - 2, b[2] + 4, 1, pulse);
        D.rect(c, b[0] - 2, b[1] + b[3] + 1, b[2] + 4, 1, pulse);
        D.rect(c, b[0] - 2, b[1] - 2, 1, b[3] + 4, pulse);
        D.rect(c, b[0] + b[2] + 1, b[1] - 2, 1, b[3] + 4, pulse);
      }
    }
    // faint scanlines for the CRT feel
    c.fillStyle = "rgba(0,0,0,0.05)";
    for (let y = 0; y < H; y += 2) c.fillRect(0, y, W, 1);
  }

  private center(id: string | undefined): { x: number; y: number; w: number; h: number; kind: string } | null {
    if (!id) return null;
    const l = this.live.get(id);
    if (!l) return null;
    return { x: l.x, y: l.y, w: l.ent.w ?? 0, h: l.ent.h ?? 0, kind: l.ent.kind };
  }

  private draw(l: Live, now: number) {
    const c = this.ctx;
    const e = l.ent;
    const glow = (e.glow ?? 0) > 0 || now - l.flash < 450 ? 1 : 0;
    const moving = Math.abs(l.x - e.x) > 0.5 || Math.abs(l.y - e.y) > 0.5;
    const ink = this.scene?.theme.ink ?? "#1b1b2a";
    switch (e.kind) {
      case "label":
        D.text(c, e.text ?? "", l.x, l.y, { size: 5, align: e.align ?? "center", color: ink });
        break;
      case "tiny":
        D.text(c, e.text ?? "", l.x, l.y, { size: 4, color: ink });
        break;
      case "crate":
        D.crate(c, l.x, l.y, e.w!, e.h!, e.text ?? "", glow);
        break;
      case "tile":
        D.tile(c, l.x, l.y, e.w!, e.h!, e.color ?? "#f5ebd7", e.text ?? "", glow);
        break;
      case "bar":
        D.bar(c, l.x, l.y, e.w!, e.h!, e.text ?? "", glow);
        break;
      case "water":
        D.water(c, l.x, l.y, e.w!, e.h!, now);
        break;
      case "spot":
        D.spot(c, l.x, l.y, e.w!, e.h!);
        break;
      case "locker":
        D.locker(c, l.x, l.y, e.w!, e.h!, e.text ?? "", e.sub ?? "", glow);
        break;
      case "block":
        D.block(c, l.x, l.y, e.w!, e.h!, e.text ?? "", glow, e.color);
        break;
      case "person":
        D.person(c, l.x, l.y, e.text ?? "", glow, now, moving);
        break;
      case "car":
        D.car(c, l.x, l.y, e.w!, e.h!, e.text ?? "", glow);
        break;
      case "fruit":
        D.fruit(c, l.x, l.y, e.w ?? 6, e.text ?? "", glow, e.color);
        break;
      case "town": {
        D.rect(c, l.x - 7, l.y - 6, 14, 12, "#1b1b2a");
        D.rect(c, l.x - 6, l.y - 5, 12, 10, glow ? "#fff6a0" : e.color ?? "#c8c8d0");
        D.rect(c, l.x - 7, l.y - 8, 14, 2, "#9b2226");
        D.text(c, e.text ?? "", l.x, l.y + 1, { size: 5 });
        if (e.sub) D.text(c, e.sub, l.x, l.y + 11, { size: 4, color: ink });
        break;
      }
      case "span":
        D.rect(c, l.x, l.y, e.w!, e.h!, "#1b1b2a");
        D.rect(c, l.x + 1, l.y + 1, e.w! - 2, e.h! - 2, glow ? "#ffe066" : e.color ?? "#8ecae6");
        if (e.w! > 18) D.text(c, e.text ?? "", l.x + e.w! / 2, l.y + 4, { size: 4 });
        break;
      case "sign":
        D.sign(c, l.x, l.y, e.w!, e.text ?? "", e.sub ?? "", glow);
        break;
      case "door":
        D.door(c, l.x, l.y, e.w!, e.h!, e.text ?? "", e.sub ?? "", glow > 0);
        break;
      case "ground":
        D.rect(c, l.x, l.y, e.w!, e.h!, "#3b2416");
        break;
      case "gate":
        D.rect(c, l.x, l.y, 3, 22, "#5a3a22");
        D.rect(c, l.x + 6, l.y, 3, 22, "#5a3a22");
        D.rect(c, l.x - 1, l.y, 11, 3, "#9b2226");
        break;
      case "nullpad":
        D.rect(c, l.x, l.y, 10, 2, "#1b1b2a");
        D.text(c, "null", l.x + 5, l.y + 6, { size: 4, color: ink });
        break;
      case "segment":
        D.line(c, l.x, l.y, e.w!, e.h!, "#5a3a22");
        break;
      case "edge": {
        const a = this.center(e.from);
        const b = this.center(e.to);
        if (!a || !b) break;
        if (a.kind === "town") {
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const len = Math.hypot(dx, dy) || 1;
          const ux = dx / len;
          const uy = dy / len;
          D.line(c, a.x + ux * 8, a.y + uy * 8, b.x - ux * 9, b.y - uy * 9, "#6d597a");
          if (e.directed) D.rect(c, b.x - ux * 10 - 1, b.y - uy * 10 - 1, 3, 3, "#d62828");
        } else D.line(c, a.x, a.y + 4, b.x, b.y - 4, "#5a3a22");
        break;
      }
      case "arrow": {
        const a = this.center(e.from);
        const b = this.center(e.to);
        if (!a || !b) break;
        const y1 = a.y + a.h / 2;
        if (Math.abs(a.y - b.y) < 1 && b.x > a.x) {
          D.line(c, a.x + a.w, y1, b.x - 1, y1, "#1b1b2a");
          D.arrowHead(c, b.x - 1, y1, 1, "#1b1b2a");
        } else {
          // loop over the top for backwards / cross-row links
          const top = Math.min(a.y, b.y) - 4;
          const ax = a.x + a.w / 2;
          const bx = b.x + b.w / 2;
          D.line(c, ax, a.y, ax, top, "#7b2cbf");
          D.line(c, ax, top, bx, top, "#7b2cbf");
          D.line(c, bx, top, bx, b.y - 1, "#7b2cbf");
          D.rect(c, bx - 1, b.y - 3, 3, 2, "#7b2cbf");
        }
        break;
      }
      case "hero": {
        let y = l.y;
        if (e.fall) y += ((now / 6) % 30);
        D.hero(c, l.x, y, e.color ?? "#e8534a", moving, now);
        const stacked = e.h ?? 0;
        const tagY = stacked ? (e.below ? l.y + 5 + (stacked - 1) * 8 : l.y - 17 - stacked * 8) : l.y - 17;
        D.nameTag(c, e.sub ? `${e.text}=${e.sub}` : e.text ?? "", l.x, tagY, e.color ?? "#e8534a");
        break;
      }
      case "banner": {
        const s = e.text ?? "";
        c.font = "6px monospace";
        const w = Math.max(80, s.length * 6 + 10);
        D.rect(c, l.x - w / 2, l.y - 6, w, 12, e.color ?? "#d62828");
        D.text(c, s, l.x, l.y, { size: 6, color: "#fff" });
        break;
      }
    }
  }
}
