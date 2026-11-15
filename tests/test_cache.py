from pathlib import Path

import pytest

from cache.cache_manager import CacheManager
from cache.disk_cache import DiskCache
from cache.maintenance import warmup
from cache.distributed_cache import DistributedCache
from cache.memory_cache import MemoryCache
from cache.redis_cache import RedisCache


def test_memory_set_get_remove() -> None:
    cache = MemoryCache()
    cache.set("a", "1")
    assert cache.get("a") == "1"
    cache.remove("a")
    assert cache.get("a") is None


def test_disk_roundtrip(tmp_path: Path) -> None:
    cache = DiskCache(str(tmp_path / "cache.json"))
    cache.set("city", "Казань")
    again = DiskCache(str(tmp_path / "cache.json"))
    assert again.get("city") == "Казань"
    again.remove("city")
    assert again.get("city") is None


def test_redis_emulator() -> None:
    cache = RedisCache("localhost", 6379)
    cache.set("token", "abc")
    assert cache.get("token") == "abc"
    cache.remove("token")
    assert cache.get("token") is None


def test_manager_falls_through_to_second_level(tmp_path: Path) -> None:
    memory = MemoryCache()
    disk = DiskCache(str(tmp_path / "cache.json"))
    disk.set("order:5", "cached-on-disk")
    manager = CacheManager([memory, disk])

    assert manager.get("order:5") == "cached-on-disk"
    assert memory.get("order:5") == "cached-on-disk"


def test_manager_writes_through_all_levels(tmp_path: Path) -> None:
    memory = MemoryCache()
    disk = DiskCache(str(tmp_path / "cache.json"))
    manager = CacheManager([memory, disk])
    manager.set("user:1", "Анна")

    assert memory.get("user:1") == "Анна"
    assert disk.get("user:1") == "Анна"
    manager.remove("user:1")
    assert memory.get("user:1") is None
    assert disk.get("user:1") is None


def test_distributed_cache_plugs_in_without_manager_changes() -> None:
    distributed = DistributedCache(shards=4)
    manager = CacheManager([MemoryCache(), distributed])
    manager.set("session", "abc")
    assert manager.get("session") == "abc"
    assert distributed.get("session") == "abc"


def test_none_is_rejected() -> None:
    with pytest.raises(ValueError):
        MemoryCache().set("a", None)


def test_warmup_fills_every_level(tmp_path: Path) -> None:
    memory = MemoryCache()
    disk = DiskCache(str(tmp_path / "cache.json"))
    manager = CacheManager([memory, disk])
    stored = warmup(manager, {"city": "Казань", "lang": "ru"})
    assert stored == 2
    assert memory.get("city") == "Казань"
    assert disk.get("lang") == "ru"
