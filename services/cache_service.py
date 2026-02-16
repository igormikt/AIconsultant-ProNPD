from functools import lru_cache
import hashlib
from utils.logger import logger

# Простой кэш ответов (хранится в памяти)
_answer_cache = {}


def get_cache_key(question: str) -> str:
    """Создает ключ для кэша из вопроса"""
    # Нормализуем вопрос (убираем лишние пробелы, приводим к нижнему регистру)
    normalized = " ".join(question.lower().split())
    # Создаем хэш
    return hashlib.md5(normalized.encode()).hexdigest()


def get_cached_answer(question: str) -> str:
    """Получает ответ из кэша, если он есть"""
    key = get_cache_key(question)
    if key in _answer_cache:
        logger.info(f"Cache hit for question: {question[:50]}...")
        return _answer_cache[key]
    return None


def cache_answer(question: str, answer: str):
    """Сохраняет ответ в кэш"""
    key = get_cache_key(question)
    _answer_cache[key] = answer
    logger.info(f"Cached answer for question: {question[:50]}...")

    # Ограничиваем размер кэша (храним последние 100 ответов)
    if len(_answer_cache) > 100:
        # Удаляем самый старый элемент
        oldest_key = next(iter(_answer_cache))
        del _answer_cache[oldest_key]
        logger.info("Cache size limit reached, removed oldest entry")


def clear_cache():
    """Очищает кэш (для обновления базы знаний)"""
    global _answer_cache
    _answer_cache = {}
    logger.info("Cache cleared")
