#!/usr/bin/env python3
"""
Скрипт для создания и инициализации таблиц SQLite базы данных.

Создаёт следующие таблицы:
1. phrases - триггерные фразы, на которые реагирует бот
2. phrase_responses - массив ответов для каждой триггерной фразы
3. subscriptions - подписки групп (peer_id) на различные типы рассылок
"""

import sqlite3
import os
from pathlib import Path


DB_PATH = os.path.join("data", "bot.db")


def create_tables(conn: sqlite3.Connection) -> None:
    """Создаёт все необходимые таблицы в базе данных."""
    cursor = conn.cursor()

    # Таблица триггерных фраз
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase_text TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Таблица ответов на фразы (один-ко-многим с phrases)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phrase_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase_id INTEGER NOT NULL,
            response_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (phrase_id) REFERENCES phrases(id) ON DELETE CASCADE
        )
    """)

    # Таблица подписок
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            peer_id INTEGER NOT NULL,
            subscription_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(peer_id, subscription_type)
        )
    """)

    # Создаём индексы для ускорения запросов
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_phrase_responses_phrase_id 
        ON phrase_responses(phrase_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_subscriptions_peer_id 
        ON subscriptions(peer_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_subscriptions_type 
        ON subscriptions(subscription_type)
    """)

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
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        Path(db_dir).mkdir(parents=True, exist_ok=True)

    print(f"Инициализация базы данных: {DB_PATH}")
    
    # Подключаемся к базе данных (создаётся автоматически, если не существует)
    conn = sqlite3.connect(DB_PATH)
    
    try:
        create_tables(conn)
        verify_tables(conn)
        print(f"\n✓ База данных успешно инициализирована: {DB_PATH}")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()

