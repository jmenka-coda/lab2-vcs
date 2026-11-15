"""Кэш в оперативной памяти."""

from typing import Any, Optional

from cache.icache import ICache


class MemoryCache(ICache):
    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        if value is None:
            raise ValueError("None нельзя сохранить: это признак промаха")
        self._store[key] = value

    def remove(self, key: str) -> None:
        self._store.pop(key, None)
