@echo off
chcp 65001 >nul
title Pro +4 thang (g1.2tb.ai.4months_eft)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================
echo   Google AI Pro - 4 thang mien phi (g1.2tb.ai.4months_eft / eft-4months)
echo ============================================
python ultra0.py --account "current@device" --no-add --force --stack --plan pro4 %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
