"""Command handlers module."""

# Используем относительные импорты для избежания циклических импортов
from . import help
from . import phrases
from . import subscribe
from . import prompt
from .base import Commands

__all__ = ['help', 'phrases', 'subscribe', 'prompt', 'Commands']
