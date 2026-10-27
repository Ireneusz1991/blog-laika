@echo off
chcp 65001 > nul
title Blog Laika - Serwer Lokalny

echo ========================================================
echo         BLOG LAIKA - CMS i Platforma Blogowa
echo   Technologia * Gospodarka * Polityka * Inne eseje
echo ========================================================
echo.
echo Sprawdzanie srodowiska Python...

python --version >nul 2>&1
if errorlevel 1 (
    echo [BLAD] Nie znaleziono Pythona w systemie!
    echo Zainstaluj Python 3.10+ i sprobuj ponownie.
    pause
    exit /b
)

echo Uruchamianie serwera na http://127.0.0.1:8000 ...
echo Aby otworzyc panel CMS, wejdz na: http://127.0.0.1:8000/admin
echo Dane logowania domyslne: admin / laik2026
echo.
echo [Nacisnij CTRL+C, aby zatrzymac serwer]
echo.

start "" "http://127.0.0.1:8000"

python app.py

pause
