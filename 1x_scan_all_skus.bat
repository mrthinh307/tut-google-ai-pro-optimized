@echo off
chcp 65001 >nul
title Scan All Google One / Gemini AI SKUs
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   SCAN ALL GOOGLE ONE SKUS ^& OFFERS (GEMINI ULTRA / PRO)
echo   (AI Ultra 30TB / 20TB, AI Pro, 12-Month EFT, 90%% Off...)
echo ============================================================
echo.
python query_sku.py %*
echo.
pause
