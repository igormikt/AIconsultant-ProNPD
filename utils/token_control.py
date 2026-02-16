import tiktoken
from config import MAX_CONTEXT_TOKENS


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Подсчитывает количество токенов в тексте"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        # Приблизительная оценка: 1 токен ≈ 4 символа
        return len(text) // 4


def truncate_text(text: str, max_tokens: int, model: str = "gpt-4") -> str:
    """Обрезает текст до указанного количества токенов"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(text)

        if len(tokens) <= max_tokens:
            return text

        truncated_tokens = tokens[:max_tokens]
        return encoding.decode(truncated_tokens)
    except Exception:
        # Приблизительная обрезка
        max_chars = max_tokens * 4
        return text[:max_chars]


def trim_context_by_tokens(articles: list, max_tokens: int = MAX_CONTEXT_TOKENS) -> str:
    """Ограничивает контекст указанным количеством токенов"""
    context = ""
    current_tokens = 0

    for article in articles:
        article_text = f"\n\n{article['topic']}: {article['content']}"
        article_tokens = count_tokens(article_text)

        if current_tokens + article_tokens <= max_tokens:
            context += article_text
            current_tokens += article_tokens
        else:
            # Добавляем частично, если есть место
            remaining_tokens = max_tokens - current_tokens
            if remaining_tokens > 100:
                truncated = truncate_text(article_text, remaining_tokens)
                context += truncated
            break

    return context
