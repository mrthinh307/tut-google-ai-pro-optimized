@echo off
chcp 65001 >nul
title Pro +12 thang EFT (g1.2tb.ai.12months_eft)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================
echo   Google AI Pro - 12 thang mien phi EFT (g1.2tb.ai.12months_eft / eft-12months)
echo ============================================
python ultra0.py --account "current@device" --no-add --force --stack --plan pro12eft %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
