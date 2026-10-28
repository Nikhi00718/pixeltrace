"use client";

import { useEffect, useRef, useState } from "react";
import type { SceneDef, Trace } from "@/lib/types";
import { setFont } from "@/scene/draw";
import type { Ent } from "@/scene/layers";
import { Renderer, Scene } from "@/scene/scene";

interface Props {
  trace: Trace;
  def: SceneDef;
  step: number;
  speedMs: number;
  onPick?: (ent: Ent) => void;
}

export default function SceneCanvas({ trace, def, step, speedMs, onPick }: Props) {
  const ref = useRef<HTMLCanvasElement>(null);
  const renderer = useRef<Renderer | null>(null);
  const scene = useRef<Scene | null>(null);
  const lastStep = useRef(0);
  const [tip, setTip] = useState<{ x: number; y: number; text: string } | null>(null);

  useEffect(() => {
    const css = getComputedStyle(document.documentElement).getPropertyValue("--font-pixel").trim();
    setFont(css || "monospace");
    renderer.current = new Renderer(ref.current!);
    return () => renderer.current?.destroy();
  }, []);

  useEffect(() => {
    const s = new Scene(trace, def);
    scene.current = s;
    renderer.current?.setScene(s);
    renderer.current?.show(Math.min(step, s.length - 1), false);
    lastStep.current = step;
    // step is applied by the next effect; only rebuild when trace/def change
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [trace, def]);

  useEffect(() => {
    renderer.current?.setSpeed(speedMs);
  }, [speedMs]);

  useEffect(() => {
    const s = scene.current;
    if (!s) return;
    const i = Math.max(0, Math.min(step, s.length - 1));
    renderer.current?.show(i, Math.abs(i - lastStep.current) <= 2);
    lastStep.current = i;
  }, [step]);

  const pick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const r = renderer.current;
    if (!r) return null;
    const rect = e.currentTarget.getBoundingClientRect();
    const { w, h } = r.size;
    const x = ((e.clientX - rect.left) / rect.width) * w;
    const y = ((e.clientY - rect.top) / rect.height) * h;
    return { ent: r.hitTest(x, y), px: e.clientX - rect.left, py: e.clientY - rect.top };
  };

  return (
    <div className="scene-wrap">
      <canvas
        ref={ref}
        className="scene-canvas"
        aria-label="Pixel-art animation of the running code"
        onMouseMove={(e) => {
          const p = pick(e);
          renderer.current?.setHover(p?.ent?.id ?? null);
          setTip(p?.ent?.tip ? { x: p.px, y: p.py, text: p.ent.tip } : null);
          e.currentTarget.style.cursor = p?.ent ? "pointer" : "default";
        }}
        onMouseLeave={() => {
          renderer.current?.setHover(null);
          setTip(null);
        }}
        onClick={(e) => {
          const p = pick(e);
          if (p?.ent && onPick) onPick(p.ent);
        }}
      />
      {tip && (
        <div className="scene-tip" style={{ left: tip.x, top: tip.y }}>
          {tip.text}
        </div>
      )}
    </div>
  );
}
