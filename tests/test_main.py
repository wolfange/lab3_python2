from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from lab3.main import main


def test_main_runs() -> None:
    main()


def test_main_module_as_script() -> None:
    root = Path(__file__).resolve().parent.parent
    env = {**os.environ, "PYTHONPATH": str(root / "src")}
    result = subprocess.run(
        [sys.executable, "-m", "lab3.main"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Лабораторная №3: очередь задач" in result.stdout
