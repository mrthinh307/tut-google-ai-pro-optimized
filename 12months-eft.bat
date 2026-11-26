@echo off
chcp 65001 >nul
title 12months-eft (Google AI Pro 5TB - 12 Months Trial)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   PACKAGE: Google AI Pro 5TB (Primary Plan - Step 1)
echo   SKU: g1.2tb.ai.subs_variant ^| OFFER: 12months-eft
echo   TRIAL PERIOD: 12 Months (FREE $0.00)
echo   ----------------------------------------------------------
echo   Notice: Ensure payment sheet explicitly states:
echo          "Free trial for 12 months" ($0.00 today).
echo          DO NOT confirm if it shows 1 month or any price!
echo ============================================================
python ultra0.py --account "current@device" --no-add --force --plan 12months-eft %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
