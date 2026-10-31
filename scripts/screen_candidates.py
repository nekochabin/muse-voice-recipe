#!/usr/bin/env python3
"""候補 wav の一次審査: 平均音程(F0)・有声率・明瞭さをはかり、
目標音程への近さで順位付けして上位を JSON で出す。

使い方:
  screen_candidates.py cand_*.wav --target-f0 260 --top 5 [--out ranking.json]

声の同一性を決めるものではない。「明らかに外れた候補を聞かずに済ませる」
ための足切りとして使う。
"""
import argparse, json, math, os, sys
import numpy as np
import soundfile as sf

def analyze(path):
    x, sr = sf.read(path)
    if x.ndim > 1:
        x = x[:, 0]
    x = x.astype(np.float64)
    win, hop = 2048, 1024
    f0s, clarity = [], []
    for i in range(0, len(x) - win, hop):
        seg = x[i:i + win]
        rms = np.sqrt(np.mean(seg ** 2))
        if rms < 0.03:
            continue
        seg = seg - seg.mean()
        ac = np.correlate(seg, seg, mode="full")[win - 1:]
        if ac[0] <= 0:
            continue
        lo, hi = int(sr / 400), int(sr / 60)  # 60〜400Hz
        if hi >= len(ac):
            continue
        peak = lo + int(np.argmax(ac[lo:hi]))
        clarity.append(float(ac[peak] / ac[0]))
        f0s.append(sr / peak)
    if not f0s:
        return {"file": path, "f0": None, "voiced": 0.0, "clarity": 0.0}
    total_frames = max(1, (len(x) - win) // hop)
    return {
        "file": path,
        "f0": float(np.median(f0s)),
        "voiced": len(f0s) / total_frames,
        "clarity": float(np.mean(clarity)),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--target-f0", type=float, required=True)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rows = [analyze(f) for f in a.files]
    for r in rows:
        if r["f0"]:
            dist = abs(math.log2(r["f0"] / a.target_f0))
            r["score"] = dist - 0.15 * r["clarity"]  # 音程の近さ優先、明瞭さは補助
        else:
            r["score"] = 99.0
    rows.sort(key=lambda r: r["score"])
    result = {"target_f0": a.target_f0, "ranking": rows, "top": rows[:a.top]}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fp:
            fp.write(text)
    print(text)

if __name__ == "__main__":
    main()
