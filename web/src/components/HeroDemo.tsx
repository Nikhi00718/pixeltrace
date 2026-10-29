"use client";

import { useEffect, useState } from "react";
import type { SceneDef, Trace } from "@/lib/types";
import SceneCanvas from "./SceneCanvas";

const DEMOS = [
  { id: "two-pointers", label: "Two pointers", code: "if (s < target) l++; else r--;" },
  { id: "reverse-list", label: "Linked list", code: "curr->next = prev;" },
  { id: "invert-tree", label: "Tree", code: "swap(root->left, root->right);" },
  { id: "islands", label: "Grid DFS", code: "sink(grid, r + 1, c);" },
];

/** Auto-playing scene on the home page, looping through the sample traces. */
export default function HeroDemo() {
  const [which, setWhich] = useState(0);
  const [data, setData] = useState<{ scene: SceneDef; trace: Trace } | null>(null);
  const [step, setStep] = useState(0);

  useEffect(() => {
    let alive = true;
    fetch(`/samples/${DEMOS[which].id}.json`)
      .then((r) => r.json())
      .then((d) => {
        if (!alive) return;
        setData(d);
        setStep(0);
      })
      .catch(() => {});
    return () => {
      alive = false;
    };
  }, [which]);

  useEffect(() => {
    if (!data) return;
    const last = data.trace.steps.length - 1;
    const t = setTimeout(
      () => (step >= last ? setWhich((w) => (w + 1) % DEMOS.length) : setStep(step + 1)),
      step >= last ? 1600 : 420,
    );
    return () => clearTimeout(t);
  }, [data, step]);

  return (
    <div className="hero-demo panel">
      {data ? <SceneCanvas trace={data.trace} def={data.scene} step={step} speedMs={320} /> : <div style={{ aspectRatio: "16 / 9" }} />}
      <div className="hero-demo-caption">
        <code>{DEMOS[which].code}</code>
        <div className="demo-tabs">
          {DEMOS.map((d, i) => (
            <button key={d.id} className={i === which ? "on" : ""} onClick={() => setWhich(i)}>
              {d.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
