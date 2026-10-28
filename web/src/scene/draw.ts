/** Pixel drawing primitives, sprites, and theme backgrounds. All coordinates are logical pixels. */

export type Ctx = CanvasRenderingContext2D;

export const POINTER_COLORS = ["#e8534a", "#3b82f6", "#f5c542", "#22c55e", "#a855f7", "#f97316", "#14b8a6", "#ec4899"];

let FONT = "monospace";
export function setFont(family: string) {
  FONT = family || "monospace";
}

export function rect(c: Ctx, x: number, y: number, w: number, h: number, color: string) {
  c.fillStyle = color;
  c.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h));
}

export function text(
  c: Ctx,
  s: string,
  x: number,
  y: number,
  opts: { size?: number; color?: string; align?: CanvasTextAlign; shadow?: string } = {},
) {
  const size = opts.size ?? 8;
  c.font = `${size}px ${FONT}`;
  c.textAlign = opts.align ?? "center";
  c.textBaseline = "middle";
  if (opts.shadow) {
    c.fillStyle = opts.shadow;
    c.fillText(s, Math.round(x) + 1, Math.round(y) + 1);
  }
  c.fillStyle = opts.color ?? "#1b1b2a";
  c.fillText(s, Math.round(x), Math.round(y));
}

export function fitSize(s: string, w: number, base = 8): number {
  const max = Math.floor((w - 2) / Math.max(1, s.length));
  return Math.max(4, Math.min(base, max));
}

/** Draw a pixel map: rows of chars, each char a palette key ('.' = transparent). */
export function pix(c: Ctx, map: string[], x: number, y: number, pal: Record<string, string>, scale = 1, flip = false) {
  const w = map[0].length;
  for (let r = 0; r < map.length; r++) {
    for (let k = 0; k < w; k++) {
      const ch = map[r][flip ? w - 1 - k : k];
      if (ch === ".") continue;
      const col = pal[ch];
      if (!col) continue;
      c.fillStyle = col;
      c.fillRect(Math.round(x + k * scale), Math.round(y + r * scale), scale, scale);
    }
  }
}

const HERO_A = [
  "..hhhh..",
  ".hhhhhh.",
  ".hssssh.",
  ".sekske.",
  ".ssssss.",
  "..smms..",
  ".cccccc.",
  "sccccccs",
  "s.cccc.s",
  "..pppp..",
  "..p..p..",
  ".bb..bb.",
];
const HERO_B = [
  "..hhhh..",
  ".hhhhhh.",
  ".hssssh.",
  ".sekske.",
  ".ssssss.",
  "..smms..",
  ".cccccc.",
  "sccccccs",
  "s.cccc.s",
  "..pppp..",
  ".p....p.",
  "bb....bb",
];

export function hero(c: Ctx, x: number, y: number, color: string, walking: boolean, t: number, flip = false) {
  const frame = walking && Math.floor(t / 120) % 2 === 1 ? HERO_B : HERO_A;
  const pal = { h: "#3b2416", s: "#f2c9a0", e: "#1b1b2a", k: "#f2c9a0", m: "#c0705a", c: color, p: "#2d3a5a", b: "#1b1b2a" };
  pix(c, frame, x - 4, y - 12, pal, 1, flip);
}

export function nameTag(c: Ctx, s: string, x: number, y: number, color: string) {
  const size = 5;
  c.font = `${size}px ${FONT}`;
  const w = Math.max(10, Math.ceil(c.measureText(s).width) + 4);
  rect(c, x - w / 2, y - 4, w, 8, color);
  rect(c, x - w / 2, y + 4, w, 1, "rgba(0,0,0,0.35)");
  text(c, s, x, y, { size, color: "#fff" });
}

export function crate(c: Ctx, x: number, y: number, w: number, h: number, label: string, glow: number) {
  rect(c, x, y, w, h, "#6b3f1f");
  rect(c, x + 1, y + 1, w - 2, h - 2, glow > 0 ? "#f0b860" : "#c98a4b");
  rect(c, x + 1, y + Math.floor(h / 2), w - 2, 1, "#9c6334");
  rect(c, x + 2, y + 2, w - 4, 1, "#e6ac6d");
  text(c, label, x + w / 2, y + h / 2 + 1, { size: fitSize(label, w), color: "#2a1608" });
}

export function tile(c: Ctx, x: number, y: number, w: number, h: number, fill: string, label: string, glow: number, ink = "#1b1b2a") {
  rect(c, x, y, w, h, "rgba(0,0,0,0.35)");
  rect(c, x + 1, y + 1, w - 2, h - 2, fill);
  if (glow > 0) {
    rect(c, x, y, w, 1, "#fff6a0");
    rect(c, x, y + h - 1, w, 1, "#fff6a0");
    rect(c, x, y, 1, h, "#fff6a0");
    rect(c, x + w - 1, y, 1, h, "#fff6a0");
  }
  if (label) text(c, label, x + w / 2, y + h / 2 + 1, { size: fitSize(label, w, w >= 14 ? 8 : 6), color: ink });
}

export function bar(c: Ctx, x: number, y: number, w: number, h: number, label: string, glow: number) {
  // y is the bottom (ground line); bar grows upward
  for (let k = 0; k < h; k += 4) {
    const bh = Math.min(4, h - k);
    rect(c, x, y - k - bh, w, bh, k % 8 === 0 ? "#8a5a44" : "#a06a50");
    rect(c, x + ((k / 4) % 2 === 0 ? 0 : Math.floor(w / 2)), y - k - bh, 1, bh, "#6a3e2e");
  }
  if (glow > 0) rect(c, x, y - h - 1, w, 1, "#fff6a0");
  text(c, label, x + w / 2, y - h - 6, { size: fitSize(label, w + 4, 6), color: "#fff", shadow: "#000" });
}

export function water(c: Ctx, x: number, y: number, w: number, h: number, t: number) {
  if (h <= 0) return;
  rect(c, x, y - h, w, h, "rgba(64,150,255,0.65)");
  const off = Math.floor(t / 200) % 2;
  rect(c, x + off, y - h, Math.max(0, w - 1), 1, "rgba(220,240,255,0.9)");
}

export function locker(c: Ctx, x: number, y: number, w: number, h: number, key: string, val: string, glow: number) {
  rect(c, x, y, w, h, "#2d3a5a");
  rect(c, x + 1, y + 1, w - 2, 8, glow > 0 ? "#ffe066" : "#9fb3d1");
  text(c, key, x + w / 2, y + 5, { size: fitSize(key, w, 6), color: "#1b1b2a" });
  rect(c, x + 1, y + 10, w - 2, h - 11, glow > 0 ? "#6c8cc4" : "#4a5f8a");
  rect(c, x + w - 4, y + 12, 2, 2, "#d0d8e8");
  if (val) text(c, val, x + w / 2, y + 10 + (h - 11) / 2 + 1, { size: fitSize(val, w, 6), color: "#fff" });
}

export function block(c: Ctx, x: number, y: number, w: number, h: number, label: string, glow: number, color = "#5aa0d8") {
  rect(c, x, y, w, h, "#1b1b2a");
  rect(c, x + 1, y + 1, w - 2, h - 2, glow > 0 ? "#ffe066" : color);
  rect(c, x + 1, y + 1, w - 2, 1, "rgba(255,255,255,0.5)");
  text(c, label, x + w / 2, y + h / 2 + 1, { size: fitSize(label, w, 8), color: "#1b1b2a" });
}

export function person(c: Ctx, x: number, y: number, label: string, glow: number, t: number, walking: boolean) {
  hero(c, x + 4, y + 14, glow > 0 ? "#ffb347" : "#7cc576", walking, t);
  // carried token
  rect(c, x - 2, y - 8, 12, 9, "#1b1b2a");
  rect(c, x - 1, y - 7, 10, 7, "#fff3c4");
  text(c, label, x + 4, y - 3, { size: fitSize(label, 12, 6) });
}

export function car(c: Ctx, x: number, y: number, w: number, h: number, label: string, glow: number) {
  rect(c, x, y, w, h, "#1b1b2a");
  rect(c, x + 1, y + 1, w - 2, h - 2, glow > 0 ? "#ffe066" : "#d9534f");
  rect(c, x + 3, y + 3, w - 6, h - 7, "#ffe9c7");
  text(c, label, x + w / 2, y + h / 2 - 1, { size: fitSize(label, w - 4, 6) });
  rect(c, x + 3, y + h, 4, 3, "#1b1b2a");
  rect(c, x + w - 7, y + h, 4, 3, "#1b1b2a");
}

export function fruit(c: Ctx, x: number, y: number, r: number, label: string, glow: number, color = "#e04848") {
  const map = [
    "...gg...",
    "..fffff.",
    ".fffffff",
    "ffffffff",
    "ffffffff",
    "ffffffff",
    ".ffffff.",
    "..ffff..",
  ];
  const scale = Math.max(1, Math.round((r * 2) / 8));
  pix(c, map, x - 4 * scale, y - 4 * scale, { g: "#3c8a3c", f: glow > 0 ? "#ffd84a" : color }, scale);
  text(c, label, x, y + 1, { size: fitSize(label, r * 2, 6), color: "#fff", shadow: "#000" });
}

export function sign(c: Ctx, x: number, y: number, w: number, label: string, val: string, glow: number) {
  rect(c, x + w / 2 - 1, y + 14, 2, 6, "#5a3a22");
  rect(c, x, y, w, 15, "#5a3a22");
  rect(c, x + 1, y + 1, w - 2, 13, glow > 0 ? "#ffe9a0" : "#e8d2a6");
  text(c, label, x + w / 2, y + 4, { size: fitSize(label, w, 5), color: "#5a3a22" });
  text(c, val, x + w / 2, y + 10, { size: fitSize(val, w, 6), color: "#1b1b2a" });
}

export function door(c: Ctx, x: number, y: number, w: number, h: number, label: string, sub: string, active: boolean) {
  rect(c, x, y, w, h, "#3b2416");
  rect(c, x + 2, y + 2, w - 4, h - 2, active ? "#c98a4b" : "#7a5030");
  rect(c, x + w - 6, y + h / 2, 2, 2, "#f5c542");
  text(c, label, x + w / 2, y + 7, { size: fitSize(label, w - 4, 5), color: "#fff", shadow: "#000" });
  if (sub) text(c, sub, x + w / 2, y + 16, { size: fitSize(sub, w - 4, 5), color: "#fff3c4", shadow: "#000" });
}

export function spot(c: Ctx, x: number, y: number, w: number, h: number) {
  c.fillStyle = "rgba(255,240,120,0.28)";
  c.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h));
  rect(c, x, y, w, 1, "rgba(255,240,120,0.9)");
  rect(c, x, y + h - 1, w, 1, "rgba(255,240,120,0.9)");
}

export function line(c: Ctx, x1: number, y1: number, x2: number, y2: number, color: string) {
  // Bresenham-ish pixel line
  const dx = Math.abs(x2 - x1);
  const dy = Math.abs(y2 - y1);
  const steps = Math.max(dx, dy, 1);
  c.fillStyle = color;
  for (let i = 0; i <= steps; i++) {
    const px = x1 + ((x2 - x1) * i) / steps;
    const py = y1 + ((y2 - y1) * i) / steps;
    c.fillRect(Math.round(px), Math.round(py), 1, 1);
  }
}

export function arrowHead(c: Ctx, x: number, y: number, dir: 1 | -1, color: string) {
  rect(c, x - dir * 2, y - 2, 1, 5, color);
  rect(c, x - dir * 1, y - 1, 1, 3, color);
  rect(c, x, y, 1, 1, color);
}

// ---------------------------------------------------------------- themes

export interface Theme {
  sky: [string, string];
  ground: string;
  accent: string;
  ink: string;
  deco: (c: Ctx, w: number, h: number, t: number) => void;
}

function clouds(c: Ctx, w: number, t: number, color = "rgba(255,255,255,0.8)") {
  for (let i = 0; i < 4; i++) {
    const x = ((i * 137 + t / 90) % (w + 60)) - 40;
    const y = 8 + ((i * 23) % 30);
    rect(c, x, y, 24, 4, color);
    rect(c, x + 5, y - 3, 13, 3, color);
  }
}

function waves(c: Ctx, w: number, h: number, t: number) {
  rect(c, 0, h - 10, w, 10, "#2b6cb0");
  for (let x = 0; x < w; x += 12) {
    const o = Math.floor(t / 300 + x / 12) % 3;
    rect(c, x + o * 2, h - 10, 5, 1, "#90cdf4");
  }
}

function rain(c: Ctx, w: number, h: number, t: number) {
  for (let i = 0; i < 40; i++) {
    const x = (i * 53) % w;
    const y = (i * 97 + t / 4) % h;
    rect(c, x, y, 1, 3, "rgba(170,200,255,0.5)");
  }
}

function stars(c: Ctx, w: number, h: number, t: number) {
  for (let i = 0; i < 50; i++) {
    const x = (i * 71) % w;
    const y = (i * 37) % h;
    const on = (Math.floor(t / 500) + i) % 5 !== 0;
    if (on) rect(c, x, y, 1, 1, "rgba(255,255,255,0.8)");
  }
}

function pines(c: Ctx, w: number, h: number) {
  for (let x = 6; x < w; x += 46) {
    for (let k = 0; k < 10; k++) rect(c, x - k, h - 18 - 20 + k * 2, 2 * k + 1, 2, "#2f6b3a");
    rect(c, x - 1, h - 18, 3, 6, "#5a3a22");
  }
}

function skyline(c: Ctx, w: number, h: number) {
  for (let x = 0; x < w; x += 30) {
    const bh = 20 + ((x * 7) % 30);
    rect(c, x, h - 12 - bh, 24, bh, "#2a2f45");
    for (let wy = h - 12 - bh + 4; wy < h - 16; wy += 6) rect(c, x + 4, wy, 3, 2, "#f5d76e");
  }
}

function fence(c: Ctx, w: number, h: number) {
  rect(c, 0, h - 18, w, 2, "#a0703a");
  for (let x = 2; x < w; x += 10) rect(c, x, h - 22, 2, 10, "#a0703a");
}

function bricks(c: Ctx, w: number, h: number) {
  for (let y = 0; y < h; y += 8)
    for (let x = (y / 8) % 2 ? -8 : 0; x < w; x += 16) rect(c, x, y, 15, 7, "rgba(0,0,0,0.12)");
}

function awning(c: Ctx, w: number) {
  for (let x = 0; x < w; x += 16) {
    rect(c, x, 0, 8, 6, "#e04848");
    rect(c, x + 8, 0, 8, 6, "#fff3e0");
  }
}

function torches(c: Ctx, w: number, h: number, t: number) {
  for (let x = 20; x < w; x += 120) {
    rect(c, x, h / 2, 2, 8, "#5a3a22");
    rect(c, x - 1, h / 2 - 3, 4, 3, Math.floor(t / 150) % 2 ? "#ffb347" : "#ff6b35");
  }
}

export const THEMES: Record<string, Theme> = {
  dock: { sky: ["#8ecae6", "#cdeefd"], ground: "#8a6a4a", accent: "#2b6cb0", ink: "#1b1b2a", deco: (c, w, h, t) => { clouds(c, w, t); waves(c, w, h, t); } },
  market: { sky: ["#ffd9a0", "#fff1d6"], ground: "#c9a27a", accent: "#e04848", ink: "#1b1b2a", deco: (c, w) => awning(c, w) },
  forest: { sky: ["#a7e3a1", "#e6f7d9"], ground: "#5a8a3c", accent: "#2f6b3a", ink: "#1b1b2a", deco: (c, w, h, t) => { clouds(c, w, t); pines(c, w, h); } },
  city: { sky: ["#3a4466", "#6b7aa6"], ground: "#3a3a4a", accent: "#90cdf4", ink: "#ffffff", deco: (c, w, h, t) => { skyline(c, w, h); rain(c, w, h, t); } },
  farm: { sky: ["#bde0fe", "#fefae0"], ground: "#9c7a4a", accent: "#e9c46a", ink: "#1b1b2a", deco: (c, w, h, t) => { clouds(c, w, t); fence(c, w, h); } },
  castle: { sky: ["#9a8c98", "#c9ada7"], ground: "#6d6875", accent: "#f5c542", ink: "#1b1b2a", deco: (c, w, h) => bricks(c, w, h) },
  cave: { sky: ["#1f1b2e", "#3a3150"], ground: "#2a2438", accent: "#ffb347", ink: "#ffffff", deco: (c, w, h, t) => torches(c, w, h, t) },
  space: { sky: ["#0b1026", "#1d2b53"], ground: "#29366f", accent: "#a855f7", ink: "#ffffff", deco: (c, w, h, t) => stars(c, w, h, t) },
  lab: { sky: ["#d8e2dc", "#f4f1de"], ground: "#8d99ae", accent: "#14b8a6", ink: "#1b1b2a", deco: (c, w, h) => bricks(c, w, h) },
};

export function background(c: Ctx, theme: Theme, w: number, h: number, t: number) {
  const bands = 8;
  for (let i = 0; i < bands; i++) {
    c.fillStyle = mix(theme.sky[0], theme.sky[1], i / (bands - 1));
    c.fillRect(0, Math.floor((h * i) / bands), w, Math.ceil(h / bands) + 1);
  }
  theme.deco(c, w, h, t);
}

function mix(a: string, b: string, k: number): string {
  const pa = parseInt(a.slice(1), 16);
  const pb = parseInt(b.slice(1), 16);
  const ch = (p: number, s: number) => (p >> s) & 255;
  const m = (s: number) => Math.round(ch(pa, s) + (ch(pb, s) - ch(pa, s)) * k);
  return `rgb(${m(16)},${m(8)},${m(0)})`;
}
