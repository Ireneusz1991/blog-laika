@echo off
set PYTHONIOENCODING=utf-8
cd /d "%~dp0.."
echo ======================================================== >> "%~dp0cron_last_run.log"
echo [CRON START] %DATE% %TIME% >> "%~dp0cron_last_run.log"
echo ======================================================== >> "%~dp0cron_last_run.log"
if exist ".git" (
    "C:\Users\irene\AppData\Local\Programs\Git\cmd\git.exe" pull --rebase origin main >> "%~dp0cron_last_run.log" 2>&1
)
"C:\Users\irene\AppData\Local\Programs\Python\Python312\python.exe" "scripts\daily_editorial_cron.py" --deploy --trigger-label "Windows Backup Cron" >> "%~dp0cron_last_run.log" 2>&1
if exist ".git" (
    "C:\Users\irene\AppData\Local\Programs\Git\cmd\git.exe" add propozycje-tematow data >> "%~dp0cron_last_run.log" 2>&1
    "C:\Users\irene\AppData\Local\Programs\Git\cmd\git.exe" commit -m "Backup aktualizacja Banku Tematow [skip ci]" >> "%~dp0cron_last_run.log" 2>&1
    "C:\Users\irene\AppData\Local\Programs\Git\cmd\git.exe" push origin main >> "%~dp0cron_last_run.log" 2>&1
)
echo [CRON FINISH] %DATE% %TIME% >> "%~dp0cron_last_run.log"
