@echo off
chcp 65001 >nul
title Pro +3 thang (g1.2tb.ai.3months_eft)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================
echo   Google AI Pro - 3 thang mien phi (g1.2tb.ai.3months_eft / eft-3months)
echo ============================================
python ultra0.py --account "current@device" --no-add --force --stack --plan pro3
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
