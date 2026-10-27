@echo off
chcp 65001 > nul
title Publikacja Blog Laika na GitHub Pages

echo ========================================================
echo     BLOG LAIKA — PUBLIKACJA NA GITHUB PAGES
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/3] Kompilacja wersji statycznej z bazy danych...
python export_static.py
if errorlevel 1 (
    echo [BLAD] Kompilacja nie powiodla sie!
    pause
    exit /b
)

echo.
echo [2/3] Aktualizacja galezi gh-pages...
set "GIT=C:\Users\irene\AppData\Local\Programs\Git\cmd\git.exe"
set "DIST_TMP=%TEMP%\blog-laika-gh-pages"

rmdir /s /q "%DIST_TMP%" 2>nul
mkdir "%DIST_TMP%" 2>nul
xcopy /E /I /Y "dist\*" "%DIST_TMP%\" >nul

"%GIT%" -C "%DIST_TMP%" init -b gh-pages >nul
"%GIT%" -C "%DIST_TMP%" config user.name "Blog Laika"
"%GIT%" -C "%DIST_TMP%" config user.email "kontakt@bloglaika.pl"
"%GIT%" -C "%DIST_TMP%" add .
"%GIT%" -C "%DIST_TMP%" commit -m "Aktualizacja publikacji na GitHub Pages" >nul
"%GIT%" -C "%DIST_TMP%" remote add origin "https://github.com/Ireneusz1991/blog-laika.git"
"%GIT%" -C "%DIST_TMP%" push origin gh-pages --force

echo.
echo [3/3] Zapisywanie zmian na glownej galezi main...
"%GIT%" -C "C:\Users\irene\blog-laika" add .
"%GIT%" -C "C:\Users\irene\blog-laika" commit -m "Zapis zmian tresci bloga" >nul 2>nul
"%GIT%" -C "C:\Users\irene\blog-laika" push origin main 2>nul

echo.
echo ========================================================
echo [SUKCES] Twoj blog zostal opublikowany na GitHub Pages!
echo Adres: https://ireneusz1991.github.io/blog-laika/
echo ========================================================
echo.
pause
