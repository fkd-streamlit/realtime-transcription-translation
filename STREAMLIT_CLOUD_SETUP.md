# Streamlit Cloud セットアップ手順

## ステップ1: 「Create app」ボタンをクリック

Streamlit Cloudのダッシュボード（My appsページ）の右上に **「Create app」** ボタンがあります。
このボタンをクリックしてください。

## ステップ2: アプリ情報を入力

「Create app」をクリックすると、以下のフォームが表示されます：

### 入力項目：

1. **Repository（リポジトリ）**
   - ドロップダウンから `fkd-streamlit/realtime-transcription-translation` を選択
   - もし表示されない場合は、検索ボックスで「realtime-transcription-translation」と検索

2. **Branch（ブランチ）**
   - `main` を選択（デフォルト）

3. **Main file path（メインファイルパス）**
   - `app.py` と入力（または `app.py` を選択）

4. **App URL（アプリURL）**（オプション）
   - 自動生成されますが、カスタムURLを設定することも可能
   - 例: `realtime-transcription-translation` → `https://realtime-transcription-translation.streamlit.app`

## ステップ3: 「Deploy!」をクリック

すべての情報を入力したら、右下の **「Deploy!」** ボタンをクリックします。

## ステップ4: デプロイの完了を待つ

- デプロイには数分かかります（初回は5-10分程度）
- 「Deploying...」と表示されている間は待機してください
- 完了すると、アプリのURLが表示されます

## ステップ5: アプリにアクセス

デプロイが完了すると、以下のようなURLが生成されます：
```
https://realtime-transcription-translation.streamlit.app
```

このURLをクリックするか、コピーして他の人と共有できます。

## トラブルシューティング

### リポジトリが表示されない場合

1. GitHubでリポジトリが正しく作成されているか確認
2. Streamlit CloudにGitHubアカウントが正しく連携されているか確認
3. リポジトリがPublicになっているか確認（Privateリポジトリも可能ですが、設定が必要）

### デプロイが失敗する場合

1. **ログを確認**
   - アプリのページで「Logs」タブを確認
   - エラーメッセージを確認

2. **requirements.txtを確認**
   - すべての依存関係が正しく記載されているか確認
   - Streamlit Cloudでサポートされていないパッケージがないか確認

3. **app.pyのパスを確認**
   - Main file pathが `app.py` になっているか確認

### 初回起動が遅い場合

- Whisperモデルのダウンロードに時間がかかります（5-10分程度）
- これは正常な動作です。2回目以降はキャッシュされるため、より高速に起動します

## アプリの管理

デプロイ後、Streamlit Cloudのダッシュボードから：
- アプリのURLを確認・コピー
- アプリの設定を変更
- ログを確認
- アプリを削除

などが可能です。

## 自動デプロイ

GitHubにプッシュするたびに、Streamlit Cloudが自動的にアプリを更新します。
手動での再デプロイは不要です。

