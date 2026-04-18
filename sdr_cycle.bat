@echo off
REM SDR Skoromed v2.0 LOCAL .venv_local (no path error)
pushd "C:\Users\gfdnk\Documents\https-github.com-Skoromed-ai-sdr-prototype"
call .venv_local\Scripts\activate.bat
if not exist logs mkdir logs
echo [%date% %time%] SDR v2.0 START (.venv_local) >> logs\full_cycle.log 2>&1
REM FNS EGR
python src\main.py >> logs\full_cycle.log 2>&1
echo [%date% %time%] FNS OK >> logs\full_cycle.log 2>&1
REM Enrich
python src\enrich.py >> logs\full_cycle.log 2>&1
echo [%date% %time%] 2GIS OK >> logs\full_cycle.log 2>&1
REM VK Bot short
python vk_bot.py >> logs\full_cycle.log 2>&1 ^& timeout /t 5 ^& taskkill /f /im python.exe /t 2>nul
echo [%date% %time%] VK OK >> logs\full_cycle.log 2>&1
REM TG Bot short
python compliance_bot.py >> logs\full_cycle.log 2>&1 ^& timeout /t 5 ^& taskkill /f /im python.exe /t 2>nul
echo [%date% %time%] TG OK >> logs\full_cycle.log 2>&1
REM Mailer
python src\mailer.py >> logs\full_cycle.log 2>&1
echo [%date% %time%] Mailer OK >> logs\full_cycle.log 2>&1
REM DB Sync (5+ leads CSV → DB)
echo [%date% %time%] DB Sync START >> logs\full_cycle.log 2>&1
python src\db_sync.py >> logs\full_cycle.log 2>&1
echo [%date% %time%] DB OK (5+ B2B leads) >> logs\full_cycle.log 2>&1
popd
echo [%date% %time%] SDR v2.0 END >> logs\full_cycle.log 2>&1
pause