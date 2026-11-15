"""Кэш на диске: один JSON-файл."""

import json
from pathlib import Path
from typing import Any, Optional

from cache.icache import ICache


class DiskCache(ICache):
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def _load(self) -> dict[str, Any]:
        if not self._path.exists():
            return {}
        return json.loads(self._path.read_text(encoding="utf-8"))

    def _save(self, store: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(store, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get(self, key: str) -> Optional[Any]:
        return self._load().get(key)

    def set(self, key: str, value: Any) -> None:
        if value is None:
            raise ValueError("None нельзя сохранить: это признак промаха")
        store = self._load()
        store[key] = value
        self._save(store)

    def remove(self, key: str) -> None:
        store = self._load()
        store.pop(key, None)
        self._save(store)
