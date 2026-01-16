"""SQLite database storage utilities."""

import sqlite3
import os
from typing import Dict, List, Optional
from pathlib import Path
from contextlib import contextmanager
from bot.config.settings import settings
from bot.config.logging import get_logger

logger = get_logger(__name__)


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.

    Yields:
        sqlite3.Connection: Database connection
    """
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()


def ensure_db_exists() -> None:
    """Ensure database file and directory exist."""
    db_path = Path(settings.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Если БД не существует, создаём таблицы
    if not db_path.exists():
        logger.info(f"Database not found at {settings.DB_PATH}, initializing...")
        # Импортируем функцию создания таблиц напрямую, чтобы избежать циклических импортов
        import sqlite3
        conn = sqlite3.connect(settings.DB_PATH)
        try:
            create_tables(conn)
            conn.commit()
        finally:
            conn.close()


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


class PhrasesStore:
    """Storage for phrases using SQLite."""

    def __init__(self):
        """Initialize phrases store."""
        ensure_db_exists()

    def load_phrases(self) -> Dict[str, List[str]]:
        """
        Load phrases from database.

        Returns:
            Dictionary mapping trigger phrases to list of responses
        """
        phrases_dict: Dict[str, List[str]] = {}
        
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Получаем фразы с их ответами
                cursor.execute("""
                    SELECT p.phrase_text, pr.response_text
                    FROM phrases p
                    LEFT JOIN phrase_responses pr ON p.id = pr.phrase_id
                    ORDER BY pr.created_at ASC
                """)
                
                for row in cursor.fetchall():
                    phrase_text = row['phrase_text']
                    response_text = row['response_text']
                    
                    # Инициализируем список ответов для фразы
                    if phrase_text not in phrases_dict:
                        phrases_dict[phrase_text] = []
                    
                    # Добавляем только непустые ответы
                    if response_text:
                        phrases_dict[phrase_text].append(response_text)
                        
        except Exception as e:
            logger.error(f"Error loading phrases: {e}")
            
        return phrases_dict

    def add_phrase(self, phrase_text: str, response_text: str) -> None:
        """
        Add a single phrase or additional response for existing phrase.

        Args:
            phrase_text: Trigger phrase text
            response_text: Response text
        """
        phrase_text_lower = phrase_text.lower()

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # Проверяем, существует ли уже фраза
                cursor.execute(
                    "SELECT id FROM phrases WHERE phrase_text = ?",
                    (phrase_text_lower,),
                )
                row = cursor.fetchone()

                if row:
                    # Фраза существует — добавляем ещё один ответ
                    phrase_id = row["id"]
                else:
                    # Фразы нет — создаём новую
                    cursor.execute(
                        "INSERT INTO phrases (phrase_text) VALUES (?)",
                        (phrase_text_lower,),
                    )
                    phrase_id = cursor.lastrowid

                # Добавляем ответ, не трогая существующие
                cursor.execute(
                    """
                    INSERT INTO phrase_responses (phrase_id, response_text)
                    VALUES (?, ?)
                    """,
                    (phrase_id, response_text),
                )

                conn.commit()
                logger.debug(
                    f"Added phrase/response: phrase='{phrase_text_lower}', response='{response_text}'"
                )

        except Exception as e:
            logger.error(f"Error adding phrase: {e}")
            raise

    def delete_phrase(self, phrase_text: str) -> bool:
        """
        Delete a phrase.

        Args:
            phrase_text: Phrase text to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Находим фразу
                cursor.execute("SELECT id FROM phrases WHERE phrase_text = ?", (phrase_text.lower(),))
                row = cursor.fetchone()
                
                if row:
                    phrase_id = row['id']
                    # Удаление каскадное, так что удалится и из phrase_responses
                    cursor.execute("DELETE FROM phrases WHERE id = ?", (phrase_id,))
                    conn.commit()
                    logger.debug(f"Deleted phrase: {phrase_text}")
                    return True
                else:
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting phrase: {e}")
            raise


class SubscriptionsStore:
    """Storage for subscriptions using SQLite."""

    def __init__(self):
        """Initialize subscriptions store."""
        ensure_db_exists()

    def load_subscriptions(self, subscription_type: str = "шутки") -> List[int]:
        """
        Load subscriptions from database.

        Args:
            subscription_type: Type of subscription (default: "шутки")

        Returns:
            List of peer_ids
        """
        subscriptions = []
        
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT peer_id FROM subscriptions
                    WHERE subscription_type = ?
                """, (subscription_type,))
                
                subscriptions = [row['peer_id'] for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error loading subscriptions: {e}")
            
        return subscriptions

    def save_subscriptions(self, subscriptions: List[int], subscription_type: str = "шутки") -> None:
        """
        Save subscriptions to database.

        Args:
            subscriptions: List of peer_ids
            subscription_type: Type of subscription (default: "шутки")
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Удаляем все подписки данного типа
                cursor.execute("DELETE FROM subscriptions WHERE subscription_type = ?", (subscription_type,))
                
                # Добавляем новые подписки
                for peer_id in subscriptions:
                    cursor.execute("""
                        INSERT OR IGNORE INTO subscriptions (peer_id, subscription_type)
                        VALUES (?, ?)
                    """, (peer_id, subscription_type))
                
                conn.commit()
                logger.debug(f"Saved {len(subscriptions)} subscriptions of type '{subscription_type}'")
                
        except Exception as e:
            logger.error(f"Error saving subscriptions: {e}")
            raise

    def add_subscription(self, peer_id: int, subscription_type: str = "шутки") -> bool:
        """
        Add a single subscription.

        Args:
            peer_id: Peer ID to add
            subscription_type: Type of subscription (default: "шутки")

        Returns:
            True if added, False if already exists
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Проверяем, существует ли уже подписка
                cursor.execute("""
                    SELECT id FROM subscriptions
                    WHERE peer_id = ? AND subscription_type = ?
                """, (peer_id, subscription_type))
                
                if cursor.fetchone():
                    return False
                
                # Добавляем подписку
                cursor.execute("""
                    INSERT INTO subscriptions (peer_id, subscription_type)
                    VALUES (?, ?)
                """, (peer_id, subscription_type))
                
                conn.commit()
                logger.debug(f"Added subscription: peer_id={peer_id}, type={subscription_type}")
                return True
                
        except Exception as e:
            logger.error(f"Error adding subscription: {e}")
            raise

    def remove_subscription(self, peer_id: int, subscription_type: str = "шутки") -> bool:
        """
        Remove a subscription.

        Args:
            peer_id: Peer ID to remove
            subscription_type: Type of subscription (default: "шутки")

        Returns:
            True if removed, False if not found
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM subscriptions
                    WHERE peer_id = ? AND subscription_type = ?
                """, (peer_id, subscription_type))
                
                conn.commit()
                deleted = cursor.rowcount > 0
                if deleted:
                    logger.debug(f"Removed subscription: peer_id={peer_id}, type={subscription_type}")
                return deleted
                
        except Exception as e:
            logger.error(f"Error removing subscription: {e}")
            raise

            