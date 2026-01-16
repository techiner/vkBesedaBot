"""JSON file storage utilities."""

import os
import json
from typing import Dict, List, Any
from pathlib import Path
import logging
from bot.config.logging import get_logger

logger = get_logger(__name__)


class JSONStore:
    """Base class for JSON file storage."""

    def __init__(self, filepath: str):
        """
        Initialize JSON store.

        Args:
            filepath: Path to JSON file
        """
        self.filepath = filepath
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Ensure the directory for the file exists."""
        file_path = Path(self.filepath)
        file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any] | List[Any]:
        """
        Load data from JSON file.

        Returns:
            Loaded data (dict or list)
        """
        if not os.path.exists(self.filepath):
            logger.debug(f"File {self.filepath} does not exist, returning empty data")
            return {}

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Error loading {self.filepath}: {e}, returning empty data")
            return {}

    def save(self, data: Dict[str, Any] | List[Any]) -> None:
        """
        Save data to JSON file.

        Args:
            data: Data to save (dict or list)
        """
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug(f"Data saved to {self.filepath}")
        except Exception as e:
            logger.error(f"Error saving to {self.filepath}: {e}")
            raise


class PhrasesStore(JSONStore):
    """Storage for phrases."""

    def load_phrases(self) -> Dict[str, str]:
        """
        Load phrases from JSON file.

        Returns:
            Dictionary mapping trigger phrases to responses
        """
        data = self.load()
        return data if isinstance(data, dict) else {}

    def save_phrases(self, phrases: Dict[str, str]) -> None:
        """
        Save phrases to JSON file.

        Args:
            phrases: Dictionary mapping trigger phrases to responses
        """
        self.save(phrases)


class SubscriptionsStore(JSONStore):
    """Storage for subscriptions."""

    def load_subscriptions(self) -> List[int]:
        """
        Load subscriptions from JSON file.

        Returns:
            List of peer_ids
        """
        data = self.load()
        if isinstance(data, list):
            return [int(x) for x in data if isinstance(x, (int, str))]
        return []

    def save_subscriptions(self, subscriptions: List[int]) -> None:
        """
        Save subscriptions to JSON file.

        Args:
            subscriptions: List of peer_ids
        """
        unique_subs = sorted({int(x) for x in subscriptions})
        self.save(unique_subs)

