import json
from pathlib import Path
from datetime import datetime

# Путь к файлу логов
LOG_FILE = Path(__file__).parent / "logs" / "bot.log"


def analyze_bot_statistics():
    """Анализирует статистику работы бота"""

    if not LOG_FILE.exists():
        print("❌ Файл логов не найден!")
        print(f"Ожидается: {LOG_FILE}")
        return

    print("📊 СТАТИСТИКА РАБОТЫ БОТА")
    print("=" * 50)

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        logs = f.readlines()

    # Подсчёт ответов
    faq_answers = len([l for l in logs if 'FAQ answer provided' in l])
    rag_answers = len([l for l in logs if 'RAG answer successfully' in l])
    errors = len([l for l in logs if 'ERROR' in l])

    # Подсчёт уникальных пользователей
    users = set()
    for line in logs:
        if 'User' in line and 'asked:' in line:
            try:
                user_id = line.split('User ')[1].split(' ')[0]
                users.add(user_id)
            except:
                pass

    # Расчёт экономии
    faq_tokens_saved = faq_answers * 500  # Примерно 500 токенов на запрос
    cost_saved = faq_tokens_saved * 0.00001  # GPT-4 примерно $0.01 за 1000 токенов

    print(f"\n📈 Ответы:")
    print(f"  ✅ FAQ ответов (без токенов):     {faq_answers}")
    print(f"  🤖 RAG ответов (с GPT):           {rag_answers}")
    print(f"  ❌ Ошибок:                         {errors}")
    print(f"  👥 Уникальных пользователей:       {len(users)}")

    print(f"\n💰 Экономия:")
    print(f"  Сэкономлено токенов:  ~{faq_tokens_saved:,}")
    print(f"  Экономия в деньгах:   ~${cost_saved:.4f}")

    total = faq_answers + rag_answers
    if total > 0:
        faq_percent = (faq_answers / total) * 100
        print(f"\n🎯 Эффективность FAQ: {faq_percent:.1f}%")

    print("\n" + "=" * 50)
    print(f"📅 Дата анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Файл логов: {LOG_FILE}")
    print(f"📏 Всего строк в логе: {len(logs)}")


if __name__ == "__main__":
    analyze_bot_statistics()
