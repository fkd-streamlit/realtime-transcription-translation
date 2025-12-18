# GitHubプッシュの認証エラーを解決する方法

認証エラーが発生しています。Personal Access Tokenを使用してプッシュする必要があります。

## ステップ1: Personal Access Tokenを作成

1. **GitHubにログイン**
   - https://github.com にアクセス
   - `fkd-streamlit`アカウントでログイン

2. **Settingsに移動**
   - 右上のプロフィール画像をクリック
   - 「Settings」をクリック

3. **Developer settingsに移動**
   - 左サイドバーの一番下「Developer settings」をクリック

4. **Personal access tokensに移動**
   - 「Personal access tokens」→「Tokens (classic)」をクリック

5. **新しいトークンを生成**
   - 「Generate new token」→「Generate new token (classic)」をクリック
   - 以下の情報を入力：
     - **Note**: `realtime-transcription`（任意の名前）
     - **Expiration**: 適切な期間を選択（例: 90 days）
     - **Select scopes**: **`repo`** にチェック（すべてのリポジトリ権限）
   - 「Generate token」をクリック

6. **トークンをコピー**
   - 表示されたトークンを**すぐにコピー**してください（再表示されません）
   - 例: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## ステップ2: Gitの認証情報を更新

### 方法A: コマンドラインでプッシュ（推奨）

PowerShellで以下のコマンドを実行：

```powershell
# プロジェクトディレクトリに移動
cd "C:\Users\FMV\Desktop\リアルタイム文字起こしと翻訳"

# プッシュ（認証情報が求められます）
git push -u origin main
```

認証情報を求められたら：
- **Username**: `fkd-streamlit`
- **Password**: **コピーしたPersonal Access Token**（通常のパスワードではありません）

### 方法B: Git Credential Managerを使用

Windowsの認証情報マネージャーをクリアして再設定：

```powershell
# 既存の認証情報を削除
git credential-manager-core erase
# または
git credential reject https://github.com

# 再度プッシュ
git push -u origin main
```

### 方法C: URLにトークンを含める（一時的）

```powershell
# リモートURLを更新（トークンを直接含める）
git remote set-url origin https://fkd-streamlit:YOUR_TOKEN@github.com/fkd-streamlit/realtime-transcription-translation.git

# プッシュ
git push -u origin main
```

⚠️ **注意**: この方法はセキュリティ上推奨されません。使用後は履歴をクリアしてください。

## ステップ3: プッシュの確認

プッシュが成功すると、以下のようなメッセージが表示されます：

```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
To https://github.com/fkd-streamlit/realtime-transcription-translation.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## ステップ4: GitHubで確認

1. https://github.com/fkd-streamlit/realtime-transcription-translation にアクセス
2. `app.py`ファイルが表示されているか確認
3. `main`ブランチが存在するか確認

## ステップ5: Streamlit Cloudで再試行

GitHubにプッシュが完了したら、Streamlit Cloudのデプロイ画面に戻って：

1. ページを**リロード**（F5キー）
2. Repository: `fkd-streamlit/realtime-transcription-translation` を選択
3. Branch: `main`
4. Main file path: `app.py`
5. 「Deploy!」をクリック

## トラブルシューティング

### 「Permission denied」エラーが続く場合

1. Personal Access Tokenが正しくコピーされているか確認
2. `repo`権限が付与されているか確認
3. トークンの有効期限が切れていないか確認

### 別のユーザーで認証されている場合

```powershell
# 現在の認証情報を確認
git config --global user.name
git config --global user.email

# 必要に応じて変更
git config --global user.name "fkd-streamlit"
git config --global user.email "your-email@example.com"
```

