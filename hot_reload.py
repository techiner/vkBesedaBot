# hot_reload.py
import sys
import importlib
import os
from pathlib import Path
from watchfiles import watch
from threading import Thread

def start():
    print("Hot-reload: старт мониторинга")

    def worker():
        for changes in watch(".", debounce=1000):  # только debounce, без лишних параметров
            reloaded = set()
            for change_type, path in changes:
                if not path.endswith(".py"):
                    continue

                # Вычисляем полное имя модуля (например, subfolder.utils → subfolder.utils)
                try:
                    rel_path = Path(path).relative_to(Path(".").resolve())
                    mod_name = ".".join(rel_path.with_suffix("").parts)
                except ValueError:
                    # Если файл вне проекта — пропускаем
                    continue

                if mod_name in sys.modules and mod_name not in reloaded:
                    try:
                        importlib.reload(sys.modules[mod_name])
                        print(f"↻ Перезагружен модуль: {mod_name}")
                        reloaded.add(mod_name)
                    except Exception as e:
                        print(f"× Ошибка перезагрузки {mod_name}: {e}")

    Thread(target=worker, daemon=True).start()