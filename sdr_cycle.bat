@echo off
cd /d "C:\Users\gfdnk\Documents\https-github.com-Skoromed-ai-sdr-prototype"
echo [%date% %time%] SDR Cycle start >> logs\full_cycle.log
python scripts\b2b_search.py >> logs\full_cycle.log 2>&1
python src\main.py >> logs\full_cycle.log 2>&1
echo [%date% %time%] SDR Cycle end (ROI check) >> logs\full_cycle.log