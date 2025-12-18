@echo off
chcp 65001 >nul
echo ========================================
echo GitHubにプッシュするスクリプト
echo ========================================
echo.

REM 現在のディレクトリを確認
echo 現在のディレクトリ: %CD%
echo.

REM Gitリポジトリか確認
git status >nul 2>&1
if errorlevel 1 (
    echo [エラー] このディレクトリはGitリポジトリではありません。
    echo.
    echo まず setup_git.bat を実行してください。
    pause
    exit /b 1
)

echo [1/4] Gitの状態を確認...
git status
echo.

echo [2/4] リモートリポジトリを設定...
REM 既存のリモートを削除（エラーを無視）
git remote remove origin >nul 2>&1

REM リモートを追加
git remote add origin https://github.com/fkd-streamlit/realtime-transcription-translation.git
if errorlevel 1 (
    echo [警告] リモートが既に設定されている可能性があります。
    git remote set-url origin https://github.com/fkd-streamlit/realtime-transcription-translation.git
)

echo ✅ リモートリポジトリを設定しました
echo    https://github.com/fkd-streamlit/realtime-transcription-translation.git
echo.

echo [3/4] メインブランチを確認...
git branch -M main
echo.

echo [4/4] GitHubにプッシュします...
echo.
echo ⚠️  認証情報が求められます:
echo     - ユーザー名: fkd-streamlit
echo     - パスワード: Personal Access Token（通常のパスワードではありません）
echo.
echo Personal Access Tokenの作成方法:
echo 1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
echo 2. Generate new token (classic) をクリック
echo 3. repo 権限にチェック
echo 4. トークンを生成してコピー
echo.
pause

git push -u origin main

if errorlevel 1 (
    echo.
    echo [エラー] プッシュに失敗しました。
    echo.
    echo 確認事項:
    echo 1. Personal Access Tokenを使用していますか？（通常のパスワードではありません）
    echo 2. リポジトリが作成されていますか？
    echo 3. インターネット接続は正常ですか？
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ プッシュ完了！
echo ========================================
echo.
echo リポジトリURL:
echo https://github.com/fkd-streamlit/realtime-transcription-translation
echo.
echo ブラウザで確認してください！
echo.
pause

