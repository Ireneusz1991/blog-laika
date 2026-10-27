@echo off
chcp 65001 > nul
title Publikacja na GitHub - Blog Laika

cd /d "%~dp0"

echo Uruchamianie kreatora publikacji...
echo.

python publish_github.py

if errorlevel 1 (
    echo.
    echo Wystapil problem podczas uruchamiania.
)

echo.
echo ========================================================
echo Okno nie zamknie sie dopoki nie nacisniesz klawisza.
pause
