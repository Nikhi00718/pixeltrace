import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Workspace from "@/components/Workspace";
import { allProblems, getProblem, starterCode } from "@/lib/problems";

export function generateStaticParams() {
  return allProblems().map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: PageProps<"/problems/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  const p = getProblem(slug);
  return { title: p ? `${p.id}. ${p.title} — PixelTrace` : "PixelTrace" };
}

export default async function ProblemPage({ params }: PageProps<"/problems/[slug]">) {
  const { slug } = await params;
  const problem = getProblem(slug);
  if (!problem) notFound();
  return <Workspace problem={problem} starter={starterCode(problem)} />;
}
