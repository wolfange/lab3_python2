from __future__ import annotations

import pytest

from lab3.task import Task


class TestTaskValidation:
    def test_valid_task(self) -> None:
        task = Task(id="A-1", priority=2, status="new")
        assert task.id == "A-1"
        assert task.priority == 2
        assert task.status == "new"

    def test_empty_id_raises(self) -> None:
        with pytest.raises(ValueError, match="id"):
            Task(id=" ")

    def test_invalid_priority_raises(self) -> None:
        with pytest.raises(ValueError, match="priority"):
            Task(id="A-2", priority=8)

    def test_invalid_status_raises(self) -> None:
        with pytest.raises(ValueError, match="status"):
            Task(id="A-3", status="waiting")
