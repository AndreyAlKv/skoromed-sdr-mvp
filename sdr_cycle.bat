chcp 65001 >nul
call .venv_local\Scripts\activate.bat
python src\main.py
python src\enrich.py
python src\db_sync.py
python src\db_query.py
pause