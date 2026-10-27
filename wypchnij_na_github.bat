@echo off
chcp 65001 > nul
title Publikacja na GitHub - Blog Laika

echo ========================================================
echo         PUBLIKACJA REPOZYTORIUM NA GITHUB
echo ========================================================
echo.
cd /d "C:\Users\irene\blog-laika"

echo Czy chcesz utworzyc automatycznie repozytorium przez GitHub CLI (gh),
echo czy podac adres istniejacego repozytorium?
echo.
echo [1] Utworz automatycznie przez GitHub CLI (wymaga jednorazowego 'gh auth login')
echo [2] Podaj adres URL istniejacego repozytorium (np. https://github.com/user/blog-laika.git)
echo.
set /p wybor="Wybierz opcje [1 lub 2]: "

if "%wybor%"=="1" (
    echo.
    echo Logowanie / sprawdzanie sesji GitHub CLI...
    gh auth status
    if errorlevel 1 (
        echo.
        echo Zaloguj sie do GitHub (wybierz GitHub.com, HTTPS, Web browser):
        gh auth login -w -p https
    )
    echo Tworzenie publicznego repozytorium na GitHubie...
    gh repo create blog-laika --public --source=. --push
    echo.
    echo Gotowe! Twoje repozytorium jest dostepne na GitHubie!
) else if "%wybor%"=="2" (
    set /p repourl="Wklej adres URL repozytorium: "
    git remote set-url origin %repourl% 2>nul || git remote add origin %repourl%
    git push -u origin main
    echo.
    echo Wypchnieto zmiany na GitHub!
) else (
    echo Nieprawidlowy wybor.
)

pause
