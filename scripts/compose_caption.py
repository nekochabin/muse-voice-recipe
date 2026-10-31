#!/usr/bin/env python3
"""3つの質問の答えから Irodori 用キャプションを合成する。

使い方:
  python3 compose_caption.py --voice young-f --pitch high --brightness clear --style earnest

出力: キャプション文（標準出力）
"""
import argparse

VOICE = {
    "young-f": "若い女性の声",
    "adult-f": "大人の女性の声",
    "young-m": "若い男性の声",
    "adult-m": "大人の男性の声",
    "neutral": "中性的な声",
}
PITCH = {
    "high": "高さは高めで",
    "mid": "高さは中くらいで",
    "low": "高さは低めで",
}
BRIGHTNESS = {
    "clear": "澄んだ明るい音色",
    "soft": "やさしく柔らかい音色",
    "lively": "元気で張りのある音色",
    "calm": "落ち着いた深みのある音色",
}
STYLE = {
    "earnest": "素直で健気、少し天然な可愛さで、一生懸命に話す",
    "reliable": "しっかり者で、明快に話す",
    "gentle": "のんびりと穏やかに話す",
    "cool": "クールに淡々と話す",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True, choices=list(VOICE))
    ap.add_argument("--pitch", required=True, choices=list(PITCH))
    ap.add_argument("--brightness", required=True, choices=list(BRIGHTNESS))
    ap.add_argument("--style", required=True, choices=list(STYLE))
    a = ap.parse_args()
    caption = (
        f"{VOICE[a.voice]}。{PITCH[a.pitch]}、{BRIGHTNESS[a.brightness]}。"
        "抑揚が豊かで、息づかいが感じられる近い距離感。"
        f"{STYLE[a.style]}。"
    )
    print(caption)

if __name__ == "__main__":
    main()
