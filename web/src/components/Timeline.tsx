"use client";

import { useEffect, useRef, useState } from "react";
import type { Trace } from "@/lib/types";

const DEPTH = ["#3a86ff", "#8338ec", "#ff006e", "#fb5607", "#ffbe0b", "#06d6a0"];

/** A scrubbable strip: one column per step, coloured by call depth; marked steps glow. */
export default function Timeline({ trace, step, onSeek, marks }: { trace: Trace; step: number; onSeek: (i: number) => void; marks: Set<number> }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const [hover, setHover] = useState<{ x: number; i: number } | null>(null);
  const dragging = useRef(false);
  const n = trace.steps.length;

  useEffect(() => {
    const c = ref.current;
    if (!c) return;
    const W = Math.max(200, c.clientWidth);
    const H = 28;
    c.width = W;
    c.height = H;
    const g = c.getContext("2d")!;
    g.fillStyle = "#0d0e16";
    g.fillRect(0, 0, W, H);
    if (!n || trace.end.kind === "preview") return;
    const colW = W / n;
    for (let i = 0; i < n; i++) {
      const s = trace.steps[i];
      const d = s.stack.length;
      const h = Math.min(H - 6, 6 + d * 4);
      g.fillStyle = s.error ? "#ef476f" : DEPTH[(d - 1) % DEPTH.length];
      g.globalAlpha = i <= step ? 1 : 0.35;
      g.fillRect(Math.floor(i * colW), H - h, Math.max(1, Math.ceil(colW) - (colW > 3 ? 1 : 0)), h);
      if (marks.has(i)) {
        g.globalAlpha = 1;
        g.fillStyle = "#4cc9f0";
        g.fillRect(Math.floor(i * colW), 0, Math.max(1, Math.ceil(colW)), 4);
      }
    }
    g.globalAlpha = 1;
    const x = Math.floor((step + 0.5) * colW);
    g.fillStyle = "#f5c542";
    g.fillRect(x - 1, 0, 3, H);
  }, [trace, step, n, marks]);

  const at = (e: React.PointerEvent<HTMLCanvasElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    return { x, i: Math.max(0, Math.min(n - 1, Math.floor((x / rect.width) * n))) };
  };

  return (
    <div className="timeline">
      <canvas
        ref={ref}
        onPointerDown={(e) => {
          dragging.current = true;
          e.currentTarget.setPointerCapture(e.pointerId);
          onSeek(at(e).i);
        }}
        onPointerMove={(e) => {
          const p = at(e);
          setHover(p);
          if (dragging.current) onSeek(p.i);
        }}
        onPointerUp={() => (dragging.current = false)}
        onPointerLeave={() => setHover(null)}
      />
      {hover && n > 0 && trace.end.kind !== "preview" && (
        <div className="timeline-tip" style={{ left: hover.x }}>
          step {hover.i + 1} · line {trace.steps[hover.i]?.line} · {trace.steps[hover.i]?.fn}()
        </div>
      )}
    </div>
  );
}
