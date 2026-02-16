import json
import numpy as np
from config import TOP_K, KNOWLEDGE_FILE, EMBEDDINGS_FILE
from services.embedding_service import get_embedding
from services.keyword_service import keyword_filter
from services.openai_service import ask_openai
from utils.token_control import trim_context_by_tokens
from utils.logger import logger

_knowledge_cache = None
_embeddings_cache = None

async def initialize_knowledge_base():
    global _knowledge_cache, _embeddings_cache

    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            _knowledge_cache = json.load(f)
        logger.info(f"Loaded {len(_knowledge_cache)} articles")

        with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
            _embeddings_cache = json.load(f)
        logger.info(f"Loaded {len(_embeddings_cache)} embeddings")

        _embeddings_cache = {item["id"]: item["embedding"] for item in _embeddings_cache}

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {e}")
        raise

def cosine_similarity(a: list, b: list) -> float:
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

async def generate_answer(user_question: str) -> str:
    try:
        filtered_articles = keyword_filter(user_question, _knowledge_cache)

        if not filtered_articles:
            logger.info("No keyword matches, using full knowledge base")
            filtered_articles = _knowledge_cache

        query_embedding = await get_embedding(user_question)

        similarities = []
        for article in filtered_articles:
            article_id = article["id"]
            if article_id in _embeddings_cache:
                embedding = _embeddings_cache[article_id]
                sim = cosine_similarity(query_embedding, embedding)
                similarities.append((sim, article["content"], article.get("laws", [])))

        similarities.sort(reverse=True, key=lambda x: x[0])
        top_articles = similarities[:TOP_K]

        logger.info(f"Selected {len(top_articles)} most relevant articles")

        context_parts = []
        for i, (score, content, laws) in enumerate(top_articles, 1):
            laws_text = f" (Законы: {', '.join(laws)})" if laws else ""
            context_parts.append(f"[Статья {i}]{laws_text}\n{content}")

        context = "\n\n---\n\n".join(context_parts)
        context = trim_context_by_tokens(context)

        answer = await ask_openai(user_question, context)

        return answer

    except Exception as e:
        logger.error(f"Error generating answer: {e}", exc_info=True)
        return "Извините, произошла ошибка при генерации ответа."
