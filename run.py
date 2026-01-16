#!/usr/bin/env python3
"""Entry point script for running the bot from project root."""

import sys
from pathlib import Path

# Добавляем src в путь
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from bot.main import main

if __name__ == "__main__":
    main()

