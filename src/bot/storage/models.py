"""Data models and types."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Subscription:
    """Subscription model."""

    peer_id: int
    subscription_type: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class Phrase:
    """Phrase model."""

    phrase_text: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class PhraseResponse:
    """Phrase response model."""

    phrase_id: int
    response_text: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None

