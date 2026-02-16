import aiosqlite
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "bot_data.db"


async def init_database():
    """Инициализация базы данных"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица пользователей
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP,
                total_questions INTEGER DEFAULT 0,
                total_tokens_used INTEGER DEFAULT 0
            )
        """)

        # Таблица вопросов
        await db.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question TEXT NOT NULL,
                answer TEXT,
                answer_type TEXT,
                tokens_used INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Таблица дневной статистики
        await db.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT (date('now')),
                total_questions INTEGER DEFAULT 0,
                faq_answers INTEGER DEFAULT 0,
                rag_answers INTEGER DEFAULT 0,
                unique_users INTEGER DEFAULT 0,
                tokens_used INTEGER DEFAULT 0
            )
        """)

        await db.commit()


async def save_user(user_id, username, first_name, last_name):
    """Сохранение или обновление пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, registered_at, last_active, total_questions)
            VALUES (?, ?, ?, ?, ?, ?, 0)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                last_active = excluded.last_active
        """, (user_id, username, first_name, last_name, datetime.now(), datetime.now()))
        await db.commit()


async def save_question(user_id, question, answer, answer_type, tokens_used=0):
    """Сохранение вопроса и ответа"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Сохранить вопрос
        await db.execute("""
            INSERT INTO questions 
            (user_id, question, answer, answer_type, tokens_used)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, question, answer, answer_type, tokens_used))

        # Обновить счётчики пользователя
        await db.execute("""
            UPDATE users 
            SET total_questions = total_questions + 1,
                total_tokens_used = total_tokens_used + ?,
                last_active = ?
            WHERE user_id = ?
        """, (tokens_used, datetime.now(), user_id))

        await db.commit()


async def get_user_stats(user_id):
    """Получить статистику пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT 
                u.total_questions,
                u.total_tokens_used,
                u.registered_at,
                u.last_active,
                COUNT(q.id) as questions_count,
                SUM(CASE WHEN q.answer_type = 'faq' THEN 1 ELSE 0 END) as faq_count,
                SUM(CASE WHEN q.answer_type = 'rag' THEN 1 ELSE 0 END) as rag_count
            FROM users u
            LEFT JOIN questions q ON u.user_id = q.user_id
            WHERE u.user_id = ?
            GROUP BY u.user_id
        """, (user_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_total_stats():
    """Получить общую статистику бота"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT 
                COUNT(DISTINCT user_id) as total_users,
                COUNT(*) as total_questions,
                SUM(CASE WHEN answer_type = 'faq' THEN 1 ELSE 0 END) as faq_count,
                SUM(CASE WHEN answer_type = 'rag' THEN 1 ELSE 0 END) as rag_count,
                SUM(tokens_used) as total_tokens
            FROM questions
        """) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_recent_questions(user_id, limit=5):
    """Получить последние вопросы пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT question, answer, answer_type, tokens_used, created_at
            FROM questions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
