/* eslint-disable @typescript-eslint/no-explicit-any */
export type V = any;

export type Difficulty = "Easy" | "Medium" | "Hard";

export interface Spec {
  method: string;
  ret: string;
  params: [string, string][];
  output?: string;
}

export interface TestCase {
  args: V[];
  expected?: V;
  name?: string;
}

export interface LayerDef {
  kind: string;
  var?: string;
  label?: string;
  style?: string;
  palette?: string;
  pointers?: (string | [string, string])[];
  window?: [string, string];
  vars?: string[];
  from?: "outer" | "top";
  children?: LayerDef[];
  [key: string]: V;
}

export interface SceneDef {
  theme: string;
  layers: LayerDef[];
}

export interface Problem {
  id: number;
  slug: string;
  title: string;
  difficulty: Difficulty;
  world: string;
  tags: string[];
  story: { title: string; text: string; goal: string };
  legend?: { sprite: string; meaning: string }[];
  spec: Spec;
  compare?: string;
  tests: TestCase[];
  visualTest?: number;
  scene: SceneDef;
  reference: string;
  hints?: string[];
  tier?: "crafted" | "auto";
}

export interface ProblemSummary {
  id: number;
  slug: string;
  title: string;
  difficulty: Difficulty;
  world: string;
  tags: string[];
  storyTitle: string;
  theme: string;
  tier: "crafted" | "auto";
}

export interface TraceFrame {
  fn: string;
  line: number;
  vars: Record<string, V>;
}

export interface TraceNode {
  val: V;
  next?: string | null;
  left?: string | null;
  right?: string | null;
  bad?: boolean;
}

export interface TraceStep {
  line: number;
  fn: string;
  stack: TraceFrame[];
  nodes: Record<string, TraceNode>;
  error?: string;
}

export interface Trace {
  steps: TraceStep[];
  end: { kind: string; code?: number | null; signal?: string; message?: string };
  truncated: boolean;
  ms?: number;
  test?: number;
}

export interface TestResult {
  i: number;
  output: V;
  expected: V;
  passed: boolean;
  error: string | null;
  stdout: string;
  stderr: string;
  ms: number;
}

export interface RunResponse {
  fatal?: string;
  compile?: { ok: boolean; errors: { line: number; col: number; message: string }[]; raw: string; ms: number };
  results?: TestResult[];
  trace?: Trace | null;
}
