"""Простое логирование событий приложения."""

from datetime import datetime


def log(level: str, message: str) -> None:
    """Печатает строку вида [время] [LEVEL] сообщение."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")
