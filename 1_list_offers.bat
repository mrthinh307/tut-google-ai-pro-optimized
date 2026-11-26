@echo off
chcp 65001 >nul
title List Available Offers (Ultra & Pro - No Purchase)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   LIST ELIGIBLE OFFERS FOR CURRENT ACCOUNT (NO PURCHASE)
echo   (Checks: Gemini AI Ultra 30TB / 20TB ^& Google AI Pro 5TB)
echo ============================================================
python ultra0.py --account "current@device" --no-add --force --list --plan all %*
echo.
pause
