"use client";

import Editor, { type OnMount } from "@monaco-editor/react";
import Link from "next/link";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { lineHits, narrate, stepsOnLine } from "@/lib/narrate";
import { previewTrace } from "@/lib/preview";
import { markOpened, markSolved } from "@/lib/progress";
import { setSound, sfx, soundPref } from "@/lib/sound";
import type { Problem, RunResponse, Trace } from "@/lib/types";
import { isPtr, pretty } from "@/lib/values";
import type { Ent } from "@/scene/layers";
import SceneCanvas from "./SceneCanvas";
import Timeline from "./Timeline";

type Monaco = Parameters<OnMount>[1];
type EditorT = Parameters<OnMount>[0];

const SPEEDS = [
  { label: "🐢", ms: 900 },
  { label: "1x", ms: 450 },
  { label: "2x", ms: 220 },
  { label: "⚡", ms: 90 },
];

const WORLD_NAMES: Record<string, string> = {
  arrays: "Harbor Docks", "two-pointers": "Twin Piers", "sliding-window": "Lighthouse Beam", stack: "Tower Yard",
  "binary-search": "Guarded Corridor", "linked-list": "Rail Yard", trees: "Orchard Forest", heap: "Pyramid Market",
  graphs: "Kingdom Roads", backtracking: "Door Maze", dp: "Farmlands", intervals: "Calendar Hall", greedy: "Vending Street", bits: "Lamp Room",
};

export default function Workspace({ problem, starter }: { problem: Problem; starter: string }) {
  const storageKey = `pixeltrace:code:${problem.slug}`;
  const [code, setCode] = useState(starter);
  const [running, setRunning] = useState(false);
  const [res, setRes] = useState<RunResponse | null>(null);
  const [trace, setTrace] = useState<Trace>(() => previewTrace(problem, problem.visualTest ?? 0));
  const [step, setStep] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [testIdx, setTestIdx] = useState(problem.visualTest ?? 0);
  const [custom, setCustom] = useState(() => JSON.stringify(problem.tests[problem.visualTest ?? 0]?.args ?? []));
  const [tab, setTab] = useState<"quest" | "levels" | "console">("quest");
  const [sound, setSoundState] = useState(false);
  const [cleared, setCleared] = useState(false);
  const [focusLine, setFocusLine] = useState<number | null>(null);
  const [picked, setPicked] = useState<string | null>(null);
  const editorRef = useRef<EditorT | null>(null);
  const monacoRef = useRef<Monaco | null>(null);
  const decoRef = useRef<string[]>([]);
  const traceRef = useRef(trace);
  const restored = useRef(false);
  const stepRef = useRef(step);

  useEffect(() => {
    traceRef.current = trace;
    stepRef.current = step;
  });

  useEffect(() => {
    markOpened(problem.slug);
  }, [problem.slug]);

  useEffect(() => {
    if (!restored.current) return; // don't overwrite saved code with the starter before it is restored
    try {
      localStorage.setItem(storageKey, code);
    } catch {}
  }, [code, storageKey]);

  const total = trace.steps.length;
  const cur = trace.steps[Math.min(step, total - 1)];
  const prevStep = trace.steps[Math.min(step, total - 1) - 1];
  const isPreview = trace.end.kind === "preview";
  const story = useMemo(() => narrate(trace, Math.min(step, total - 1)), [trace, step, total]);
  const hits = useMemo(() => (isPreview ? new Map<number, number>() : lineHits(trace)), [trace, isPreview]);
  const marks = useMemo(() => new Set(focusLine ? stepsOnLine(trace, focusLine) : []), [trace, focusLine]);

  // playback
  useEffect(() => {
    if (!playing) return;
    const atEnd = step >= total - 1;
    const t = setTimeout(() => (atEnd ? setPlaying(false) : setStep(step + 1)), atEnd ? 0 : SPEEDS[speed].ms);
    return () => clearTimeout(t);
  }, [playing, step, total, speed]);

  // sound on step
  useEffect(() => {
    if (isPreview || !cur) return;
    if (cur.error) sfx.crash();
    else if (prevStep && cur.stack.length > prevStep.stack.length) sfx.call();
    else if (playing) sfx.step(cur.line);
  }, [cur, prevStep, isPreview, playing]);

  // editor decorations: current line, hit counts
  useEffect(() => {
    const ed = editorRef.current;
    const m = monacoRef.current;
    if (!ed || !m) return;
    const line = !isPreview && cur ? cur.line : 0;
    const decos: Parameters<EditorT["deltaDecorations"]>[1] = [];
    if (line) {
      decos.push({
        range: new m.Range(line, 1, line, 1),
        options: { isWholeLine: true, className: cur?.error ? "line-crash" : "line-active", glyphMarginClassName: cur?.error ? "glyph-crash" : "glyph-here" },
      });
    }
    const model = ed.getModel();
    for (const [ln, n] of hits) {
      if (!model || ln > model.getLineCount()) continue;
      const endCol = model.getLineMaxColumn(ln);
      decos.push({
        range: new m.Range(ln, endCol, ln, endCol),
        options: { afterContentClassName: `hit-count hit-${Math.min(n, 999)}${ln === focusLine ? " focus" : ""}` },
      });
    }
    // Monaco cannot put per-line text in afterContent, so each count gets its own tiny CSS rule.
    let style = document.getElementById("hit-styles");
    if (!style) {
      style = document.createElement("style");
      style.id = "hit-styles";
      document.head.appendChild(style);
    }
    style.textContent = [...new Set([...hits.values()].map((n) => Math.min(n, 999)))]
      .map((n) => `.hit-${n}::after{content:"  ×${n}"}`)
      .join(" ");
    decoRef.current = ed.deltaDecorations(decoRef.current, decos);
    if (line) ed.revealLineInCenterIfOutsideViewport(line);
  }, [cur, isPreview, hits, focusLine]);

  // compile error markers
  useEffect(() => {
    const ed = editorRef.current;
    const m = monacoRef.current;
    const model = ed?.getModel();
    if (!ed || !m || !model) return;
    const errs = res?.compile?.errors ?? [];
    m.editor.setModelMarkers(
      model,
      "g++",
      errs.map((e) => ({ startLineNumber: e.line, startColumn: e.col, endLineNumber: e.line, endColumn: e.col + 1, message: e.message, severity: m.MarkerSeverity.Error })),
    );
  }, [res]);

  const run = useCallback(
    async (traceIndex: number, customArgs: unknown[] | null = null) => {
      setRunning(true);
      setPlaying(false);
      setCleared(false);
      setFocusLine(null);
      try {
        const r = await fetch("/api/run", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ slug: problem.slug, code, trace: traceIndex, custom: customArgs }),
        });
        const data = (await r.json()) as RunResponse;
        setRes(data);
        if (data.trace && data.trace.steps.length) {
          setTrace(data.trace);
          setStep(0);
          setPlaying(true);
        }
        const official = (data.results ?? []).slice(0, problem.tests.length);
        const allPass = official.length === problem.tests.length && official.every((x) => x.passed);
        if (allPass) {
          markSolved(problem.slug);
          setCleared(true);
          sfx.clear();
        } else if (data.results?.length) sfx.fail();
        setTab(data.fatal || (data.compile && !data.compile.ok) ? "console" : "levels");
      } catch (e) {
        setRes({ fatal: String(e) });
        setTab("console");
      } finally {
        setRunning(false);
      }
    },
    [code, problem.slug, problem.tests.length],
  );

  const runCustom = () => {
    try {
      const args = JSON.parse(custom);
      if (!Array.isArray(args)) throw new Error("not an array");
      setTestIdx(problem.tests.length);
      run(problem.tests.length, args);
    } catch {
      setRes({ fatal: "Custom input must be a JSON array of arguments, e.g. [[2,7,11,15], 9]" });
      setTab("console");
    }
  };

  const jumpToLine = (line: number) => {
    const t = traceRef.current;
    if (t.end.kind === "preview") return;
    const list = stepsOnLine(t, line);
    if (!list.length) return;
    setFocusLine(line);
    setPlaying(false);
    const next = list.find((i) => i > stepRef.current) ?? list[0];
    setStep(next);
  };

  const onMount: OnMount = (ed, m) => {
    editorRef.current = ed;
    monacoRef.current = m;
    m.editor.defineTheme("pixel", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "keyword", foreground: "f5c542" },
        { token: "type", foreground: "4cc9f0" },
        { token: "number", foreground: "06d6a0" },
        { token: "comment", foreground: "6b6f94", fontStyle: "italic" },
        { token: "string", foreground: "ff8fab" },
      ],
      colors: {
        "editor.background": "#14152299",
        "editor.lineHighlightBackground": "#1f2135",
        "editorLineNumber.foreground": "#4a4f73",
        "editorLineNumber.activeForeground": "#f5c542",
        "editorGutter.background": "#101120",
      },
    });
    m.editor.setTheme("pixel");
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) setCode(saved);
    } catch {}
    restored.current = true;
    setSoundState(soundPref());
    setSound(soundPref());
    ed.addCommand(m.KeyMod.CtrlCmd | m.KeyCode.Enter, () => document.getElementById("run-btn")?.click());
    ed.onMouseDown((e) => {
      const t = e.target.type;
      const ln = e.target.position?.lineNumber;
      if (ln && (t === m.editor.MouseTargetType.GUTTER_GLYPH_MARGIN || t === m.editor.MouseTargetType.GUTTER_LINE_NUMBERS)) jumpToLine(ln);
    });
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const el = e.target as HTMLElement;
      if (el.closest(".monaco-editor") || el.tagName === "TEXTAREA" || el.tagName === "INPUT") return;
      if (e.key === "ArrowRight") setStep((s) => Math.min(s + 1, total - 1));
      else if (e.key === "ArrowLeft") setStep((s) => Math.max(s - 1, 0));
      else if (e.key === "Home") setStep(0);
      else if (e.key === "End") setStep(total - 1);
      else if (e.key === " ") {
        e.preventDefault();
        setPlaying((p) => !p);
      } else return;
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [total]);

  const onPick = (ent: Ent) => {
    setPicked(ent.tip ?? null);
    setPlaying(false);
  };

  const results = res?.results ?? [];
  const passed = results.filter((r, i) => i < problem.tests.length && r.passed).length;
  const top = cur?.stack[cur.stack.length - 1];
  const scene = useMemo(() => problem.scene, [problem.scene]);
  const crashed = !!cur?.error;

  return (
    <div className="ws">
      <header className="hud">
        <Link href="/" className="hud-back" title="Back to the world map">◀ MAP</Link>
        <span className="hud-world">{WORLD_NAMES[problem.world] ?? problem.world}</span>
        <h1 className="hud-title">
          <span className="pid">#{problem.id}</span> {problem.title}
        </h1>
        <span className={`diff diff-${problem.difficulty.toLowerCase()}`}>{problem.difficulty}</span>
        <div className="hearts" title={results.length ? `${passed}/${problem.tests.length} levels cleared` : "Run to test"}>
          {problem.tests.map((_, i) => (
            <span key={i} className={`heart ${results[i] ? (results[i].passed ? "full" : "broken") : ""}`} />
          ))}
        </div>
        <button
          className={`hud-btn ${sound ? "on" : ""}`}
          onClick={() => {
            setSound(!sound);
            setSoundState(!sound);
          }}
          title="8-bit sound"
        >
          {sound ? "♪ ON" : "♪ OFF"}
        </button>
      </header>

      <div className="ws-grid">
        <section className="ws-code">
          <div className="quest panel">
            <div className="tabs">
              {(
                [
                  ["quest", "📜 Quest"],
                  ["levels", results.length ? `🎯 Levels ${passed}/${problem.tests.length}` : "🎯 Levels"],
                  ["console", "🖥 Console"],
                ] as const
              ).map(([t, label]) => (
                <button key={t} className={tab === t ? "tab on" : "tab"} onClick={() => setTab(t)}>
                  {label}
                </button>
              ))}
            </div>
            <div className="tabbody">
              {tab === "quest" && (
                <div className="story">
                  <h2>{problem.story.title}</h2>
                  <p>{problem.story.text}</p>
                  <p className="goal">
                    <b>🎯 Goal</b> {problem.story.goal}
                  </p>
                  <div className="sig">
                    <code>
                      {problem.spec.ret} {problem.spec.method}({problem.spec.params.map(([t, n]) => `${t} ${n}`).join(", ")})
                    </code>
                  </div>
                  {problem.legend?.length ? (
                    <ul className="legend">
                      {problem.legend.map((l) => (
                        <li key={l.sprite}>
                          <b>{l.sprite}</b> {l.meaning}
                        </li>
                      ))}
                    </ul>
                  ) : null}
                  {problem.hints?.length ? (
                    <details>
                      <summary>💡 Hints ({problem.hints.length})</summary>
                      <ol>
                        {problem.hints.map((h) => (
                          <li key={h}>{h}</li>
                        ))}
                      </ol>
                    </details>
                  ) : null}
                  <details>
                    <summary>🗝 Reference solution (spoiler)</summary>
                    <pre className="code">{problem.reference}</pre>
                    <button className="btn small" onClick={() => setCode(problem.reference)}>
                      Load into editor
                    </button>
                  </details>
                  <p className="small">
                    Practice the original: <a href={`https://leetcode.com/problems/${problem.slug}/`} target="_blank" rel="noreferrer">LeetCode {problem.id}</a> ·{" "}
                    {problem.tags.join(" · ")}
                  </p>
                </div>
              )}
              {tab === "levels" && (
                <div className="tests">
                  {problem.tests.map((t, i) => {
                    const r = results[i];
                    return (
                      <div key={i} className={`test ${r ? (r.passed ? "pass" : "fail") : ""} ${testIdx === i && !isPreview ? "watching" : ""}`}>
                        <div className="test-head">
                          <b>{t.name ?? `Level ${i + 1}`}</b>
                          {r && <span className="badge">{r.passed ? "CLEAR" : r.error ?? "WRONG"}</span>}
                          <button className="btn small" disabled={running} onClick={() => { setTestIdx(i); run(i); }}>
                            {testIdx === i && !isPreview ? "👁 watching" : "▶ watch"}
                          </button>
                        </div>
                        <div className="kv">
                          {problem.spec.params.map(([, n], k) => (
                            <div key={n}>
                              <span>{n}</span> = {JSON.stringify(t.args[k])}
                            </div>
                          ))}
                          <div>
                            <span>expected</span> = {JSON.stringify(t.expected)}
                          </div>
                          {r && (
                            <div>
                              <span>yours</span> = {r.output === undefined || r.output === null ? "—" : JSON.stringify(r.output)} <i>({r.ms} ms)</i>
                            </div>
                          )}
                          {r?.stdout ? <pre className="stdout">{r.stdout}</pre> : null}
                        </div>
                      </div>
                    );
                  })}
                  <div className="test custom">
                    <div className="test-head">
                      <b>🧪 Custom level</b>
                      {results[problem.tests.length] && (
                        <span className="badge">{results[problem.tests.length].passed ? "MATCHES REF" : results[problem.tests.length].error ?? "DIFFERS"}</span>
                      )}
                    </div>
                    <textarea value={custom} onChange={(e) => setCustom(e.target.value)} spellCheck={false} rows={2} />
                    <div className="small">JSON array: {problem.spec.params.map(([t, n]) => `${n}: ${t}`).join(", ")}</div>
                    {results[problem.tests.length] && (
                      <div className="kv">
                        <div>
                          <span>reference</span> = {JSON.stringify(results[problem.tests.length].expected)}
                        </div>
                        <div>
                          <span>yours</span> = {JSON.stringify(results[problem.tests.length].output)}
                        </div>
                      </div>
                    )}
                    <button className="btn small" disabled={running} onClick={runCustom}>
                      ▶ Run &amp; watch custom
                    </button>
                  </div>
                </div>
              )}
              {tab === "console" && (
                <div className="output">
                  {res?.fatal && <pre className="err">{res.fatal}</pre>}
                  {res?.compile && !res.compile.ok && (
                    <>
                      <h3>Compile error</h3>
                      <pre className="err">{res.compile.raw}</pre>
                    </>
                  )}
                  {res?.compile?.ok && <p>✔ Compiled in {res.compile.ms} ms.</p>}
                  {results.map((r) => (r.stderr ? <pre key={r.i} className="err">{`Level ${r.i + 1}: ${r.stderr}`}</pre> : null))}
                  {results.some((r) => r.stdout) && (
                    <>
                      <h3 className="ok">Your cout</h3>
                      {results.map((r) => (r.stdout ? <pre key={r.i} className="stdout">{`[level ${r.i + 1}] ${r.stdout}`}</pre> : null))}
                    </>
                  )}
                  {res?.trace && (
                    <p className="small">
                      Trace: {res.trace.steps.length} steps{res.trace.truncated ? " (truncated)" : ""} · ended by {res.trace.end.kind}
                      {res.trace.end.signal ? ` ${res.trace.end.signal}` : ""}
                      {res.trace.ms ? ` · ${res.trace.ms} ms in gdb` : ""}
                    </p>
                  )}
                  {!res && <p className="small">Compiler messages, crashes and your cout show up here.</p>}
                </div>
              )}
            </div>
          </div>

          <div className="editor-wrap">
            <div className="editor-bar">
              <span className="small">C++17 · click a line number to jump to when it runs</span>
              <div>
                <button className="btn ghost small" onClick={() => setCode(starter)}>
                  Reset
                </button>
                <button id="run-btn" className="btn primary run" disabled={running} onClick={() => run(testIdx < problem.tests.length ? testIdx : problem.visualTest ?? 0)}>
                  {running ? <span className="spin">◐</span> : "▶"} {running ? "Compiling…" : "Run & watch"}
                </button>
              </div>
            </div>
            <div className="editor-body">
              <Editor
                height="100%"
                defaultLanguage="cpp"
                theme="vs-dark"
                value={code}
                onChange={(v) => setCode(v ?? "")}
                onMount={onMount}
                options={{
                  fontSize: 14,
                  minimap: { enabled: false },
                  glyphMargin: true,
                  scrollBeyondLastLine: false,
                  fontFamily: "var(--font-mono), monospace",
                  tabSize: 4,
                  automaticLayout: true,
                  renderLineHighlight: "line",
                  padding: { top: 8 },
                }}
              />
            </div>
          </div>
        </section>

        <section className="ws-stage">
          <div className={`stage panel ${crashed ? "shake" : ""}`}>
            <SceneCanvas trace={trace} def={scene} step={step} speedMs={Math.round(SPEEDS[speed].ms * 0.75)} onPick={onPick} />
            {isPreview && !running && (
              <div className="stage-hint">
                <span className="blink">▶</span> Starting scene for {problem.tests[testIdx]?.name ?? `level ${testIdx + 1}`}. Write your code and press Run.
              </div>
            )}
            {running && (
              <div className="stage-loading">
                <div className="loader-bar" />
                <span>compiling with g++ · walking every line with gdb…</span>
              </div>
            )}
            {cleared && (
              <div className="clear-overlay" onClick={() => setCleared(false)}>
                <div className="confetti">
                  {Array.from({ length: 24 }, (_, k) => (
                    <i key={k} style={{ left: `${(k * 37) % 100}%`, animationDelay: `${(k % 8) * 0.12}s`, background: ["#f5c542", "#4cc9f0", "#ef476f", "#06d6a0"][k % 4] }} />
                  ))}
                </div>
                <div className="clear-card">
                  <div className="clear-title">LEVEL CLEAR!</div>
                  <div className="stars">★ ★ ★</div>
                  <div className="small">All {problem.tests.length} levels passed. The replay keeps playing behind this — click to watch.</div>
                  <Link href="/" className="btn primary small" onClick={(e) => e.stopPropagation()}>
                    Back to map
                  </Link>
                </div>
              </div>
            )}
          </div>

          <div className="narrator panel">
            <div className="owl" aria-hidden>
              <svg viewBox="0 0 10 10" width="36" height="36" shapeRendering="crispEdges">
                <rect x="2" y="1" width="6" height="7" fill="#8d6e63" />
                <rect x="1" y="0" width="2" height="2" fill="#8d6e63" />
                <rect x="7" y="0" width="2" height="2" fill="#8d6e63" />
                <rect x="2" y="2" width="3" height="3" fill="#fff" />
                <rect x="5" y="2" width="3" height="3" fill="#fff" />
                <rect x="3" y="3" width="1" height="1" fill="#1b1b2a" />
                <rect x="6" y="3" width="1" height="1" fill="#1b1b2a" />
                <rect x="4" y="5" width="2" height="1" fill="#f5c542" />
                <rect x="3" y="6" width="4" height="2" fill="#d7ccc8" />
                <rect x="3" y="8" width="1" height="1" fill="#f5c542" />
                <rect x="6" y="8" width="1" height="1" fill="#f5c542" />
              </svg>
            </div>
            <div className="bubble" key={`${step}-${total}`}>
              {isPreview ? (
                <p>Hoo! I narrate every step. Press <b>Run &amp; watch</b>, then hover any sprite to inspect it, or click a line number to jump to it.</p>
              ) : (
                story.map((s, k) => (
                  <p key={k}>
                    {s}
                  </p>
                ))
              )}
              {picked && !isPreview && (
                <p className="picked">
                  🔍 {picked} <button className="x" onClick={() => setPicked(null)}>×</button>
                </p>
              )}
            </div>
          </div>

          <div className="gamepad panel">
            <div className="pad-buttons">
              <button className="pad" onClick={() => setStep(0)} disabled={isPreview} title="First (Home)">⏮</button>
              <button className="pad" onClick={() => setStep((s) => Math.max(0, s - 1))} disabled={isPreview} title="Back (←)">◀</button>
              <button className="pad big" onClick={() => (step >= total - 1 ? (setStep(0), setPlaying(true)) : setPlaying((p) => !p))} disabled={isPreview} title="Play / pause (space)">
                {playing ? "❚❚" : "▶"}
              </button>
              <button className="pad" onClick={() => setStep((s) => Math.min(total - 1, s + 1))} disabled={isPreview} title="Forward (→)">▶</button>
              <button className="pad" onClick={() => setStep(total - 1)} disabled={isPreview} title="Last (End)">⏭</button>
            </div>
            <Timeline trace={trace} step={step} marks={marks} onSeek={(i) => { setPlaying(false); setStep(i); }} />
            <div className="pad-right">
              <span className="counter">{isPreview ? "READY" : `${step + 1}/${total}`}</span>
              <div className="speeds">
                {SPEEDS.map((s, i) => (
                  <button key={s.label} className={speed === i ? "spd on" : "spd"} onClick={() => setSpeed(i)} title={`${s.ms} ms per step`}>
                    {s.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="inspect panel">
            <div className="inspect-col">
              <h3>
                Variables {top ? <small>in {top.fn}() · line {top.line}</small> : null}
              </h3>
              <table>
                <tbody>
                  {top &&
                    Object.entries(top.vars).map(([k, v]) => {
                      const before = prevStep?.stack[cur.stack.length - 1]?.vars[k];
                      const changed = !isPreview && prevStep && prevStep.stack.length === cur.stack.length && JSON.stringify(before) !== JSON.stringify(v);
                      return (
                        <tr key={k} className={changed ? "changed" : ""}>
                          <td className="vn">{k}</td>
                          <td className="vv">{isPtr(v) && cur.nodes[v.$p] ? `→ node ${pretty(cur.nodes[v.$p].val)}` : pretty(v)}</td>
                        </tr>
                      );
                    })}
                </tbody>
              </table>
            </div>
            <div className="inspect-col narrow">
              <h3>Call stack</h3>
              <ol className="calls">
                {cur?.stack
                  .slice()
                  .reverse()
                  .map((f, i) => (
                    <li key={i} className={i === 0 ? "on" : ""}>
                      {f.fn}() <small>:{f.line}</small>
                    </li>
                  ))}
              </ol>
              {res?.trace?.truncated && <p className="small warn">Stopped after {total} steps.</p>}
              <p className="keys small">
                <kbd>←</kbd>
                <kbd>→</kbd> step · <kbd>space</kbd> play · <kbd>Ctrl</kbd>+<kbd>↵</kbd> run
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
