# main.py - FULL SDR PROTOTYPE: scrape + enrich + LLM + mail preview
import json
import os
def run_full_pipeline():
    print("=== SDR MVP FULL RUN ===")
    # Step 1: Scrape (uncomment for fresh)
    # os.system("python src/scraper.py")
    
    # Step 2: Enrich contacts
    print("\n🔍 Running enrich...")
    os.system("python src/enrich.py")
    
    # Step 3: Load enriched + personalize
    with open('src/data/enriched_companies.json', 'r', encoding='utf-8') as f:
        enriched = json.load(f)
    
    leads_with_email = [c for c in enriched if c.get('emails')]
    print(f"\n✅ Found {len(leads_with_email)} LEADS WITH EMAILS!")
    
    for lead in leads_with_email:
        print(f"\n📧 EMAIL for {lead['name'][:50]}")
        print(f"TO: {lead['emails'][0]}")
        print(f"Phones: {lead['phones']}")
        print("\nLLM Prompt for GPT:")
        prompt = f"""
Напиши B2B холодное письмо на русском для "{lead['name']}" ({lead['url']}).
Предлагаем AI SDR: авто-лиды для медкнижек (scrape + emails + звонки).
Тема: AI для лидов медкнижек Москва +30%
От: info@skoromed.ai
CTA: ответ/звонок +7(999)123-45-67
        """
        print(prompt.strip())
        print("\nSIMULATED GPT:")
        print("Тема: AI SDR для ваших лидов медкнижек!")
        print("Добрый день! Вижу вы делаете медкнижки срочно.")
        print("Skoromed AI: +30% клиентов авто (scrape Yandex + emails).")
        print("Обсудим? +7(999)123-45-67 | info@skoromed.ai")
        print("--- READY TO MAIL ---\n")
if __name__ == "__main__":
    run_full_pipeline()
    print("\n🚀 SDR READY! Next: real OpenAI + SMTP mailer.py")