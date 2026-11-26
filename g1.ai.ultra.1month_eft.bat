@echo off
chcp 65001 >nul
title g1.ai.ultra.1month_eft (Gemini AI Ultra 30TB - 1 Month Trial)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   PACKAGE: Gemini AI Ultra 30TB (Promo SKU [104])
echo   SKU: g1.ai.ultra.1month_eft
echo   TRIAL PERIOD: 1 Month (FREE $0.00)
echo   ----------------------------------------------------------
echo   Notice: Verify payment sheet displays 1-month trial ($0.00).
echo          DO NOT confirm if any charge is due today!
echo ============================================================
python ultra0.py --account "current@device" --no-add --force --plan g1.ai.ultra.1month_eft %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
