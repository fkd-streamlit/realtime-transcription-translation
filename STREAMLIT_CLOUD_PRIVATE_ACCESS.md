# Streamlit Cloudのプライベートリポジトリアクセス設定

Streamlit Cloudの設定画面に「Private access」の警告が表示されている場合、以下の対処が必要です。

## 問題

Streamlit Cloudがプライベートリポジトリにアクセスできないという警告が表示されています。

## 解決方法

### 方法1: リポジトリをPublicに変更（推奨・簡単）

1. **GitHubでリポジトリを開く**
   - https://github.com/fkd-streamlit/realtime-transcription-translation にアクセス

2. **Settingsタブをクリック**
   - リポジトリページの上部のタブから「Settings」を選択

3. **リポジトリの公開設定を変更**
   - ページの一番下までスクロール
   - 「Danger Zone」セクションを探す
   - 「Change visibility」をクリック
   - 「Change to public」を選択
   - リポジトリ名を入力して確認

4. **Streamlit Cloudで再試行**
   - Streamlit Cloudのデプロイ画面に戻る
   - ページをリロード（F5キー）
   - 再度デプロイを試みる

### 方法2: Streamlit Cloudにプライベートアクセス権限を付与

プライベートリポジトリのまま使用したい場合：

1. **Streamlit Cloudの設定画面で**
   - 「Private access」セクションの「Connect here →」リンクをクリック

2. **GitHubで権限を付与**
   - GitHubの認証画面が開きます
   - Streamlit Cloudにプライベートリポジトリへのアクセス権限を付与
   - 必要な権限を確認して承認

3. **Streamlit Cloudで再試行**
   - 設定画面に戻る
   - 「Private access」の警告が消えているか確認
   - デプロイを再試行

## 推奨事項

一般的には、**方法1（Publicに変更）**が最も簡単です。

- このアプリは機密情報を含まないため、Publicでも問題ありません
- Streamlit Cloudの無料プランで簡単にデプロイできます
- 他の人も簡単にアクセスできます

## 次のステップ

1. GitHubでリポジトリをPublicに変更
2. Streamlit Cloudのデプロイ画面をリロード
3. Repository: `fkd-streamlit/realtime-transcription-translation` を選択
4. Branch: `main`
5. Main file path: `app.py`
6. 「Deploy!」をクリック

## 確認事項

GitHubにプッシュが完了しているか確認：

```powershell
# プロジェクトディレクトリで
cd "C:\Users\FMV\Desktop\リアルタイム文字起こしと翻訳"

# GitHubの状態を確認
git log --oneline -1
git remote -v
```

GitHubのリポジトリページで以下を確認：
- `app.py`ファイルが表示されているか
- `main`ブランチが存在するか
- リポジトリがPublicかPrivateか

