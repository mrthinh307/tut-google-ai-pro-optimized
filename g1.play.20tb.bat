@echo off
chcp 65001 >nul
title g1.play.20tb (Gemini AI Ultra 20TB - Original Ultra 5x - 12 Months)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   PACKAGE: Gemini AI Ultra 20TB (Original Ultra 5x)
echo   SKU: g1.play.20tb ^| OFFER: eft-12month
echo   TRIAL PERIOD: 12 Months (FREE $0.00)
echo   ----------------------------------------------------------
echo   Notice: Verify payment sheet displays 12-month trial ($0.00).
echo          DO NOT confirm if any charge is due today!
echo ============================================================
python ultra0.py --account "current@device" --no-add --force --plan 5x %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
