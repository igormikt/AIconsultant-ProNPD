from openai import AsyncOpenAI
from config import OPENAI_API_KEY, EMBEDDING_MODEL
from utils.logger import logger

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_embedding(text: str) -> list:
    try:
        response = await client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text[:8000]
        )
        logger.debug(f"Embedding generated for text length: {len(text)}")
        return response.data[0].embedding

    except Exception as e:
        logger.error(f"Error getting embedding: {e}", exc_info=True)
        raise Exception(f"Не удалось получить embedding: {str(e)}")
