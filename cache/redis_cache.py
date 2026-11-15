"""Кэш с интерфейсом Redis.

Сервер Redis для лабораторной не требуется: данные лежат в словаре,
а адрес сохраняется, чтобы узел сети выглядел как внешнее хранилище.
"""

from typing import Any, Optional

from cache.icache import ICache


class RedisCache(ICache):
    def __init__(self, host: str = "localhost", port: int = 6379) -> None:
        self.host = host
        self.port = port
        self._store: dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        if value is None:
            raise ValueError("None нельзя сохранить: это признак промаха")
        self._store[key] = value

    def remove(self, key: str) -> None:
        self._store.pop(key, None)
