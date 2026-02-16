from utils.logger import logger

def keyword_filter(query: str, knowledge: list, min_matches: int = 1) -> list:
    query_lower = query.lower()
    filtered = []

    for item in knowledge:
        matches = 0
        keywords = item.get("keywords", [])

        for kw in keywords:
            if kw.lower() in query_lower:
                matches += 1

        if matches >= min_matches:
            filtered.append(item)

    if filtered:
        logger.info(f"Keyword filter: {len(filtered)} articles matched")
        return filtered
    else:
        logger.info("Keyword filter: no matches")
        return []
