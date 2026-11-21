@echo off
chcp 65001 >nul
title Auto chay tu file 2 den 6 (Pro 5TB)
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set AUTO_FLOW=1

echo ============================================================
echo   LUONG TU DONG CHAY FILE BAT 2 -^> 6 (Google AI Pro 5TB)
echo   - Mac dinh KHONG tu dong bam Subscribe (them --auto-subcribe de bat)
echo   - Gap hop thoai Error -^> Dung ngay bat hien tai, chay bat tiep theo
echo   - Dung lai ngay khi Successful (hoac het luot dau)
echo ============================================================

set "FILE_0=6_Pro_3_thang_eft.bat"
set "FILE_1=2_Pro_12_thang_Buoc_1.bat"
set "FILE_2=3_Pro_Them_6_thang_Buoc_2.bat"
set "FILE_3=4_Pro_Them_6_thang_Buoc_3.bat"
set "FILE_4=5_Pro_Du_phong_6_thang.bat"

for %%F in (
    "%FILE_0%"
    "%FILE_1%"
    "%FILE_2%"
    "%FILE_3%"
    "%FILE_4%"
) do (
    echo.
    echo ^>^>^> Dang chay: %%~F ...
    call "%%~F" %*
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
echo   Da thu het luot dau (6, 2 -^> 5), khong co file nao thanh cong.
echo ============================================================

:done
set AUTO_FLOW=
echo.
pause
