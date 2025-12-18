@echo off
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
    echo プロジェクトディレクトリに移動してから実行してください。
    echo.
    echo 例:
    echo   cd "C:\Users\FMV\Desktop\リアルタイム文字起こしと翻訳"
    echo   push_to_github.bat
    pause
    exit /b 1
)

echo [1/3] Gitの状態を確認しています...
git status
echo.

echo [2/3] リモートリポジトリを設定しています...
echo.
echo リポジトリのURLを入力してください:
echo 例: https://github.com/fkd-streamlit/realtime-transcription-translation.git
echo.
set /p REPO_URL="リポジトリURL: "

if "%REPO_URL%"=="" (
    echo [エラー] URLが入力されていません。
    pause
    exit /b 1
)

REM 既存のリモートを削除（エラーを無視）
git remote remove origin >nul 2>&1

REM リモートを追加
git remote add origin %REPO_URL%
if errorlevel 1 (
    echo [エラー] リモートリポジトリの追加に失敗しました。
    pause
    exit /b 1
)

echo [3/3] GitHubにプッシュしています...
echo.
echo ⚠️  認証情報が求められます:
echo     - ユーザー名: fkd-streamlit
echo     - パスワード: Personal Access Token（通常のパスワードではありません）
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo [エラー] プッシュに失敗しました。
    echo.
    echo 確認事項:
    echo 1. Personal Access Tokenを使用していますか？
    echo 2. リポジトリURLが正しいですか？
    echo 3. リポジトリが作成されていますか？
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ プッシュ完了！
echo ========================================
echo.
echo リポジトリURL: %REPO_URL%
echo.
pause

