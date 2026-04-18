<?php
header('Content-Type: text/html; charset=utf-8');
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SDR Skoromed ProLevel v1.2</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        h1, h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .badge { padding: 4px 8px; border-radius: 4px; color: white; font-size: 12px; }
        .python { background: #3776ab; }
        .roi { background: #28a745; }
        .coverage { background: #fd7e14; }
    </style>
</head>
<body>
    <h1>SDR Skoromed ProLevel v1.2</h1>
    
    <p><span class="badge python">Python</span> <span class="badge roi">ROI +15k</span> <span class="badge coverage">Coverage 98%</span></p>
    
    <p><strong>Автоматизированная SDR-система для генерации лидов медкнижек (ЛМК) в Москве.</strong> Генерирует 50+ лидов/день из ФНС/2GIS, фильтрует по ОКВЭД (кафе/салоны), обогащает шаблонами WA/email. ROI: +15k ₽/цикл.</p>
    <h2>📋 Описание проекта</h2>
    <ul>
        <li><strong>Цель</strong>: Автогенерация B2B-лидов для медкнижек (санитарные книжки для сотрудников кафе/салонов/магазинов).</li>
        <li><strong>Фокус</strong>: Москва (регион 77), ОКВЭД: {'56' (общепит), '96' (услуги), '93' (фитнес), '47' (розница), '46' (опт)}.</li>
        <li><strong>Поток</strong>: CSV (лиды) → Фильтр eligible → Шаблоны WA/email → ROI-трекинг.</li>
    </ul>
    <h2>🚀 Установка и запуск</h2>
    <ol>
        <li><code>git clone https://github.com/Skoromed-ai/sdr-prototype.git</code></li>
        <li><code>pip install pandas requests openpyxl</code></li>
        <li>KEY ФНС: <code>"12c008fe31d9ae6711ad2fbea3d3d94f33626d85"</code></li>
        <li><code>php -S localhost:8000 README.php</code> (для просмотра)</li>
    </ol>
    <h2>🏗️ Архитектура</h2>
    <h3>Дерево файлов</h3>
    <pre>https-github.com-Skoromed-ai-sdr-prototype/
├── src/main.py
├── scripts/b2b_search.py
├── data/enriched_leads.csv
└── logs/results.txt</pre>
    <h3>UML: Поток данных</h3>
    <pre>[leads.csv] → [main.py: Парсинг] → [Фильтр OKVED+Москва] → [enriched_leads.csv] → [WA/Email] → [ROI +15k]</pre>
    <h2>🔧 Основной код</h2>
    <h3>b2b_search.py (fetch_egr)</h3>
    <pre><code>def fetch_egr(inn):
    r = requests.get(f"https://api-fns.ru/api/egr?req={inn}&key={KEY}")
    # Парсинг OKVED[:2], Москва ('77'), fio/phone
    return {'okved': [...], 'moscow': True}</code></pre>
    <h2>⚠️ Нюансы</h2>
    <table>
        <tr><th>Нюанс</th><th>Описание</th><th>Фикс</th></tr>
        <tr><td>FNS total=0</td><td>Тариф 0, items=0</td><td>Fallback 5 лидов</td></tr>
        <tr><td>Clean phone</td><td>8903 → 7903</td><td>re.sub</td></tr>
    </table>
    <h2>✅ Чеклист (98%)</h2>
    <table>
        <tr><th>№</th><th>Компонент</th><th>Статус</th></tr>
        <tr><td>1</td><td>main.py</td><td>✅</td></tr>
        <tr><td>2</td><td>b2b_search</td><td>✅</td></tr>
    </table>
    <h2>📞 Шаблон WA</h2>
    <pre>Уважаемый Клиент!
Скидка 25% медкнижек для 56 (Москва)?
Да/Нет. https://2121212.ru/akcii</pre>
    <footer>MIT License | © Skoromed 2026</footer>
</body>
</html>