import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "bot_data.db"


def view_database():
    """Просмотр содержимого базы данных"""

    if not DB_PATH.exists():
        print("❌ База данных не найдена!")
        print(f"Ожидается: {DB_PATH}")
        print("\n💡 Сначала запустите бота, чтобы создать БД")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n" + "=" * 70)
    print("📊 ПРОСМОТР БАЗЫ ДАННЫХ БОТА")
    print("=" * 70)

    # 1. Статистика пользователей
    print("\n👥 ПОЛЬЗОВАТЕЛИ:")
    print("-" * 70)
    cursor.execute("""
        SELECT 
            user_id, 
            username, 
            first_name, 
            last_name, 
            total_questions, 
            total_tokens_used,
            registered_at,
            last_active
        FROM users 
        ORDER BY total_questions DESC
    """)

    users = cursor.fetchall()
    if users:
        print(f"{'ID':<12} {'Username':<15} {'Имя':<15} {'Вопросов':<10} {'Токенов':<10} {'Зарегистрирован'}")
        print("-" * 70)
        for user in users:
            user_id, username, first_name, last_name, questions, tokens, reg_at, last_act = user
            name = f"{first_name or ''} {last_name or ''}".strip() or "Без имени"
            username_display = username or "—"
            reg_date = reg_at.split()[0] if reg_at else "—"
            print(f"{user_id:<12} {username_display:<15} {name:<15} {questions:<10} {tokens:<10} {reg_date}")
    else:
        print("Пользователей пока нет")

    # 2. Последние вопросы
    print("\n\n💬 ПОСЛЕДНИЕ 10 ВОПРОСОВ:")
    print("-" * 70)
    cursor.execute("""
        SELECT 
            q.id,
            q.user_id,
            u.username,
            q.question,
            q.answer_type,
            q.tokens_used,
            q.created_at
        FROM questions q
        LEFT JOIN users u ON q.user_id = u.user_id
        ORDER BY q.created_at DESC
        LIMIT 10
    """)

    questions = cursor.fetchall()
    if questions:
        for i, q in enumerate(questions, 1):
            q_id, user_id, username, question, answer_type, tokens, created = q
            username_display = username or f"User_{user_id}"
            question_short = question[:60] + "..." if len(question) > 60 else question
            created_time = created.split('.')[0] if created else "—"

            print(f"\n{i}. [{answer_type.upper()}] от @{username_display}")
            print(f"   Вопрос: {question_short}")
            print(f"   Токены: {tokens} | Время: {created_time}")
    else:
        print("Вопросов пока нет")

    # 3. Общая статистика
    print("\n\n📈 ОБЩАЯ СТАТИСТИКА:")
    print("-" * 70)
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT user_id) as total_users,
            COUNT(*) as total_questions,
            SUM(CASE WHEN answer_type = 'faq' THEN 1 ELSE 0 END) as faq_count,
            SUM(CASE WHEN answer_type = 'rag' THEN 1 ELSE 0 END) as rag_count,
            SUM(CASE WHEN answer_type = 'error' THEN 1 ELSE 0 END) as error_count,
            SUM(tokens_used) as total_tokens
        FROM questions
    """)

    stats = cursor.fetchone()
    if stats:
        total_users, total_q, faq, rag, errors, tokens = stats
        total_answered = faq + rag
        faq_percent = (faq / total_answered * 100) if total_answered > 0 else 0

        print(f"Всего пользователей:     {total_users or 0}")
        print(f"Всего вопросов:          {total_q or 0}")
        print(f"  ├─ FAQ ответов:        {faq or 0} ({faq_percent:.1f}%)")
        print(f"  ├─ RAG ответов:        {rag or 0}")
        print(f"  └─ Ошибок:             {errors or 0}")
        print(f"Всего токенов:           {tokens or 0:,}")

        # Расчёт стоимости
        cost = (tokens or 0) * 0.00001  # Примерная стоимость GPT-4
        savings = (faq or 0) * 500 * 0.00001  # Сэкономлено на FAQ
        print(f"Потрачено (~):           ${cost:.4f}")
        print(f"Сэкономлено на FAQ (~):  ${savings:.4f}")

    # 4. Топ активных пользователей
    print("\n\n🏆 ТОП-5 АКТИВНЫХ ПОЛЬЗОВАТЕЛЕЙ:")
    print("-" * 70)
    cursor.execute("""
        SELECT 
            u.username,
            u.first_name,
            u.total_questions,
            u.total_tokens_used
        FROM users u
        ORDER BY u.total_questions DESC
        LIMIT 5
    """)

    top_users = cursor.fetchall()
    if top_users:
        for i, (username, first_name, questions, tokens) in enumerate(top_users, 1):
            display_name = username or first_name or "Пользователь"
            print(f"{i}. @{display_name}: {questions} вопросов, {tokens} токенов")
    else:
        print("Данных пока нет")

    # 5. Распределение по типам ответов (последние 7 дней)
    print("\n\n📅 АКТИВНОСТЬ ЗА ПОСЛЕДНИЕ 7 ДНЕЙ:")
    print("-" * 70)
    cursor.execute("""
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as total,
            SUM(CASE WHEN answer_type = 'faq' THEN 1 ELSE 0 END) as faq,
            SUM(CASE WHEN answer_type = 'rag' THEN 1 ELSE 0 END) as rag
        FROM questions
        WHERE created_at >= datetime('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date DESC
    """)

    daily = cursor.fetchall()
    if daily:
        print(f"{'Дата':<12} {'Всего':<8} {'FAQ':<8} {'RAG':<8}")
        print("-" * 70)
        for date, total, faq, rag in daily:
            print(f"{date:<12} {total:<8} {faq:<8} {rag:<8}")
    else:
        print("Данных за последние 7 дней нет")

    conn.close()

    print("\n" + "=" * 70)
    print(f"📁 Файл БД: {DB_PATH}")
    print(f"📅 Дата просмотра: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    view_database()
