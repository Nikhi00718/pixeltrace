export const metadata = { title: "How it works — PixelTrace" };

export default function About() {
  return (
    <div className="about panel">
      <h1>How PixelTrace works</h1>
      <ol>
        <li>
          <b>You write C++.</b> Only the <code>class Solution</code>, exactly like LeetCode. <code>ListNode</code>,{" "}
          <code>TreeNode</code> and <code>bits/stdc++.h</code> are already there.
        </li>
        <li>
          <b>Real g++ compiles it</b> with <code>-O0 -g -D_GLIBCXX_ASSERTIONS</code>, so out-of-range{" "}
          <code>vector</code> access is caught instead of reading garbage.
        </li>
        <li>
          <b>gdb walks every line</b> of your solution and records the locals, the call stack and every reachable{" "}
          <code>ListNode</code>/<code>TreeNode</code>. STL containers are read through libstdc++&apos;s pretty-printers.
        </li>
        <li>
          <b>The scene engine maps variables to sprites.</b> Each problem has a situation file saying which variable is
          the dock of crates, which ints are the characters walking on it, which map is the locker wall, and so on.
          Anything unmapped still shows up through the automatic layout.
        </li>
        <li>
          <b>Frames are diffed and tweened.</b> When a value moves, its sprite glides; when it changes, it flashes; when
          a pointer goes past the end of the dock, the character falls into the sea.
        </li>
      </ol>
      <h2>Scene kinds</h2>
      <table className="kinds">
        <tbody>
          <tr><td>array</td><td>crates on a dock, letter tiles, or brick towers (bars)</td></tr>
          <tr><td>grid</td><td>tile map: islands, oranges, maze, DP table, board</td></tr>
          <tr><td>map / set</td><td>a wall of lockers</td></tr>
          <tr><td>stack</td><td>a tower of blocks</td></tr>
          <tr><td>queue</td><td>people waiting at a gate</td></tr>
          <tr><td>heap</td><td>a fruit pyramid in heap order</td></tr>
          <tr><td>list</td><td>a train; pointer variables ride on cars</td></tr>
          <tr><td>tree</td><td>an orchard tree; nodes are fruit</td></tr>
          <tr><td>graph</td><td>towns and roads, coloured by visit state</td></tr>
          <tr><td>intervals</td><td>a calendar of bookings</td></tr>
          <tr><td>calls</td><td>a row of doors, one per recursive call</td></tr>
        </tbody>
      </table>
      <p className="small">
        Problem titles and numbers refer to LeetCode for practice. Stories, tests and reference solutions on this site
        are written for PixelTrace.
      </p>
    </div>
  );
}
