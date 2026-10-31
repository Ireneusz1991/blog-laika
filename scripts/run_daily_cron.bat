@echo off
cd /d "%~dp0.."
echo ======================================================== >> "%~dp0cron_last_run.log"
echo [CRON START] %DATE% %TIME% >> "%~dp0cron_last_run.log"
echo ======================================================== >> "%~dp0cron_last_run.log"
"C:\Users\irene\AppData\Local\Programs\Python\Python312\python.exe" "scripts\daily_editorial_cron.py" --deploy >> "%~dp0cron_last_run.log" 2>&1
echo [CRON FINISH] %DATE% %TIME% >> "%~dp0cron_last_run.log"
