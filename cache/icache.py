"""Абстракция узла сети кэшей."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class ICache(ABC):
    """Единый контракт хранилища. Основной модуль зависит только от него."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Вернуть значение или None, если ключа нет."""

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Сохранить значение по ключу."""

    @abstractmethod
    def remove(self, key: str) -> None:
        """Удалить ключ. Отсутствие ключа не считается ошибкой."""
