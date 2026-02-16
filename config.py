import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# API ключи
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Модели OpenAI
OPENAI_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

# Параметры RAG
TOP_K = 2
MAX_CONTEXT_TOKENS = 2000

# Параметры rate limiting
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60

# Температура генерации
TEMPERATURE = 0.2

# Пути к файлам
BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge" / "knowledge.json"
EMBEDDINGS_FILE = BASE_DIR / "knowledge" / "embeddings.json"
SYSTEM_PROMPT_FILE = BASE_DIR / "prompts" / "system_prompt.txt"
LOG_FILE = BASE_DIR / "bot.log"


def validate_config():
    """Проверка конфигурации"""
    errors = []

    if not TELEGRAM_TOKEN:
        errors.append("TELEGRAM_TOKEN не установлен")
    if not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY не установлен")

    if not KNOWLEDGE_FILE.exists():
        errors.append(f"Файл базы знаний не найден: {KNOWLEDGE_FILE}")
    if not EMBEDDINGS_FILE.exists():
        errors.append(f"Файл embeddings не найден: {EMBEDDINGS_FILE}")
    if not SYSTEM_PROMPT_FILE.exists():
        errors.append(f"Файл системного промпта не найден: {SYSTEM_PROMPT_FILE}")

    if errors:
        raise ValueError("Ошибки конфигурации:\n" + "\n".join(f"- {e}" for e in errors))

    return True
