from __future__ import annotations

from lab3.queue import TaskQueue
from lab3.task import Task


def _build_demo_queue() -> TaskQueue:
    return TaskQueue(
        [
            Task(id="T-1", priority=2, status="new", payload={"kind": "email"}),
            Task(id="T-2", priority=5, status="in_progress", payload={"kind": "etl"}),
            Task(id="T-3", priority=1, status="done", payload={"kind": "report"}),
            Task(id="T-4", priority=4, status="new", payload={"kind": "billing"}),
        ]
    )


def main() -> None:
    queue = _build_demo_queue()
    print("Лабораторная №3: очередь задач")
    print(f"Всего задач: {len(queue)}")

    print("Новые задачи:")
    for task in queue.iter_by_status("new"):
        print(f"- {task.id} (priority={task.priority})")

    high_priority_sum = sum(task.priority for task in queue.iter_by_priority(min_priority=4))
    print(f"Сумма приоритетов (>=4): {high_priority_sum}")


if __name__ == "__main__":
    main()
