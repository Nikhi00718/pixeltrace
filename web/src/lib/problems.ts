import "server-only";
import fs from "node:fs";
import path from "node:path";
import type { Problem, ProblemSummary } from "./types";

const DIR = path.join(process.cwd(), "data", "problems");

let cache: Problem[] | null = null;

export function allProblems(): Problem[] {
  if (cache && process.env.NODE_ENV === "production") return cache;
  const files = fs.existsSync(DIR) ? fs.readdirSync(DIR).filter((f) => f.endsWith(".json")) : [];
  const list = files.map((f) => JSON.parse(fs.readFileSync(path.join(DIR, f), "utf8")) as Problem);
  list.sort((a, b) => a.id - b.id);
  cache = list;
  return list;
}

export function getProblem(slug: string): Problem | undefined {
  return allProblems().find((p) => p.slug === slug);
}

export function summaries(): ProblemSummary[] {
  return allProblems().map((p) => ({
    id: p.id,
    slug: p.slug,
    title: p.title,
    difficulty: p.difficulty,
    world: p.world,
    tags: p.tags,
    storyTitle: p.story.title,
    theme: p.scene.theme,
    tier: p.tier ?? "crafted",
  }));
}

export const WORLDS: { id: string; name: string; blurb: string; theme: string }[] = [
  { id: "arrays", name: "Harbor Docks", blurb: "Arrays, hashing and prefix tricks", theme: "dock" },
  { id: "two-pointers", name: "Twin Piers", blurb: "Two pointers walking toward each other", theme: "dock" },
  { id: "sliding-window", name: "Lighthouse Beam", blurb: "Sliding windows over sequences", theme: "city" },
  { id: "stack", name: "Tower Yard", blurb: "Stacks and monotonic stacks", theme: "castle" },
  { id: "binary-search", name: "Guarded Corridor", blurb: "Halve the search space each step", theme: "cave" },
  { id: "linked-list", name: "Rail Yard", blurb: "Linked lists as trains", theme: "farm" },
  { id: "trees", name: "Orchard Forest", blurb: "Binary trees and recursion", theme: "forest" },
  { id: "heap", name: "Pyramid Market", blurb: "Heaps and priority queues", theme: "market" },
  { id: "graphs", name: "Kingdom Roads", blurb: "Grids, BFS, DFS and topological order", theme: "forest" },
  { id: "backtracking", name: "Door Maze", blurb: "Recursion that tries and undoes", theme: "cave" },
  { id: "dp", name: "Farmlands", blurb: "Dynamic programming tables", theme: "farm" },
  { id: "intervals", name: "Calendar Hall", blurb: "Merging and scheduling intervals", theme: "lab" },
  { id: "greedy", name: "Vending Street", blurb: "Greedy choices", theme: "market" },
  { id: "bits", name: "Lamp Room", blurb: "Bit manipulation", theme: "space" },
];

export function starterCode(p: Problem): string {
  const params = p.spec.params.map(([t, n]) => `${t} ${n}`).join(", ");
  return `class Solution {\npublic:\n    ${p.spec.ret} ${p.spec.method}(${params}) {\n        \n    }\n};\n`;
}
