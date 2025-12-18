# アプリの公開・共有方法ガイド

このアプリを他の人と共有する方法は複数あります。用途に応じて選択してください。

## 方法1: Streamlit Cloud（推奨・無料）

**メリット:**
- ✅ ブラウザからアクセスできるWebアプリとして公開
- ✅ 無料で利用可能
- ✅ 自動デプロイ（GitHubにプッシュするだけで自動更新）
- ✅ アカウント不要でアクセス可能

**デメリット:**
- ⚠️ 初回起動時にWhisperモデルのダウンロードが必要（時間がかかる）
- ⚠️ 無料プランはリソース制限あり

### セットアップ手順

1. **GitHubにプッシュ済みであることを確認**
   ```bash
   # 既にプッシュ済みならOK
   ```

2. **Streamlit Cloudにアクセス**
   - https://streamlit.io/cloud にアクセス
   - 「Sign up」をクリック
   - GitHubアカウントでログイン（`fkd-streamlit`でログイン）

3. **アプリをデプロイ**
   - 「New app」ボタンをクリック
   - 以下の情報を入力：
     - **Repository**: `fkd-streamlit/realtime-transcription-translation` を選択
     - **Branch**: `main`
     - **Main file path**: `app.py`
   - 「Deploy!」をクリック

4. **デプロイ完了**
   - 数分待つと、アプリのURLが生成されます
   - 例: `https://realtime-transcription-translation.streamlit.app`
   - このURLを共有すれば、誰でもブラウザからアクセスできます！

### 注意事項

- 初回起動時、Whisperモデルのダウンロードに時間がかかります（5-10分程度）
- 無料プランでは、一定時間アクセスがないとスリープします
- 大きな音声ファイルの処理には時間がかかる場合があります

---

## 方法2: GitHubからクローンしてローカル実行

**メリット:**
- ✅ 完全にローカルで動作（プライバシー重視）
- ✅ インターネット接続不要（初回ダウンロード後）
- ✅ カスタマイズ可能

**デメリット:**
- ⚠️ 各ユーザーが環境構築が必要
- ⚠️ Pythonとffmpegのインストールが必要

### 他の人が使用する方法

1. **リポジトリをクローン**
   ```bash
   git clone https://github.com/fkd-streamlit/realtime-transcription-translation.git
   cd realtime-transcription-translation
   ```

2. **依存関係をインストール**
   ```bash
   pip install -r requirements.txt
   ```

3. **ffmpegをインストール**（未インストールの場合）
   - Windows: https://ffmpeg.org/download.html
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

4. **アプリを起動**
   ```bash
   streamlit run app.py
   ```

---

## 方法3: ZIPファイルで共有

**メリット:**
- ✅ GitHubアカウント不要
- ✅ 簡単に共有可能

**デメリット:**
- ⚠️ 更新が困難
- ⚠️ 各ユーザーが環境構築が必要

### 手順

1. **プロジェクトフォルダをZIP圧縮**
   - `.git`フォルダは除外（ZIPサイズを小さくするため）

2. **ZIPファイルを共有**
   - メール、クラウドストレージ（Google Drive、Dropboxなど）で共有

3. **受け取った人が使用**
   - ZIPを解凍
   - 依存関係をインストール: `pip install -r requirements.txt`
   - アプリを起動: `streamlit run app.py`

---

## 方法4: Dockerコンテナ化（上級者向け）

**メリット:**
- ✅ 環境の違いを気にせず実行可能
- ✅ 一貫した動作が保証される

**デメリット:**
- ⚠️ Dockerの知識が必要
- ⚠️ Dockerのインストールが必要

### Dockerfileの例

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 推奨される共有方法

### 一般的な用途
→ **Streamlit Cloud**（方法1）
- 最も簡単で、ブラウザからアクセス可能
- URLを共有するだけ

### プライバシー重視・オフライン使用
→ **GitHubからクローン**（方法2）
- 完全にローカルで動作
- データが外部に送信されない

### 一時的な共有・GitHub不要
→ **ZIPファイル**（方法3）
- 簡単に共有可能
- 環境構築が必要

---

## Streamlit Cloudの詳細設定

### 設定ファイル（`.streamlit/config.toml`）の作成

プロジェクトルートに `.streamlit/config.toml` を作成すると、Streamlit Cloudの設定をカスタマイズできます：

```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### 環境変数の設定

Streamlit Cloudのダッシュボードで環境変数を設定できます（このアプリでは不要ですが、将来的にAPIキーなどが必要な場合に使用）。

---

## トラブルシューティング

### Streamlit Cloudでデプロイが失敗する場合

1. **requirements.txtを確認**
   - すべての依存関係が正しく記載されているか確認

2. **app.pyのパスを確認**
   - Main file pathが `app.py` になっているか確認

3. **ログを確認**
   - Streamlit Cloudのダッシュボードで「Logs」タブを確認

### ローカルで起動できない場合

1. **Pythonのバージョン確認**
   ```bash
   python --version  # 3.8以上が必要
   ```

2. **依存関係の再インストール**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **ffmpegの確認**
   ```bash
   ffmpeg -version
   ```

