#!/usr/bin/env python3
"""上位候補をビープ音区切りで1本の聞き比べファイルに連結する。
あわせて再生順とファイル名の対応表（<out>-map.txt）を出す。

使い方:
  make_audition.py top1.wav top2.wav ... --out audition.wav
"""
import argparse, os
import numpy as np
import soundfile as sf

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sr_out = None
    parts, lines = [], []
    for idx, f in enumerate(a.files, 1):
        x, sr = sf.read(f)
        if x.ndim > 1:
            x = x[:, 0]
        if sr_out is None:
            sr_out = sr
        beep_t = np.arange(int(sr * 0.3)) / sr
        beep = 0.25 * np.sin(2 * np.pi * 880 * beep_t)
        gap = np.zeros(int(sr * 0.5))
        lead = np.zeros(int(sr * 0.3))
        parts += [lead, beep, gap, x.astype(np.float64), gap]
        lines.append(f"{idx}: {os.path.basename(f)}")
    joined = np.concatenate(parts)
    sf.write(a.out, joined, sr_out)
    with open(a.out + "-map.txt", "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")
    print(f"wrote {a.out} ({len(joined)/sr_out:.1f}s) and {a.out}-map.txt")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
