#!/usr/bin/env python3
"""
Скрипт для создания и инициализации таблиц SQLite базы данных.

Создаёт следующие таблицы:
1. phrases - триггерные фразы, на которые реагирует бот
2. phrase_responses - массив ответов для каждой триггерной фразы
3. subscriptions - подписки групп (peer_id) на различные типы рассылок
"""

import sqlite3
from pathlib import Path
from bot.config.settings import settings
from bot.storage.db_store import create_tables


def create_tables_wrapper(conn: sqlite3.Connection) -> None:
    """Обёртка для create_tables с выводом сообщения."""
    create_tables(conn)
    conn.commit()
    print("✓ Таблицы успешно созданы")


def verify_tables(conn: sqlite3.Connection) -> None:
    """Проверяет, что все таблицы созданы корректно."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name IN ('phrases', 'phrase_responses', 'subscriptions')
    """)
    tables = [row[0] for row in cursor.fetchall()]
    
    expected_tables = {'phrases', 'phrase_responses', 'subscriptions'}
    if set(tables) == expected_tables:
        print("✓ Все таблицы присутствуют в базе данных")
    else:
        missing = expected_tables - set(tables)
        print(f"⚠ Предупреждение: отсутствуют таблицы: {missing}")


def main():
    """Основная функция для инициализации базы данных."""
    # Создаём директорию data, если её нет
    db_path = Path(settings.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Инициализация базы данных: {settings.DB_PATH}")
    
    # Подключаемся к базе данных (создаётся автоматически, если не существует)
    conn = sqlite3.connect(settings.DB_PATH)
    
    try:
        create_tables_wrapper(conn)
        verify_tables(conn)
        print(f"\n✓ База данных успешно инициализирована: {settings.DB_PATH}")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()

