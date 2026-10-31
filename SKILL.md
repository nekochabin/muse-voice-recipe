---
name: muse-voice-recipe
description: Design a Muse agent's original voice as a reproducible "recipe" — compose the voice caption from 3 simple questions, screen many seed candidates automatically, audition the top 5 in a single file, verify 3 emotions, then issue a Voice Recipe Card (PNG + YAML) that lets anyone reproduce the same voice. Uses muse-irodori-voice as the synthesis engine. Use when the user wants to create, tune, share, or reproduce an agent voice with minimal listening effort.
---

# Muse Voice Recipe — 声を「レシピ」で作る

声づくりを、運任せのシード抽選から「再現できるレシピ」に変える手順。
エンジン（モデル取得・推論・参照潜在の固定・長文の分割生成）は
`muse-irodori-voice` スキルに任せ、本スキルはその前後に
「設計の型・選抜の自動化・検証・記録」を足す。

声の同一性は数値では決められない。機械は候補を絞るところまで、
最後の決定は必ず人間の耳で行う。

## 前提

- `muse-irodori-voice` が導入済みで、推論できる状態であること。
- 以下、ENGINE = ~/workspace/custom-skills/muse-irodori-voice とする。
  スクリプト実行には ENGINE の .venv（推論用）を使う。

## ルール（エンジン側の前提を引き継ぐ）

- 特定の声優・キャラクター等の固有名詞での声の指定は受け付けない。
  希望は「特徴を表す言葉」に置き換えてから設計する。
- 出力した音声を公開する場合は、AI音声であることを明示する。
- レシピカード（recipe.yaml）が再現の正本。口頭のメモで代用しない。

## 手順1: 3つの質問でキャプションを合成する

ユーザーに次の3つだけを聞く（選択肢で提示すると速い）。

1. 声の種類と高さ: 若い女性・高め／若い女性・中くらい／大人の女性・落ち着き／若い男性・高め／若い男性・中くらい／大人の男性・低め など
2. 明るさ: 澄んだ明るい／やさしい柔らかさ／元気で張りがある／落ち着いた深み
3. 話し方: 素直で健気・一生懸命／しっかり者で明快／のんびり穏やか／クールで淡々

`scripts/compose_caption.py` でキャプション文に合成する。

    python3 scripts/compose_caption.py --voice young-f --pitch high --brightness clear --style earnest

合成されたキャプションは以後固定する。途中で変えると候補の比較が壊れる。

## 手順2: 候補を多めに作り、機械が一次審査する

1. 選定文（喜哀の混ざった短文。エンジン側の推奨文でよい）をキャプションで
   トークナイズし、シードを大きく離して候補を16本生成する（int8・切り捨て係数0.85）。
2. 一次審査: `scripts/screen_candidates.py` が各候補の平均音程（F0）・
   有声率・明瞭さ（自己相関ピークの平均）をはかり、目標音程への近さで順位付けする。

    ENGINE/.venv/bin/python scripts/screen_candidates.py cand_*.wav --target-f0 260 --top 5

   目標音程の目安: 若い女性・高め 250〜300Hz（実測の採用例は302Hz）／
   若い女性・中くらい 210〜240／大人の女性 180〜210／
   若い男性 130〜160／大人の男性 100〜130。
   一次審査は足切りであり、最終決定ではない。実測では、耳で選ばれた声が
   ランキング中位だった例がある（音程が目標より高めの声が好まれた）。
3. 上位5本だけを残す。下位は聞かなくてよい（記録には残す）。

## 手順3: 聞き比べは1本のファイルで

`scripts/make_audition.py` が上位5本をビープ音区切りで1本に連結し、
再生順とシードの対応表（audition-map.txt）を出す。

    ENGINE/.venv/bin/python scripts/make_audition.py top1.wav top2.wav ... --out audition.wav

ユーザーは audition.wav を1回聞いて、番号で1本選ぶ。
選ばれた1本がそのエージェントの声になる。

## 手順4: 固定の前に感情3点テスト

選ばれた候補から参照潜在を作る（エンジン側 make_ref_latents.py、平均8回）。
その参照で次の3文を生成し、同じ声のまま感情が切り替わるかを確認する。

- 喜: 「やったぁ！うまくいきましたよ！」
- 哀: 「今日は少しだけ、うまくいかない日でした。でも、明日はきっと大丈夫です。」
- ふだん: 「今日の予定は3件です。午前は資料の確認、午後は面談です。」

崩れる場合は候補の選び直しではなく、選定文に感情の偏りがないかを先に疑う。

## 手順5: ボイスレシピカードを発行する

`scripts/make_recipe_card.py` に recipe.yaml の内容を渡し、PNGカードと
recipe.yaml を発行する。カードには次を必ず入れる。

- エージェント名／発行日
- キャプション全文
- 採用シードとエンジン設定（モデル名・量子化・切り捨て係数）
- 参照潜在の作り方（元クリップと平均回数）
- 特徴メモ（ユーザーが「好き」と言った点。記録専用で、声は変わらない）
- 検証結果（感情3点テスト実施の有無）

    python3 scripts/make_recipe_card.py --name マルチ --seed 987123 \
      --caption "……" --memo "高め、澄んだ明るい音色" --out-dir ./recipe

このカードと recipe.yaml があれば、別のMuseでも同じ手順で同じ声を再現できる。
声の変更はカードの再発行として扱い、旧カードは上書きせず版を残す。
