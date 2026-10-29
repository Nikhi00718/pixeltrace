"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { loadProgress, type Progress } from "@/lib/progress";
import type { ProblemSummary } from "@/lib/types";
import WorldMap from "./WorldMap";

interface World {
  id: string;
  name: string;
  blurb: string;
  theme: string;
  count: number;
}

export default function ProblemBrowser({ problems, worlds }: { problems: ProblemSummary[]; worlds: World[] }) {
  const [q, setQ] = useState("");
  const [diff, setDiff] = useState("All");
  const [world, setWorld] = useState(worlds[0]?.id ?? "");
  const [progress, setProgress] = useState<Progress>({ solved: {} });

  useEffect(() => {
    const t = setTimeout(() => setProgress(loadProgress()), 0);
    return () => clearTimeout(t);
  }, []);

  const mapWorlds = useMemo(
    () => worlds.map((w) => ({ ...w, solved: problems.filter((p) => p.world === w.id && progress.solved[p.slug]).length })),
    [worlds, problems, progress],
  );
  const solvedCount = problems.filter((p) => progress.solved[p.slug]).length;
  const searching = q.trim() !== "" || diff !== "All";
  const shown = useMemo(() => {
    const s = q.trim().toLowerCase();
    const rank = { Easy: 0, Medium: 1, Hard: 2 } as const;
    return problems
      .filter(
      (p) =>
        (diff === "All" || p.difficulty === diff) &&
        (searching ? true : p.world === world) &&
        (!s || p.title.toLowerCase().includes(s) || String(p.id) === s || p.tags.some((t) => t.includes(s)) || p.storyTitle.toLowerCase().includes(s)),
      )
      .sort((a, b) => (searching ? a.id - b.id : rank[a.difficulty] - rank[b.difficulty] || a.id - b.id));
  }, [problems, q, diff, world, searching]);
  const cur = worlds.find((w) => w.id === world);
  const last = progress.last ? problems.find((p) => p.slug === progress.last) : undefined;
  const level = Math.floor(solvedCount / 3) + 1;
  const xp = ((solvedCount % 3) / 3) * 100;

  return (
    <section className="browser" id="worlds" style={{ display: "flex", flexDirection: "column", gap: 22 }}>
      <div className="player-card panel">
        <div className="avatar" aria-hidden>
          <svg viewBox="0 0 8 12" width="32" height="48" shapeRendering="crispEdges">
            <rect x="2" y="0" width="4" height="2" fill="#3b2416" />
            <rect x="1" y="1" width="6" height="1" fill="#3b2416" />
            <rect x="1" y="2" width="6" height="3" fill="#f2c9a0" />
            <rect x="2" y="3" width="1" height="1" fill="#1b1b2a" />
            <rect x="5" y="3" width="1" height="1" fill="#1b1b2a" />
            <rect x="1" y="6" width="6" height="3" fill="#e8534a" />
            <rect x="2" y="9" width="4" height="1" fill="#2d3a5a" />
            <rect x="1" y="10" width="2" height="2" fill="#1b1b2a" />
            <rect x="5" y="10" width="2" height="2" fill="#1b1b2a" />
          </svg>
        </div>
        <div className="player-info">
          <div className="lvl">LV {level} CODER</div>
          <div className="xp">
            <div className="xp-fill" style={{ width: `${xp}%` }} />
          </div>
          <div className="small">
            {solvedCount}/{problems.length} levels cleared · next level every 3 clears
          </div>
        </div>
        {last && (
          <Link href={`/problems/${last.slug}`} className="btn primary continue">
            ▶ Continue: {last.title}
          </Link>
        )}
      </div>

      <div>
        <div className="section-title">
          <h2>Choose an island</h2>
          <span className="small">Each world is one pattern. Click an island to walk there.</span>
        </div>
        <WorldMap worlds={mapWorlds} selected={world} onSelect={(id) => { setWorld(id); setQ(""); setDiff("All"); }} />
      </div>

      <div className="filters">
        <input placeholder="🔎 Search every world: title, number, tag…" value={q} onChange={(e) => setQ(e.target.value)} />
        {["All", "Easy", "Medium", "Hard"].map((d) => (
          <button key={d} className={diff === d ? "chip on" : "chip"} onClick={() => setDiff(d)}>
            {d}
          </button>
        ))}
      </div>

      <div className="world-head">
        <h2>{searching ? `Search results (${shown.length})` : cur?.name}</h2>
        {!searching && cur && <span className="small">{cur.blurb}</span>}
        {!searching && (
          <div className="world-tabs">
            {mapWorlds.map((w) => (
              <button key={w.id} className={w.id === world ? "wt on" : "wt"} onClick={() => setWorld(w.id)} title={w.name}>
                {w.name.split(" ")[0]}
                {w.solved >= w.count && w.count > 0 ? " ⚑" : ""}
              </button>
            ))}
          </div>
        )}
      </div>

      <ul className="levels">
        {shown.map((p, i) => (
          <li key={p.slug}>
            <Link href={`/problems/${p.slug}`} className={`level-tile diff-edge-${p.difficulty.toLowerCase()} ${progress.solved[p.slug] ? "solved" : ""}`}>
              <span className="level-no">{searching ? `#${p.id}` : `${i + 1}`}</span>
              <span className="level-title">{p.title}</span>
              <span className="level-story">“{p.storyTitle}”</span>
              <span className="level-meta">
                <span className={`diff diff-${p.difficulty.toLowerCase()}`}>{p.difficulty}</span>
                {progress.solved[p.slug] ? <span className="check">★ CLEAR</span> : <span className="lc">#{p.id}</span>}
              </span>
            </Link>
          </li>
        ))}
        {!shown.length && <li className="empty">Nothing here yet.</li>}
      </ul>
    </section>
  );
}
