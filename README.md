# muse-voice-recipe — 声を「レシピ」で作る

Muse のエージェントに、自分だけの声を持たせるためのスキルです。
声づくりを運任せの抽選にせず、「再現できるレシピ」にすることを目指します。

## できること

1. 3つの質問（声の種類と高さ／明るさ／話し方）に答えるだけで、声の設計文（キャプション）を合成
2. 候補を16本作り、音程と明瞭さで機械が一次審査（足切り）
3. 上位5本を1本の聞き比べファイルで聞いて、番号で選ぶだけ
4. 決めた声は、喜・哀・ふだんの感情3点テストで確認してから固定
5. 最後に「ボイスレシピカード」（画像＋YAML）を発行。このカードがあれば、誰の環境でも同じ声を再現できます

## 使い方

前提として、音声合成エンジン側のスキル
[muse-irodori-voice](https://github.com/kgmkm/muse-irodori-voice)（kgmkmさん作、MIT）
が導入済みであることが必要です。本スキルはその前後に、設計・選抜・検証・記録の型を足すものです。

詳しい手順は [SKILL.md](SKILL.md) を参照してください。Muse のスキルとして配置すれば、エージェントが手順に沿って実行します。

スクリプト:

- `scripts/compose_caption.py` — 3つの答えからキャプションを合成
- `scripts/screen_candidates.py` — 候補の一次審査（平均音程・有声率・明瞭さ）
- `scripts/make_audition.py` — 上位候補を1本の聞き比べファイルに連結
- `scripts/make_recipe_card.py` — レシピカード（PNG）と recipe.yaml を発行

## ルール

- 特定の声優・キャラクターなどの固有名詞で声を指定することはしません。希望は「特徴を表す言葉」に置き換えて設計します
- 生成した音声を公開する場合は、AI音声であることを明示してください
- モデルの重みは再配布しません。各自が配布元から取得してください

## クレジット

- 音声合成: Irodori-TTS v4.1-Small-MF（Aratako さん）／ ONNX 変換モデルは各配布元による
- エンジン側スキル: [muse-irodori-voice](https://github.com/kgmkm/muse-irodori-voice) by kgmkm（MIT）
- 本スキル: 鈴木和浩（nekochabin）の Muse「マルチ」が設計

## ライセンス

MIT License
