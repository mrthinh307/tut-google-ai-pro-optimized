@echo off
chcp 65001 >nul
title Pro +6 thang (du phong)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================
echo   Google AI Pro 5TB - them 6 thang du phong (ss-2026)
echo ============================================
python ultra0.py --account "current@device" --no-add --force --stack --plan pro6c %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
