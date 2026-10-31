#!/usr/bin/env python3
"""ボイスレシピカード（PNG）と recipe.yaml を発行する。

使い方:
  make_recipe_card.py --name マルチ --seed 987123 --caption "……" \
    --memo "高め、澄んだ明るい音色" --out-dir ./recipe [--verified]
"""
import argparse, os, textwrap
from datetime import date
from PIL import Image, ImageDraw, ImageFont

REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
ENGINE_LINE = "Irodori-TTS v4.1-Small-MF / ONNX int8 / 切り捨て係数 0.85"
REF_LINE = "参照潜在: 採用クリップ1本を平均8回エンコード（-16 LUFS正規化）"

def F(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)

def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for ch in text:
        t = cur + ch
        if draw.textlength(t, font=font) <= maxw or ch in "、。，）」！？・":
            cur = t
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--seed", required=True)
    ap.add_argument("--caption", required=True)
    ap.add_argument("--memo", default="")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--verified", action="store_true", help="感情3点テスト実施済み")
    a = ap.parse_args()
    today = date.today().isoformat()
    os.makedirs(a.out_dir, exist_ok=True)

    yaml_text = (
        f"name: {a.name}\n"
        f"issued: {today}\n"
        f"engine: {ENGINE_LINE}\n"
        f"caption: {a.caption}\n"
        f"seed: {a.seed}\n"
        f"reference: {REF_LINE}\n"
        f"feature_memo: {a.memo}\n"
        f"emotion_test: {'done' if a.verified else 'not yet'}\n"
    )
    with open(os.path.join(a.out_dir, "recipe.yaml"), "w", encoding="utf-8") as fp:
        fp.write(yaml_text)

    W, H = 1240, 1600
    img = Image.new("RGB", (W, H), (18, 52, 74))
    d = ImageDraw.Draw(img)
    y = 78
    d.text((80, y), "ボイスレシピカード", font=F(40, True), fill=(255, 205, 150)); y += 78
    d.text((80, y), f"エージェント: {a.name}", font=F(54, True), fill=(255, 255, 255)); y += 92
    d.text((80, y), f"発行日: {today}", font=F(32), fill=(205, 225, 235)); y += 64
    d.text((80, y), "キャプション（声の設計）", font=F(34, True), fill=(255, 205, 150)); y += 52
    for ln in wrap(d, a.caption, F(34), W - 160):
        d.text((80, y), ln, font=F(34), fill=(255, 255, 255)); y += 50
    y += 18
    d.text((80, y), f"採用シード: {a.seed}", font=F(34), fill=(255, 255, 255)); y += 52
    d.text((80, y), f"エンジン: {ENGINE_LINE}", font=F(30), fill=(205, 225, 235)); y += 48
    d.text((80, y), REF_LINE, font=F(30), fill=(205, 225, 235)); y += 62
    if a.memo:
        d.text((80, y), "特徴メモ", font=F(34, True), fill=(255, 205, 150)); y += 52
        for ln in wrap(d, a.memo, F(34), W - 160):
            d.text((80, y), ln, font=F(34), fill=(255, 255, 255)); y += 50
        y += 18
    d.text((80, y), f"感情3点テスト: {'実施済み（喜・哀・ふだん）' if a.verified else '未実施'}",
           font=F(32), fill=(255, 255, 255))
    y += 90
    img = img.crop((0, 0, W, y))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([36, 36, W - 36, y - 36], radius=30, outline=(255, 190, 110), width=4)
    out_png = os.path.join(a.out_dir, "recipe-card.png")
    img.save(out_png)
    print(f"wrote {out_png} and recipe.yaml")

if __name__ == "__main__":
    main()
