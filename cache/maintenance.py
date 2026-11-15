"""Прогрев кэша заранее известными данными."""

from typing import Any

from cache.cache_manager import CacheManager


def warmup(manager: CacheManager, items: dict[str, Any]) -> int:
    """Кладёт пары ключ-значение во все уровни и возвращает число записей."""
    count = 0
    for key, value in items.items():
        manager.set(key, value)
        count += 1
    return count
