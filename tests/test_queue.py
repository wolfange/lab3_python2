from __future__ import annotations

from collections.abc import Iterator

import pytest

from lab3.queue import TaskQueue, TaskQueueIterator
from lab3.task import Task


def _sample_queue() -> TaskQueue:
    return TaskQueue(
        [
            Task(id="T-1", priority=1, status="new"),
            Task(id="T-2", priority=5, status="in_progress"),
            Task(id="T-3", priority=3, status="done"),
            Task(id="T-4", priority=4, status="new"),
        ]
    )


class TestTaskQueueBasics:
    def test_enqueue_and_len(self) -> None:
        queue = TaskQueue()
        queue.enqueue(Task(id="N-1"))
        queue.enqueue(Task(id="N-2"))
        assert len(queue) == 2
        assert bool(queue) is True

    def test_dequeue_fifo(self) -> None:
        queue = TaskQueue([Task(id="A"), Task(id="B")])
        first = queue.dequeue()
        second = queue.dequeue()
        assert first.id == "A"
        assert second.id == "B"
        assert len(queue) == 0

    def test_dequeue_empty_raises(self) -> None:
        queue = TaskQueue()
        with pytest.raises(IndexError, match="пуста"):
            queue.dequeue()


class TestIterationProtocol:
    def test_iter_returns_iterator(self) -> None:
        queue = _sample_queue()
        iterator = iter(queue)
        assert isinstance(iterator, TaskQueueIterator)

    def test_repeatable_iteration(self) -> None:
        queue = _sample_queue()
        first_pass = [task.id for task in queue]
        second_pass = [task.id for task in queue]
        assert first_pass == ["T-1", "T-2", "T-3", "T-4"]
        assert second_pass == first_pass

    def test_stop_iteration_is_raised(self) -> None:
        queue = TaskQueue([Task(id="S-1")])
        iterator = iter(queue)
        assert next(iterator).id == "S-1"
        with pytest.raises(StopIteration):
            next(iterator)


class TestLazyFilters:
    def test_filter_by_status_is_lazy_iterator(self) -> None:
        queue = _sample_queue()
        stream = queue.iter_by_status("new")
        assert isinstance(stream, Iterator)
        assert [task.id for task in stream] == ["T-1", "T-4"]

    def test_filter_by_priority_range(self) -> None:
        queue = _sample_queue()
        ids = [task.id for task in queue.iter_by_priority(min_priority=4, max_priority=5)]
        assert ids == ["T-2", "T-4"]

    def test_invalid_priority_range_raises(self) -> None:
        queue = _sample_queue()
        with pytest.raises(ValueError, match="min_priority"):
            list(queue.iter_by_priority(min_priority=5, max_priority=3))

    def test_iter_where_with_large_generator(self) -> None:
        def source() -> Iterator[Task]:
            for i in range(10_000):
                status = "done" if i % 2 == 0 else "new"
                yield Task(id=f"L-{i}", priority=(i % 5) + 1, status=status)

        queue = TaskQueue(source())
        done_count = sum(1 for _ in queue.iter_by_status("done"))
        assert done_count == 5_000


class TestPythonCompatibility:
    def test_works_with_list_and_sum(self) -> None:
        queue = _sample_queue()
        items = list(queue)
        assert len(items) == 4
        assert sum(task.priority for task in queue) == 13
