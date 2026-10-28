import { NextResponse } from "next/server";
import { getProblem } from "@/lib/problems";

const RUNNER_URL = process.env.RUNNER_URL ?? "http://127.0.0.1:8765";
const RUNNER_TOKEN = process.env.RUNNER_TOKEN ?? "";

export async function POST(req: Request) {
  let body: { slug?: string; code?: string; trace?: number; custom?: unknown[] | null };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ fatal: "Bad request body" }, { status: 400 });
  }
  const problem = body.slug ? getProblem(body.slug) : undefined;
  if (!problem) return NextResponse.json({ fatal: "Unknown problem" }, { status: 404 });
  if (typeof body.code !== "string" || body.code.length > 40000) {
    return NextResponse.json({ fatal: "Code missing or too long" }, { status: 400 });
  }

  const tests: { args: unknown[]; expected?: unknown; has_expected: boolean }[] = problem.tests.map((t) => ({
    args: t.args,
    expected: t.expected,
    has_expected: true,
  }));
  if (Array.isArray(body.custom)) {
    if (body.custom.length !== problem.spec.params.length) {
      return NextResponse.json({ fatal: `Custom input needs ${problem.spec.params.length} argument(s)` }, { status: 400 });
    }
    tests.push({ args: body.custom, has_expected: false });
  }
  const trace = typeof body.trace === "number" ? body.trace : problem.visualTest ?? 0;

  try {
    const res = await fetch(`${RUNNER_URL}/run`, {
      method: "POST",
      headers: { "content-type": "application/json", ...(RUNNER_TOKEN ? { authorization: `Bearer ${RUNNER_TOKEN}` } : {}) },
      body: JSON.stringify({
        code: body.code,
        spec: { ...problem.spec, output: problem.spec.output ?? "return" },
        tests,
        compare: problem.compare ?? "exact",
        trace,
        reference: problem.reference,
      }),
      signal: AbortSignal.timeout(90_000),
    });
    if (!res.ok) return NextResponse.json({ fatal: `Runner error ${res.status}: ${(await res.text()).slice(0, 300)}` }, { status: 502 });
    return NextResponse.json(await res.json());
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return NextResponse.json(
      { fatal: `Cannot reach the C++ runner at ${RUNNER_URL} (${msg}). Start it with: docker compose up --build` },
      { status: 503 },
    );
  }
}
