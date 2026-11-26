@echo off
chcp 65001 >nul
title Auto Run Google AI Pro 5TB Packages
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set AUTO_FLOW=1

echo ============================================================
echo   AUTOMATED SEQUENCE FOR Google AI Pro 5TB
echo   - Default does NOT automatically click Subscribe (use --auto-subscribe to enable)
echo   - On Error dialog -^> Immediately exit current batch, run next offer
echo   - Stops on Successful execution (or after all attempts exhausted)
echo ============================================================

set "FILE_0=g1.2tb.ai.3months_eft.bat"
set "FILE_1=12months-eft.bat"
set "FILE_2=6months-eft.bat"
set "FILE_3=6months-eft-2.bat"
set "FILE_4=6months-eft-ss-2026.bat"

for %%F in (
    "%FILE_0%"
    "%FILE_1%"
    "%FILE_2%"
    "%FILE_3%"
    "%FILE_4%"
) do (
    echo.
    echo ^>^>^> Running: %%~F ...
    call "%%~F" %*
    if not errorlevel 1 (
        echo.
        echo ============================================================
        echo   [SUCCESSFUL] Completed successfully with: %%~F
        echo ============================================================
        goto :done
    )
    echo   [ERROR] %%~F returned error, switching to next batch file...
)

echo.
echo ============================================================
echo   Tried all primary batch files. None succeeded.
echo ============================================================

:done
set AUTO_FLOW=
echo.
pause
