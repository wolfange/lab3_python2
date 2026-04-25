from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

_ALLOWED_STATUSES = {"new", "in_progress", "blocked", "done"}


@dataclass(slots=True)
class Task:
    """Задача с минимальным набором полей для работы очереди."""

    id: str
    priority: int = 3
    status: str = "new"
    payload: Any = field(default=None)

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("task id должен быть непустой строкой")
        if not isinstance(self.priority, int) or not 1 <= self.priority <= 5:
            raise ValueError("priority должен быть целым числом в диапазоне 1..5")
        if self.status not in _ALLOWED_STATUSES:
            raise ValueError(
                "status должен быть одним из: new, in_progress, blocked, done"
            )
