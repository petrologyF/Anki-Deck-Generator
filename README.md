# Anki Deck Generator

> **JSONデータから洗練されたデザインのAnkiカードを瞬時に生成**
> 
> 学生や研究者のための、高生産性デスクトップツールです。データの管理はシンプルに、学習は美しく。

---

## 特徴

### モダンで高品質な意匠
VS Code をリスペクトしたプロフェッショナルなインターフェースを採用。開発者や高生産性を求めるユーザーに馴染み深い、ダークモード標準の美しいUIを提供します。

### スマートな制作ワークフロー
独自の「ガイダンス・システム」を搭載。
- **保存が必要な時**: 保存アイコンが青く発光
- **生成準備が整った時**: 実行アイコンが青く発光
次にすべき操作を視覚的に誘導し、操作ミスを最小限に抑えます。

### 洗練されたカードデザイン
Ankiの標準モデルを大幅に拡張。品詞や例文が際立つCSSが内蔵されており、単語を「ただ覚える」だけでなく「文脈の中で理解する」ためのデザインを実現しています。

### 複数ジャンルの独立管理
「英単語用」と「一般暗記用」のデータをタブで切り替えて編集可能。それぞれ独立した `.apkg` ファイルとして生成されます。設定画面（設定アイコン）から、インポート先のAnkiデッキ名を自由にカスタマイズすることも可能です。

### 自動配信システム (Discord連携)
生成されたデッキ（.apkg）を Discord Webhook 経由で自動送信。PCで作って、スマホの通知から即座に AnkiMobile/AnkiDroid で受け取ることができます。

---

## クイックスタート

### 1. 準備
[Python 3.8以上](https://www.python.org/downloads/) がインストールされていることを確認してください。

### 2. インストール
リポジトリをダウンロードして解凍し、そのディレクトリで以下を実行します：

```bash
pip install -r requirements.txt
```

### 3. 設定
1.  **環境変数の設定**: `.env.example` をコピーして `.env` という名前のファイルを作成し、Discord Webhook URL を記入します。
    ```bash
    copy .env.example .env
    ```
2.  **データの準備**: 初めて使用する場合は、`data/words.json.example` をコピーして `data/words.json` を作成してください。
    ```bash
    copy data/words.json.example data/words.json
    ```

### 4. アプリの起動
```bash
python run.py
```

---

## 使い方

1.  **データ作成**: 中央のエディタで `words.json` または `others.json` のタブを選択し、単語・項目データを編集します。
2.  **保存 (`Ctrl+S`)**: 左端の **保存（ディスク）アイコン** をクリックして変更を確定させます。
3.  **デッキ生成**: **生成（再生）アイコン** をクリックすると、それぞれのデータに対応した独立した `.apkg` ファイルが `output` フォルダに作成されます。
4.  **同期**: DiscordのWebhook URLを設定しておけば、生成と同時に自動で送信されます。
5.  **設定の変更**: 左下の **歯車アイコン** から、Discord連携先やAnkiのインポート先デッキ名（Default, Others など）を自由に変更できます。

---

## AIを使ったデータ生成プロンプト

LLM（Gemini, ChatGPT, Claude など）を使って、Anki用のJSONデータを簡単に作成できます。以下のプロンプトをコピーしてAIに渡し、出力されたJSONをアプリの各タブに貼り付けてください。

### 英単語用 (`words.json`) プロンプト

```text
以下の英単語リストを学習するためのJSONデータを作成してください。
キーには英単語、値には詳細情報（reading, pos, meaning, synonyms, example, tags）を含むオブジェクトを指定してください。

【出力形式の例】
{
  "vulnerable": {
    "reading": "vʌ́lnərəbl",
    "pos": "形容詞",
    "meaning": "傷つきやすい、脆弱な",
    "synonyms": "susceptible, weak",
    "example": "The system is <i>vulnerable</i> to cyber attacks.",
    "tags": ["IT", "TOEIC"]
  }
}

【作成してほしい単語】
・mitigate
・ubiquitous
・resilient
```

### 一般暗記項目用 (`others.json`) プロンプト

```text
以下の学習テーマについて、暗記用の一問一答形式のJSONデータを作成してください。
キーには「問題文（表）」、値には「解答（裏）」の文字列を指定してください。タグなどの付加情報が必要な場合は値にオブジェクトを指定できます。

【出力形式の例】
{
  "日本で一番高い山は？": "富士山",
  "相対性理論を提唱した人物は？": {
    "back": "アルベルト・アインシュタイン",
    "tags": ["物理", "歴史"]
  }
}

【作成してほしいテーマ】
・IT基本用語（ネットワーク関連）について5問
```

---

## 技術仕様

| コンポーネント | 技術 |
| :--- | :--- |
| **UI Framework** | [Flet](https://flet.dev/) (Flutter based Python framework) |
| **Deck Logic** | [Genanki](https://github.com/kerrickstaley/genanki) |
| **Styling** | VS Code Inspired Design System |
| **Typography** | Outfit (Google Fonts) |

---

## コントリビュート
不具合の報告や新機能の提案は、GitHubのIssueまたはPull Requestにてお待ちしております。

---

> [!TIP]
> **ヒント: アイコンの変更について**
> 独自のアイコン（`icon.ico`）を使用する場合は、`assets` フォルダ内のファイルを差し替えた後、`flet pack` を使用してビルドすることで反映されます。
