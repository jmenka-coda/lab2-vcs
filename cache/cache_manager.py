"""Основной модуль. Знает только список ICache, не конкретные классы."""

from typing import Any, Optional

from cache.icache import ICache


class CacheManager:
    def __init__(self, caches: list[ICache]) -> None:
        if not caches:
            raise ValueError("Нужен хотя бы один кэш")
        self._caches = list(caches)

    def get(self, key: str) -> Optional[Any]:
        """Искать по уровням: если в первом нет, смотреть следующий."""
        for index, cache in enumerate(self._caches):
            value = cache.get(key)
            if value is None:
                continue
            for upper in self._caches[:index]:
                upper.set(key, value)
            return value
        return None

    def set(self, key: str, value: Any) -> None:
        for cache in self._caches:
            cache.set(key, value)

    def remove(self, key: str) -> None:
        for cache in self._caches:
            cache.remove(key)
