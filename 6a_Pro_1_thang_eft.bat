@echo off
chcp 65001 >nul
title Pro +1 thang (g1.2tb.ai.1month_eft)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================
echo   Google AI Pro - 1 thang mien phi (g1.2tb.ai.1month_eft / eft-1month)
echo ============================================
python ultra0.py --account "current@device" --no-add --force --stack --plan pro1 %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
