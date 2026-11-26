@echo off
chcp 65001 >nul
title g1.2tb.ai.4months_eft (Google AI Pro - 4 Months EFT)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   PACKAGE: Google AI Pro (Extended Free Trial)
echo   SKU: g1.2tb.ai.4months_eft ^| OFFER: eft-4months
echo   TRIAL PERIOD: 4 Months (FREE $0.00)
echo   ----------------------------------------------------------
echo   Notice: Verify payment sheet displays 4-month trial ($0.00).
echo          DO NOT confirm if any charge is due today!
echo ============================================================
python ultra0.py --account "current@device" --no-add --force --stack --plan g1.2tb.ai.4months_eft %*
set EXIT_CODE=%ERRORLEVEL%
if defined AUTO_FLOW exit /b %EXIT_CODE%
echo.
pause
exit /b %EXIT_CODE%
