@echo off
chcp 65001 >nul
title g1.30tb.12months_eft (Google One Ultra 30TB - 12 Months Trial)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   PACKAGE: Google One Ultra 30TB
echo   SKU: g1.30tb.12months_eft
echo   TRIAL PERIOD: 12 Months (FREE $0.00)
echo   ----------------------------------------------------------
echo   Notice: Verify payment sheet displays 12-month trial ($0.00).
echo          DO NOT confirm if any charge is due today!
echo ============================================================
python ultra0.py --account "current@device" --no-add --force --plan g1.30tb.12months_eft %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
