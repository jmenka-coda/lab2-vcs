"""Сборка сети кэшей. Конкретные узлы создаются здесь и передаются в CacheManager."""

from cache.cache_manager import CacheManager
from cache.disk_cache import DiskCache
from cache.distributed_cache import DistributedCache
from cache.memory_cache import MemoryCache
from cache.redis_cache import RedisCache
from logger import log


def main() -> None:
    memory = MemoryCache()
    disk = DiskCache("data/disk_cache.json")
    redis = RedisCache("localhost", 6379)

    manager = CacheManager([memory, disk, redis])
    manager.set("user:1", "Анна")
    log("info", "сквозное чтение: " + str(manager.get("user:1")))

    # Промах в первом уровне, попадание во втором.
    cold_memory = MemoryCache()
    warm_disk = DiskCache("data/disk_only.json")
    warm_disk.set("order:5", "cached-on-disk")
    cascade = CacheManager([cold_memory, warm_disk])
    log("info", "каскад: " + str(cascade.get("order:5")))
    log("info", "после подъёма в память: " + str(cold_memory.get("order:5")))

    log("info", "Добавляем DistributedCache без изменения CacheManager")
    extended = CacheManager(
        [
            MemoryCache(),
            DiskCache("data/disk_cache.json"),
            RedisCache(),
            DistributedCache(shards=4),
        ]
    )
    extended.set("session", "abc")
    log("info", "четыре уровня: " + str(extended.get("session")))


if __name__ == "__main__":
    main()
