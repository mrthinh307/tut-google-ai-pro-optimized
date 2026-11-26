@echo off
chcp 65001 >nul
title Environment Check
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================================
echo   Checking Emulator / Frida Server / Billing Module
echo ============================================================
python ultra0.py --check
echo.
pause
