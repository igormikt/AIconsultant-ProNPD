import json
import asyncio
from pathlib import Path
from openai import AsyncOpenAI
from config import OPENAI_API_KEY, EMBEDDING_MODEL, KNOWLEDGE_FILE, EMBEDDINGS_FILE

async def generate_embeddings():
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    print(f"Загрузка базы знаний из {KNOWLEDGE_FILE}...")
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        knowledge = json.load(f)

    print(f"Найдено статей: {len(knowledge)}")

    embeddings_data = []

    for i, article in enumerate(knowledge, 1):
        print(f"Обработка статьи {i}/{len(knowledge)}: ID={article['id']}")

        try:
            response = await client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=article["content"][:8000]
            )

            embedding = response.data[0].embedding

            embeddings_data.append({
                "id": article["id"],
                "embedding": embedding
            })

            print(f"  Embedding создан (размерность: {len(embedding)})")

        except Exception as e:
            print(f"  Ошибка: {e}")
            continue

    print(f"\nСохранение embeddings в {EMBEDDINGS_FILE}...")
    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(embeddings_data, f, ensure_ascii=False, indent=2)

    print(f"Готово! Создано {len(embeddings_data)} embeddings")

if __name__ == "__main__":
    asyncio.run(generate_embeddings())
