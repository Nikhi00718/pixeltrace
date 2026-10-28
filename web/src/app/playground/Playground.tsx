"use client";

import { useEffect, useState } from "react";
import SceneCanvas from "@/components/SceneCanvas";
import type { SceneDef, Trace } from "@/lib/types";

const SAMPLES = ["two-pointers", "reverse-list", "invert-tree", "islands"];

/** Replays any trace JSON against any scene definition. Used to author and debug situation files. */
export default function Playground() {
  const [sceneText, setSceneText] = useState("");
  const [traceText, setTraceText] = useState("");
  const [scene, setScene] = useState<SceneDef | null>(null);
  const [trace, setTrace] = useState<Trace | null>(null);
  const [step, setStep] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [err, setErr] = useState("");

  const load = async (name: string) => {
    const r = await fetch(`/samples/${name}.json`);
    const data = await r.json();
    setSceneText(JSON.stringify(data.scene, null, 2));
    setTraceText(JSON.stringify(data.trace));
    setScene(data.scene);
    setTrace(data.trace);
    setStep(0);
    setErr("");
  };

  useEffect(() => {
    let alive = true;
    fetch(`/samples/${SAMPLES[0]}.json`)
      .then((r) => r.json())
      .then((data) => {
        if (!alive) return;
        setSceneText(JSON.stringify(data.scene, null, 2));
        setTraceText(JSON.stringify(data.trace));
        setScene(data.scene);
        setTrace(data.trace);
      });
    return () => {
      alive = false;
    };
  }, []);

  useEffect(() => {
    if (!playing || !trace) return;
    const atEnd = step >= trace.steps.length - 1;
    const t = setTimeout(() => (atEnd ? setPlaying(false) : setStep(step + 1)), atEnd ? 0 : 450);
    return () => clearTimeout(t);
  }, [playing, step, trace]);

  const apply = () => {
    try {
      setScene(JSON.parse(sceneText));
      setTrace(JSON.parse(traceText));
      setStep(0);
      setErr("");
    } catch (e) {
      setErr(String(e));
    }
  };

  const total = trace?.steps.length ?? 0;
  return (
    <div className="playground">
      <div className="pg-left panel">
        <h1>Scene playground</h1>
        <div className="filters">
          {SAMPLES.map((s) => (
            <button key={s} className="chip" onClick={() => load(s)}>
              {s}
            </button>
          ))}
        </div>
        <label className="small">Scene definition</label>
        <textarea value={sceneText} onChange={(e) => setSceneText(e.target.value)} rows={14} spellCheck={false} />
        <label className="small">Trace JSON (the runner&apos;s trace object)</label>
        <textarea value={traceText} onChange={(e) => setTraceText(e.target.value)} rows={8} spellCheck={false} />
        <button className="btn primary" onClick={apply}>
          Apply
        </button>
        {err && <pre className="err">{err}</pre>}
      </div>
      <div className="pg-right">
        <div className="stage panel">{scene && trace && <SceneCanvas trace={trace} def={scene} step={step} speedMs={340} />}</div>
        <div className="controls panel">
          <button className="btn icon" onClick={() => setStep((s) => Math.max(0, s - 1))}>◀</button>
          <button className="btn icon primary" onClick={() => (step >= total - 1 ? (setStep(0), setPlaying(true)) : setPlaying((p) => !p))}>
            {playing ? "⏸" : "▶"}
          </button>
          <button className="btn icon" onClick={() => setStep((s) => Math.min(total - 1, s + 1))}>▶▶</button>
          <input type="range" min={0} max={Math.max(0, total - 1)} value={step} onChange={(e) => setStep(Number(e.target.value))} />
          <span className="counter">
            {step + 1}/{total} · line {trace?.steps[step]?.line ?? "-"}
          </span>
        </div>
      </div>
    </div>
  );
}
