@echo off
chcp 65001 >nul
title Auto chay tu file 2 den 5 (Pro 5TB)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set AUTO_FLOW=1

echo ============================================================
echo   LUONG TU DONG CHAY FILE BAT 2 -^> 5 (Google AI Pro 5TB)
echo   - Tu dong an Subscribe khi Module thanh toan hien len
echo   - Gap hop thoai Error -^> Dung ngay bat hien tai, chay bat tiep theo
echo   - Dung lai ngay khi Successful (hoac bam Ctrl + C de thoat)
echo ============================================================

set "FILE_0=2_Pro_12_thang_Buoc_1.bat"
set "FILE_1=3_Pro_Them_6_thang_Buoc_2.bat"
set "FILE_2=4_Pro_Them_6_thang_Buoc_3.bat"
set "FILE_3=5_Pro_Du_phong_6_thang.bat"

for %%F in (
    "%FILE_0%"
    "%FILE_1%"
    "%FILE_2%"
    "%FILE_3%"
) do (
    echo.
    echo ^>^>^> Dang chay: %%~F ...
    call "%%~F"
    if not errorlevel 1 (
        echo.
        echo ============================================================
        echo   [SUCCESSFUL] Thanh cong tai file: %%~F
        echo ============================================================
        goto :done
    )
    echo   [ERROR] %%~F bao loi, chuyen sang file bat tiep theo...
)

echo.
echo ============================================================
echo   Da thu het luot dau 2 -^> 5. Chuyen sang che do RANDOM 2 -^> 5...
echo ============================================================

:random_loop
set /a "IDX=%RANDOM% %% 4"
call set "TARGET=%%FILE_%IDX%%%"
echo.
echo ^>^>^> [RANDOM] Dang chay: %TARGET% ...
call "%TARGET%"
if not errorlevel 1 (
    echo.
    echo ============================================================
    echo   [SUCCESSFUL] Thanh cong tai file: %TARGET%
    echo ============================================================
    goto :done
)
echo   [ERROR] %TARGET% bao loi, random file tiep theo...
goto :random_loop

:done
set AUTO_FLOW=
echo.
pause
