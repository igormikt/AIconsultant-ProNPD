from openai import AsyncOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE, SYSTEM_PROMPT_FILE
from utils.logger import logger

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

_system_prompt_cache = None

def load_system_prompt() -> str:
    global _system_prompt_cache

    if _system_prompt_cache is None:
        try:
            with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
                _system_prompt_cache = f.read()
            logger.info("System prompt loaded")
        except FileNotFoundError:
            logger.error(f"System prompt file not found: {SYSTEM_PROMPT_FILE}")
            raise

    return _system_prompt_cache

async def ask_openai(question: str, context: str) -> str:
    try:
        system_prompt = load_system_prompt()

        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": f"Контекст:\n\n{context}"},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content
        logger.info(f"OpenAI response generated, tokens: {response.usage.total_tokens}")

        return answer

    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}", exc_info=True)
        raise Exception(f"Ошибка при обращении к OpenAI API: {str(e)}")
