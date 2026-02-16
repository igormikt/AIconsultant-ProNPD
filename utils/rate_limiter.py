from collections import defaultdict
from datetime import datetime, timedelta
from config import RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW


class RateLimiter:
    def __init__(self):
        self.user_requests = defaultdict(list)

    def check_limit(self, user_id: int) -> bool:
        """
        Проверяет, не превысил ли пользователь лимит запросов

        Returns:
            True - запрос разрешен
            False - превышен лимит
        """
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=RATE_LIMIT_WINDOW)

        # Удаляем старые запросы
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id]
            if req_time > cutoff_time
        ]

        # Проверяем лимит
        if len(self.user_requests[user_id]) >= RATE_LIMIT_REQUESTS:
            return False

        # Добавляем текущий запрос
        self.user_requests[user_id].append(now)
        return True


# Глобальный экземпляр
rate_limiter = RateLimiter()
