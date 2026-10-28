import ProblemBrowser from "@/components/ProblemBrowser";
import { WORLDS, summaries } from "@/lib/problems";

export default function Home() {
  const list = summaries();
  const worlds = WORLDS.map((w) => ({ ...w, count: list.filter((p) => p.world === w.id).length })).filter((w) => w.count > 0);
  return (
    <div className="home">
      <section className="hero">
        <h1>Watch your C++ come alive.</h1>
        <p>
          {list.length} problems across {worlds.length} pixel worlds. Write a C++ solution and every line plays out
          as a scene: arrays become crates on a dock, stacks become towers, linked lists become trains, trees grow fruit.
          Pick an island to start.
        </p>
      </section>
      <ProblemBrowser problems={list} worlds={worlds} />
    </div>
  );
}
