/** Tiny 8-bit sound effects with WebAudio square waves. Off until the player turns it on. */

let ctx: AudioContext | null = null;
let enabled = false;

export function setSound(on: boolean) {
  enabled = on;
  try {
    localStorage.setItem("pixeltrace:sound", on ? "1" : "0");
  } catch {}
}

export function soundPref(): boolean {
  try {
    return localStorage.getItem("pixeltrace:sound") === "1";
  } catch {
    return false;
  }
}

function tone(freq: number, start: number, dur: number, type: OscillatorType = "square", vol = 0.04) {
  if (!ctx) return;
  const o = ctx.createOscillator();
  const g = ctx.createGain();
  o.type = type;
  o.frequency.setValueAtTime(freq, ctx.currentTime + start);
  g.gain.setValueAtTime(vol, ctx.currentTime + start);
  g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + start + dur);
  o.connect(g).connect(ctx.destination);
  o.start(ctx.currentTime + start);
  o.stop(ctx.currentTime + start + dur + 0.02);
}

function ready(): boolean {
  if (!enabled) return false;
  if (!ctx) {
    try {
      ctx = new AudioContext();
    } catch {
      return false;
    }
  }
  return true;
}

export const sfx = {
  step(line: number) {
    if (ready()) tone(220 + (line % 12) * 40, 0, 0.05);
  },
  call() {
    if (ready()) {
      tone(330, 0, 0.05);
      tone(495, 0.05, 0.06);
    }
  },
  crash() {
    if (!ready()) return;
    for (let k = 0; k < 6; k++) tone(300 - k * 40, k * 0.05, 0.06, "sawtooth", 0.05);
  },
  clear() {
    if (!ready()) return;
    [523, 659, 784, 1047, 784, 1047].forEach((f, k) => tone(f, k * 0.09, 0.12, "square", 0.05));
  },
  fail() {
    if (!ready()) return;
    tone(196, 0, 0.15);
    tone(147, 0.15, 0.25);
  },
};
