"use client";

import { useEffect, useRef, useState } from "react";
import * as D from "@/scene/draw";

export interface MapWorld {
  id: string;
  name: string;
  blurb: string;
  theme: string;
  count: number;
  solved: number;
}

const W = 320;
const H = 168;

// Winding route across the sea; one island per world, in learning order.
const SPOTS: [number, number][] = [
  [30, 40], [74, 28], [118, 44], [160, 30], [204, 42], [250, 28], [292, 46],
  [270, 92], [226, 104], [182, 92], [138, 110], [94, 96], [50, 112], [30, 146],
];

const ICONS: Record<string, string[]> = {
  arrays: ["........", ".kkkkkk.", ".kwwwwk.", ".kkkkkk.", ".kwwwwk.", ".kkkkkk.", "........", "........"],
  "two-pointers": ["........", "r......b", "rr....bb", "r......b", "........", "kkkkkkkk", "k.k..k.k", "........"],
  "sliding-window": ["...yy...", "..yyyy..", "...rr...", "...ww...", "...rr...", "...ww...", "..rrrr..", "........"],
  stack: ["..g..g..", "..gggg..", "..gwwg..", "..gggg..", "..gwwg..", "..gggg..", ".gggggg.", "........"],
  "binary-search": ["..kkkk..", ".k....k.", ".k.yy.k.", ".k.yy.k.", ".k....k.", ".k....k.", ".kkkkkk.", "........"],
  "linked-list": ["........", "........", "rrr.rrr.", "rwr-rwr.", "rrr.rrr.", "k.k.k.k.", "........", "........"],
  trees: ["..ggg...", ".ggrgg..", "ggggrgg.", ".grggg..", "..ggg...", "...k....", "...k....", "........"],
  heap: ["...y....", "..yyy...", ".yyyyy..", "yyyyyyy.", "........", "........", "........", "........"],
  graphs: [".r....b.", "..\\..//.", "...yy...", "...yy...", "../..\\..", ".g....r.", "........", "........"],
  backtracking: ["..kkkk..", ".kbbbbk.", ".kbbbbk.", ".kbbybk.", ".kbbbbk.", ".kbbbbk.", ".kkkkkk.", "........"],
  dp: ["........", "y.y.y.y.", "gygygyg.", "gggggggg", "kkkkkkkk", "kgkgkgkg", "........", "........"],
  intervals: [".kkkkkk.", ".rrrrrr.", ".kwwwwk.", ".kwbwwk.", ".kwwwwk.", ".kkkkkk.", "........", "........"],
  greedy: [".rrrrrr.", ".rwwwwr.", ".rwyywr.", ".rwwwwr.", ".rrrrrr.", ".r....r.", "........", "........"],
  bits: ["...yy...", "..yyyy..", "..yyyy..", "...yy...", "...kk...", "..kkkk..", "........", "........"],
};
const ICON_PAL = { k: "#5a3a22", w: "#f5ebd7", r: "#d62828", b: "#3b82f6", y: "#f5c542", g: "#2f6b3a", "-": "#1b1b2a", "/": "#6d597a", "\\": "#6d597a" };

export default function WorldMap({ worlds, selected, onSelect }: { worlds: MapWorld[]; selected: string; onSelect: (id: string) => void }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const state = useRef({ hover: -1, sel: 0, heroX: SPOTS[0][0], heroY: SPOTS[0][1] - 6, fromX: 0, fromY: 0, t0: 0, moving: false });
  const [label, setLabel] = useState<{ x: number; y: number; w: MapWorld } | null>(null);

  useEffect(() => {
    const idx = worlds.findIndex((w) => w.id === selected);
    const s = state.current;
    if (idx >= 0 && idx !== s.sel) {
      s.fromX = s.heroX;
      s.fromY = s.heroY;
      s.sel = idx;
      s.t0 = performance.now();
      s.moving = true;
    }
  }, [selected, worlds]);

  useEffect(() => {
    const css = getComputedStyle(document.documentElement).getPropertyValue("--font-pixel").trim();
    D.setFont(css || "monospace");
    const c = ref.current!;
    const S = 3;
    c.width = W * S;
    c.height = H * S;
    const g = c.getContext("2d")!;
    let raf = 0;
    const loop = (now: number) => {
      raf = requestAnimationFrame(loop);
      g.setTransform(S, 0, 0, S, 0, 0);
      g.imageSmoothingEnabled = false;
      // sea
      g.fillStyle = "#1d4e89";
      g.fillRect(0, 0, W, H);
      for (let y = 4; y < H; y += 9) {
        for (let x = (y * 7) % 23; x < W; x += 23) {
          const o = Math.floor(now / 400 + x + y) % 3;
          D.rect(g, x + o, y, 4, 1, "#3a7bd5");
        }
      }
      const n = Math.min(worlds.length, SPOTS.length);
      // path
      for (let k = 0; k + 1 < n; k++) {
        const [x1, y1] = SPOTS[k];
        const [x2, y2] = SPOTS[k + 1];
        const steps = Math.ceil(Math.hypot(x2 - x1, y2 - y1) / 4);
        for (let i = 1; i < steps; i += 2) D.rect(g, x1 + ((x2 - x1) * i) / steps, y1 + 2 + ((y2 - y1) * i) / steps, 2, 2, "#f5ebd7");
      }
      // islands
      const s = state.current;
      for (let k = 0; k < n; k++) {
        const [x, y] = SPOTS[k];
        const w = worlds[k];
        const theme = D.THEMES[w.theme] ?? D.THEMES.dock;
        const hov = s.hover === k || s.sel === k;
        D.rect(g, x - 15, y - 3, 30, 12, "#e9d8a6");
        D.rect(g, x - 13, y - 6, 26, 12, hov ? "#7bc96f" : "#5a9e4b");
        D.rect(g, x - 10, y - 8, 20, 4, hov ? "#7bc96f" : "#5a9e4b");
        D.rect(g, x - 13, y + 5, 26, 1, "#3f7a35");
        D.pix(g, ICONS[w.id] ?? ICONS.arrays, x - 4, y - 9, ICON_PAL);
        if (w.count && w.solved >= w.count) {
          D.rect(g, x + 9, y - 14, 1, 9, "#5a3a22");
          D.rect(g, x + 10, y - 14, 5, 3, "#f5c542");
        } else if (w.solved) {
          D.text(g, `${w.solved}/${w.count}`, x, y + 12, { size: 4, color: "#fff", shadow: "#000" });
        }
        if (hov) {
          const pulse = Math.floor(now / 250) % 2 ? "#fff" : theme.accent;
          D.rect(g, x - 15, y - 11, 30, 1, pulse);
        }
      }
      // hero walks to the selected island
      const [tx, ty] = SPOTS[Math.min(s.sel, n - 1)];
      let walking = false;
      if (s.moving) {
        const k = Math.min(1, (now - s.t0) / 700);
        s.heroX = s.fromX + (tx - s.fromX) * k;
        s.heroY = s.fromY + (ty - 6 - s.fromY) * k;
        walking = k < 1;
        if (k >= 1) s.moving = false;
      } else {
        s.heroX = tx;
        s.heroY = ty - 6 + (Math.floor(now / 500) % 2 ? -1 : 0);
      }
      D.hero(g, s.heroX - 8, s.heroY, "#e8534a", walking, now, s.heroX < tx);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [worlds]);

  const at = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const r = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - r.left) / r.width) * W;
    const y = ((e.clientY - r.top) / r.height) * H;
    const k = SPOTS.slice(0, worlds.length).findIndex(([sx, sy]) => Math.abs(sx - x) < 16 && Math.abs(sy - y) < 12);
    return { k, px: e.clientX - r.left, py: e.clientY - r.top };
  };

  return (
    <div className="worldmap">
      <canvas
        ref={ref}
        className="worldmap-canvas"
        onMouseMove={(e) => {
          const p = at(e);
          state.current.hover = p.k;
          e.currentTarget.style.cursor = p.k >= 0 ? "pointer" : "default";
          setLabel(p.k >= 0 ? { x: p.px, y: p.py, w: worlds[p.k] } : null);
        }}
        onMouseLeave={() => {
          state.current.hover = -1;
          setLabel(null);
        }}
        onClick={(e) => {
          const p = at(e);
          if (p.k >= 0) onSelect(worlds[p.k].id);
        }}
      />
      {label && (
        <div className="map-tip" style={{ left: label.x, top: label.y }}>
          <b>{label.w.name}</b>
          <span>{label.w.blurb}</span>
          <span>
            {label.w.solved}/{label.w.count} cleared
          </span>
        </div>
      )}
    </div>
  );
}
