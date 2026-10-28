/** Per-browser progress: which levels were cleared and which was opened last. */

const KEY = "pixeltrace:progress";

export interface Progress {
  solved: Record<string, number>; // slug -> timestamp
  last?: string;
}

export function loadProgress(): Progress {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return { solved: {}, ...JSON.parse(raw) };
  } catch {}
  return { solved: {} };
}

function save(p: Progress) {
  try {
    localStorage.setItem(KEY, JSON.stringify(p));
  } catch {}
}

export function markSolved(slug: string) {
  const p = loadProgress();
  if (!p.solved[slug]) p.solved[slug] = Date.now();
  save(p);
}

export function markOpened(slug: string) {
  const p = loadProgress();
  p.last = slug;
  save(p);
}
