# Anki Deck Generator [VS Code Edition]

[日本語の解説は下にあります (Japanese description below)]

An automated tool to transform your vocabulary lists in JSON format into high-quality Anki flashcard decks (`.apkg`), featuring a professional VS Code-inspired desktop interface.

---

## 🚀 Overview (EN)

This application is designed for students and researchers who want to spend more time studying and less time creating flashcards. By editing a simple JSON file, you can generate beautifully styled Anki decks with a single click.

### ✨ Key Features
- **Pro Interface**: Sleek, high-productivity UI inspired by VS Code.
- **Smart Highlighting**: Sidebar icons glow blue to guide you through the "Edit → Save → Generate" workflow.
- **Auto-Styling**: Professional card CSS including automated Light/Dark mode support.
- **Discord Integration**: Automatically send your generated decks to a Discord channel via Webhook.

### 🛠️ Setup (For Non-Enginnering Students)
1. **Install Python**: Ensure you have [Python 3.8+](https://www.python.org/downloads/) installed on your PC.
2. **Download Code**: Download this repository and unzip it.
3. **Install Dependencies**: Open your terminal (PowerShell or Command Prompt) in this folder and run:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run**: 
   ```bash
   python run.py
   ```

### 📖 How to Use
1. **Edit**: Type your word data directly into the center screen.
2. **Save**: Click the **Save (Disk)** icon on the left sidebar (it will glow blue when changes are detected).
3. **Generate**: Click the **Generate (Play)** icon (it will glow blue once the file is saved).
4. **Retrieve**: Your deck will appear in the `output` folder and instantly be sent to your Discord (if configured).

---

## 🚀 概要 (JP)

このアプリは、JSON形式の単語リストから高品質なAnkiデッキ（.apkg）を自動生成するためのデスクトップツールです。VS Codeをリスペクトしたプロフェッショナルなデザインで、効率的に暗記カードを作成できます。

### ✨ 主な機能
- **本格的なUI**: プログラミングエディタ「VS Code」をイメージした、使いやすく直感的なインターフェース。
- **スマート・ガイダンス**: 次に何をすべきか（保存か、生成か）をアイコンの「青い光」が教えてくれます。
- **自動デザイン**: 美しいCSSが最初から組み込まれており、Ankiのライト/ダークモードにも自動対応。
- **Discord連携**: 設定したWebhookを通じて、生成されたデッキを自動でDiscordに送信します。

### 🛠️ セットアップ（プログラミング初心者向け）
1. **Pythonのインストール**: PCに [Python 3.8以上](https://www.python.org/downloads/) がインストールされていることを確認してください。
2. **コードのダウンロード**: このリポジトリ全体をダウンロードして解凍します。
3. **ライブラリのインストール**: フォルダ内でターミナル（PowerShell等）を開き、以下を実行します：
   ```bash
   pip install -r requirements.txt
   ```
4. **実行**: 
   ```bash
   python run.py
   ```

### 📖 仕様方法
1. **編集**: 中央のエディタに単語データを入力します。
2. **保存**: 左端の **保存（ディスク）アイコン** をクリックします（変更があると青く光ります）。
3. **生成**: **生成（再生）アイコン** をクリックします（保存が完了すると青く光ります）。
4. **受取**: `output` フォルダにデッキが作成されます。Discordを設定していれば自動で送信されます。

---

## 🛠️ Requirements / 必要環境
- Python 3.8+
- [Flet](https://flet.dev/)
- [Genanki](https://github.com/kerrickstaley/genanki)
