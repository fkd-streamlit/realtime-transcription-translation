# クイックスタートガイド

既にGitHubアカウントをお持ちの場合の簡単な手順です。

## ステップ1: GitHubでリポジトリを作成

1. GitHubのダッシュボードで、左上の「New」ボタン（緑色のボタン）をクリック
   - または https://github.com/new にアクセス

2. リポジトリ情報を入力：
   - **Repository name**: `realtime-transcription-translation`（任意の名前）
   - **Description**: `リアルタイム文字起こしと翻訳アプリ - faster-whisper使用`
   - **Public** または **Private** を選択
   - ⚠️ **「Add a README file」などのチェックは外してください**（既にファイルがあるため）

3. 「Create repository」をクリック

4. 作成されたリポジトリのページで、**URLをコピー**してください
   - 例: `https://github.com/fkd-streamlit/realtime-transcription-translation.git`

## ステップ2: ローカルでGitを初期化

### 方法A: 自動スクリプトを使用（推奨）

1. **`setup_git.bat`をダブルクリック**
   - Gitの初期化とコミットが自動で実行されます

### 方法B: 手動でコマンドを実行

PowerShellまたはコマンドプロンプトで：

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
```

## ステップ3: GitHubにプッシュ

PowerShellまたはコマンドプロンプトで：

```powershell
# ⚠️ 以下のURLを、ステップ1で作成したリポジトリのURLに置き換えてください
git remote add origin https://github.com/fkd-streamlit/リポジトリ名.git

# GitHubにプッシュ
git push -u origin main
```

### 認証について

初回プッシュ時、認証情報が求められます：

**方法1: Personal Access Token（推奨）**
- GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- 「Generate new token (classic)」をクリック
- トークン名を入力（例: `realtime-transcription`）
- 有効期限を選択
- **`repo`** 権限にチェック
- 「Generate token」をクリック
- 表示されたトークンをコピー（再表示されないので注意）
- ユーザー名: `fkd-streamlit`
- パスワード: **コピーしたトークン**（通常のパスワードではない）

**方法2: GitHub CLI**
```powershell
# GitHub CLIをインストール後
gh auth login
```

## ステップ4: 確認

GitHubのリポジトリページをリロードして、ファイルがアップロードされているか確認してください。

## 完了！

これで、他の人にリポジトリのURLを共有できます：

```
https://github.com/fkd-streamlit/リポジトリ名
```

他の人は以下のコマンドで使用できます：

```bash
git clone https://github.com/fkd-streamlit/リポジトリ名.git
cd リポジトリ名
pip install -r requirements.txt
streamlit run app.py
```

## トラブルシューティング

### 「remote origin already exists」エラー

既にリモートが設定されている場合：
```powershell
git remote remove origin
git remote add origin https://github.com/fkd-streamlit/リポジトリ名.git
```

### 認証エラー

Personal Access Tokenを使用しているか確認してください。通常のパスワードでは動作しません。

### Gitがインストールされていない

[Git for Windows](https://git-scm.com/download/win)をダウンロードしてインストールしてください。

