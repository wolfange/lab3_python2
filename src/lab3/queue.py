from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator

from lab3.task import Task


class TaskQueueIterator(Iterator[Task]):
    """Итератор по снимку списка задач."""

    def __init__(self, tasks: list[Task]) -> None:
        self._tasks = tasks
        self._index = 0

    def __iter__(self) -> TaskQueueIterator:
        return self

    def __next__(self) -> Task:
        if self._index >= len(self._tasks):
            raise StopIteration
        task = self._tasks[self._index]
        self._index += 1
        return task


class TaskQueue(Iterable[Task]):
    """Очередь задач с поддержкой повторного обхода и ленивых операций."""

    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        self._tasks: list[Task] = []
        if tasks is not None:
            self.extend(tasks)

    def enqueue(self, task: Task) -> None:
        """Добавить задачу в конец очереди."""
        self._tasks.append(task)

    def dequeue(self) -> Task:
        """Извлечь задачу из начала очереди."""
        if not self._tasks:
            raise IndexError("очередь пуста")
        return self._tasks.pop(0)

    def extend(self, tasks: Iterable[Task]) -> None:
        """Добавить в очередь задачи из любого итерируемого источника."""
        for task in tasks:
            self.enqueue(task)

    def __iter__(self) -> TaskQueueIterator:
        return TaskQueueIterator(self._tasks)

    def __len__(self) -> int:
        return len(self._tasks)

    def __bool__(self) -> bool:
        return bool(self._tasks)

    def iter_where(self, predicate: Callable[[Task], bool]) -> Iterator[Task]:
        """Лениво вернуть задачи, удовлетворяющие условию."""
        return (task for task in self if predicate(task))

    def iter_by_status(self, status: str) -> Iterator[Task]:
        """Лениво вернуть задачи с указанным статусом."""
        return self.iter_where(lambda task: task.status == status)

    def iter_by_priority(
        self,
        *,
        min_priority: int = 1,
        max_priority: int = 5,
    ) -> Iterator[Task]:
        """Лениво вернуть задачи по диапазону приоритета."""
        if min_priority > max_priority:
            raise ValueError("min_priority не может быть больше max_priority")
        return self.iter_where(
            lambda task: min_priority <= task.priority <= max_priority
        )

    def __repr__(self) -> str:
        return f"TaskQueue(size={len(self)})"
