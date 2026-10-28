# PowerShell: Codzienne poranne wyszukiwanie tematów i publikacja Blog Laika
Write-Host "=== [Blog Laika] Rozpoczynanie porannego wyszukiwania tematów ===" -ForegroundColor Cyan

$RepoPath = Split-Path -Parent $PSScriptRoot
Set-Location $RepoPath

# 1. Uruchomienie generatora tematów
Write-Host "[1/3] Generowanie propozycji w modelu Samokreacji (7 dni x 4 tematy)..." -ForegroundColor Yellow
python scripts/generate_proposals.py

# 2. Kompilacja wersji statycznej
Write-Host "[2/3] Kompilacja platformy statycznej..." -ForegroundColor Yellow
python export_static.py

# 3. Informacja o sukcesie
Write-Host "[3/3] Gotowe! Najnowszy zestaw tematów z grafikami załadowany do CMS." -ForegroundColor Green
Write-Host "Otwórz panel: https://blog-laika.com/admin/ lub lokalnie: file://$RepoPath/dist/admin/index.html" -ForegroundColor Cyan
