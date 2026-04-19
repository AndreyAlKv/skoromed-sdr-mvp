chcp 65001 >nul
taskkill /f /im notepad.exe >nul 2>nul
call .venv_local\Scripts\activate.bat
echo SDR v2.2.7 START
python src\main.py
python src\enrich.py
python src\mailer.py
python src\db_sync.py
python src\db_query.py
python src\export_results.py
echo SDR END OK - CSV: data/archives/results_export.csv (165+ leads)
pause