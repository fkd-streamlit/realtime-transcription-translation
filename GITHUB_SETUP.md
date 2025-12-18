# GitHubでの共有手順

このアプリをGitHubで共有するための詳細な手順です。

## 方法1: GitHubリポジトリを作成してプッシュ

### ステップ1: GitHubでリポジトリを作成

1. [GitHub](https://github.com)にアクセスしてログイン
2. 右上の「+」ボタン → 「New repository」をクリック
3. 以下の情報を入力：
   - **Repository name**: `realtime-transcription-translation`（任意の名前）
   - **Description**: `リアルタイム文字起こしと翻訳アプリ - faster-whisper使用`
   - **Public** または **Private** を選択
   - **Initialize this repository with** のチェックは外す（既にファイルがあるため）
4. 「Create repository」をクリック

### ステップ2: ローカルでGitを初期化してプッシュ

PowerShellまたはコマンドプロンプトで以下のコマンドを実行：

```powershell
# 現在のディレクトリに移動（既にいる場合は不要）
cd "C:\Users\FMV\Desktop\リアルタイム文字起こしと翻訳"

# Gitを初期化
git init

# すべてのファイルを追加
git add .

# 初回コミット
git commit -m "Initial commit: リアルタイム文字起こしと翻訳アプリ"

# メインブランチに設定
git branch -M main

# GitHubリポジトリをリモートとして追加
# ⚠️ 以下のURLを、あなたが作成したリポジトリのURLに置き換えてください
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git

# GitHubにプッシュ
git push -u origin main
```

### ステップ3: 認証

初回プッシュ時、GitHubの認証情報が求められます：
- **ユーザー名**: GitHubのユーザー名
- **パスワード**: Personal Access Token（PAT）を使用
  - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  - 「Generate new token」で新しいトークンを作成
  - `repo`権限を選択
  - トークンをコピーしてパスワードとして使用

## 方法2: GitHub Desktopを使用（GUIで簡単）

1. [GitHub Desktop](https://desktop.github.com/)をダウンロード・インストール
2. GitHub Desktopを起動してGitHubアカウントでログイン
3. 「File」→「Add Local Repository」
4. フォルダを選択: `C:\Users\FMV\Desktop\リアルタイム文字起こしと翻訳`
5. 「Publish repository」をクリック
6. リポジトリ名を入力して「Publish」をクリック

## 方法3: ZIPファイルで共有（GitHub不要）

GitHubを使わずに共有する場合：

1. プロジェクトフォルダをZIP圧縮
2. ZIPファイルを共有（メール、クラウドストレージなど）
3. 受け取った人は：
   ```bash
   # ZIPを解凍
   # 依存関係をインストール
   pip install -r requirements.txt
   # アプリを起動
   streamlit run app.py
   ```

## 方法4: Streamlit Cloudで公開（無料ホスティング）

Streamlit Cloudを使えば、ブラウザでアクセスできるWebアプリとして公開できます：

1. GitHubにプッシュ（方法1または2を実行）
2. [Streamlit Cloud](https://streamlit.io/cloud)にアクセス
3. 「Sign up」→ GitHubアカウントでログイン
4. 「New app」をクリック
5. リポジトリを選択
6. Main file path: `app.py` を指定
7. 「Deploy」をクリック

これで、誰でもブラウザからアクセスできるWebアプリになります！

## 他の人が使用する方法

GitHubリポジトリのURLを共有したら、他の人は以下のコマンドで使用できます：

```bash
# リポジトリをクローン
git clone https://github.com/あなたのユーザー名/リポジトリ名.git

# ディレクトリに移動
cd リポジトリ名

# 依存関係をインストール
pip install -r requirements.txt

# アプリを起動
streamlit run app.py
```

## トラブルシューティング

### Gitがインストールされていない場合

[Git for Windows](https://git-scm.com/download/win)をダウンロードしてインストールしてください。

### 認証エラーが発生する場合

Personal Access Tokenを使用しているか確認してください。パスワードではなくトークンを使用します。

### プッシュが拒否される場合

リモートリポジトリのURLが正しいか確認してください：
```bash
git remote -v
```

間違っている場合は削除して再追加：
```bash
git remote remove origin
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
```

