"""Распределённый кэш: ключ попадает в один из шардов.

Четвёртый узел сети. Подключается снаружи и не требует правок CacheManager.
"""

from typing import Any, Optional

from cache.icache import ICache


class DistributedCache(ICache):
    def __init__(self, shards: int = 4) -> None:
        if shards < 1:
            raise ValueError("Нужен хотя бы один шард")
        self._shards: list[dict[str, Any]] = [{} for _ in range(shards)]

    def _shard(self, key: str) -> dict[str, Any]:
        return self._shards[hash(key) % len(self._shards)]

    def get(self, key: str) -> Optional[Any]:
        return self._shard(key).get(key)

    def set(self, key: str, value: Any) -> None:
        if value is None:
            raise ValueError("None нельзя сохранить: это признак промаха")
        self._shard(key)[key] = value

    def remove(self, key: str) -> None:
        self._shard(key).pop(key, None)
