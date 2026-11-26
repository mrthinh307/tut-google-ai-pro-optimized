@echo off
chcp 65001 >nul
title 6months-eft (Google AI Pro 5TB - Stack +6 Months)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   PACKAGE: Google AI Pro 5TB (Stack Extension - Step 2)
echo   SKU: g1.2tb.ai.subs_variant ^| OFFER: 6months-eft
echo   TRIAL PERIOD: +6 Months Extension (FREE $0.00)
echo   ----------------------------------------------------------
echo   Notice: Only run when an active subscription exists.
echo          DO NOT confirm if any charge is due today!
echo ============================================================
python ultra0.py --account "current@device" --no-add --force --stack --plan 6months-eft %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
