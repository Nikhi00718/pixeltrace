import Link from "next/link";
import HeroDemo from "@/components/HeroDemo";
import ProblemBrowser from "@/components/ProblemBrowser";
import { WORLDS, summaries } from "@/lib/problems";

export default function Home() {
  const list = summaries();
  const worlds = WORLDS.map((w) => ({ ...w, count: list.filter((p) => p.world === w.id).length })).filter((w) => w.count > 0);
  const first = list.find((p) => p.slug === "two-sum") ?? list[0];
  return (
    <div className="home">
      <section className="hero">
        <div>
          <div className="eyebrow">▶ C++ · REAL G++ · LINE-BY-LINE</div>
          <h1>
            Watch your C++ <em>come alive</em>.
          </h1>
          <p>
            Write a solution and every line plays out as a pixel scene: arrays are crates on a dock, stacks are towers,
            linked lists are trains, trees grow fruit. Pause, scrub, and hover anything to see its value.
          </p>
          <div className="hero-cta">
            {first && (
              <Link href={`/problems/${first.slug}`} className="btn accent">
                ▶ Start with {first.title}
              </Link>
            )}
            <a href="#worlds" className="btn ghost">
              Browse worlds
            </a>
          </div>
          <div className="hero-stats">
            <div>
              <b>{list.length}</b>
              <span>problems</span>
            </div>
            <div>
              <b>{worlds.length}</b>
              <span>worlds</span>
            </div>
            <div>
              <b>gdb</b>
              <span>traces every line</span>
            </div>
          </div>
        </div>
        <HeroDemo />
      </section>
      <ProblemBrowser problems={list} worlds={worlds} />
    </div>
  );
}
