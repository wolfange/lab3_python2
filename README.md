# Лабораторная работа №3. Очередь задач: итераторы и генераторы

## Описание

Реализация пользовательской коллекции `TaskQueue` для платформы обработки задач. Очередь поддерживает протокол итерации, повторный обход, ленивую фильтрацию по статусу и приоритету, а также совместима со стандартными конструкциями Python (`for`, `list`, `sum`).

## Требования

- Python >= 3.10

## Установка

```bash
git clone https://github.com/wolfange/lab3_python2.git
cd lab3_python2

# Установка в режиме разработки
pip install -e .

# Зависимости для тестов и покрытия
pip install -e ".[dev]"
```

## Структура проекта

```text
lab3_python2/
├── src/lab3/
│   ├── __init__.py          # Экспорт публичного API
│   ├── task.py              # Модель задачи Task
│   ├── queue.py             # TaskQueue, TaskQueueIterator, ленивые фильтры
│   └── main.py              # Точка входа, демонстрация
├── tests/                   # Модульные тесты
├── pyproject.toml           # Конфигурация проекта и pytest/coverage
├── Dockerfile               # Сборка образа и прогон тестов в контейнере
├── .dockerignore
└── README.md                # Этот файл
```

## Основные компоненты

### 1. Модель задачи `Task`

`Task` реализован через `dataclass(slots=True)` и содержит поля:

- `id` — идентификатор задачи;
- `priority` — приоритет в диапазоне `1..5`;
- `status` — статус из множества `new`, `in_progress`, `blocked`, `done`;
- `payload` — произвольные данные задачи.

Проверка инвариантов выполняется в `__post_init__`, при нарушении выбрасывается `ValueError`.

### 2. Очередь `TaskQueue`

`TaskQueue` предоставляет:

- `enqueue(task)` — добавить задачу в конец очереди;
- `dequeue()` — извлечь задачу из начала (FIFO);
- `extend(tasks)` — добавить задачи из любого итерируемого источника;
- `__iter__()` — вернуть новый итератор для повторного обхода;
- `__len__()` и `__bool__()` — стандартная интеграция с Python.

### 3. Итератор `TaskQueueIterator`

Отдельный класс итератора с явной реализацией `__next__` и корректной обработкой `StopIteration`.

### 4. Ленивые генераторы

Для потоковой обработки реализованы методы:

- `iter_where(predicate)` — общий ленивый фильтр;
- `iter_by_status(status)` — фильтр по статусу;
- `iter_by_priority(min_priority, max_priority)` — фильтр по диапазону приоритета.

Методы возвращают генераторы и не создают промежуточные списки.

## Использование

### Базовый запуск демо

```bash
python -m lab3.main
```

или

```bash
python3 -m lab3.main
```

### Программное использование

```python
from lab3 import Task, TaskQueue

queue = TaskQueue([
	Task(id="T-1", priority=2, status="new"),
	Task(id="T-2", priority=5, status="in_progress"),
])

for task in queue.iter_by_priority(min_priority=4):
	print(task.id)
```

### Тестирование

```bash
pytest
```

С покрытием:

```bash
pytest --cov=lab3 --cov-report=term-missing
```

## Docker

Сборка образа и прогон тестов внутри контейнера:

```bash
docker build -t lab3-python2 .
docker run --rm lab3-python2
```

## Чему я научился


1. Реализация пользовательских итерируемых коллекций в Python.
2. Явная реализация итераторов и корректное завершение через `StopIteration`.
3. Ленивые вычисления и фильтрация с использованием генераторов.
4. Проектирование очереди задач с совместимостью со стандартным Python API.
5. Тестирование итераторов и генераторов в `pytest` с контролем покрытия.