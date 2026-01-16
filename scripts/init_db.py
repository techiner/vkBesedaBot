#!/usr/bin/env python3
"""
Скрипт для создания и инициализации таблиц SQLite базы данных.
Можно запускать из корня проекта: python scripts/init_db.py
"""

import sys
from pathlib import Path

# Добавляем src в путь для импорта модулей бота
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from bot.storage.init_db import main

if __name__ == "__main__":
    main()

