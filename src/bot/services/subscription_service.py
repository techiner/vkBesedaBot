"""Subscription service."""

from typing import List
from bot.storage.db_store import SubscriptionsStore


def get_subscribers(subscription_type: str = "шутки") -> List[int]:
    """
    Get list of all subscribers.

    Args:
        subscription_type: Type of subscription (default: "шутки")

    Returns:
        List of peer_ids
    """
    store = SubscriptionsStore()
    return store.load_subscriptions(subscription_type)


def add_subscriber(peer_id: int, subscription_type: str = "шутки") -> bool:
    """
    Add a new subscriber.

    Args:
        peer_id: Peer ID to add
        subscription_type: Type of subscription (default: "шутки")

    Returns:
        True if added, False if already exists
    """
    store = SubscriptionsStore()
    return store.add_subscription(peer_id, subscription_type)

