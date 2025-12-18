@echo off
echo ========================================
echo GitHub共有セットアップスクリプト
echo ========================================
echo.

REM Gitがインストールされているか確認
git --version >nul 2>&1
if errorlevel 1 (
    echo [エラー] Gitがインストールされていません。
    echo Git for Windowsをインストールしてください: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Gitを初期化しています...
git init
if errorlevel 1 (
    echo [エラー] Gitの初期化に失敗しました。
    pause
    exit /b 1
)

echo [2/5] ファイルを追加しています...
git add .
if errorlevel 1 (
    echo [エラー] ファイルの追加に失敗しました。
    pause
    exit /b 1
)

echo [3/5] 初回コミットを作成しています...
git commit -m "Initial commit: リアルタイム文字起こしと翻訳アプリ"
if errorlevel 1 (
    echo [警告] コミットに失敗しました。既にコミット済みの可能性があります。
)

echo [4/5] メインブランチに設定しています...
git branch -M main

echo.
echo ========================================
echo セットアップ完了！
echo ========================================
echo.
echo 次のステップ:
echo 1. GitHubでリポジトリを作成してください
echo    https://github.com/new
echo.
echo 2. 以下のコマンドを実行してプッシュしてください:
echo    git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
echo    git push -u origin main
echo.
echo 詳細は GITHUB_SETUP.md を参照してください。
echo.
pause

