chcp 65001 >nul
taskkill /f /im notepad.exe >nul 2>nul
call .venv_local\Scripts\activate.bat
echo SDR v2.2.6 START
python src\main.py
python src\enrich.py
python src\mailer.py
python src\db_sync.py
python src\db_query.py
echo SDR END OK
pause