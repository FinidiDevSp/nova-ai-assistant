from __future__ import annotations

"""Plugin que reproduce respuestas mediante síntesis de voz."""

import pyttsx3

from . import BasePlugin


class Plugin(BasePlugin):
    """Convierte texto en voz usando ``pyttsx3``."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)
        self.engine = pyttsx3.init()

    def can_handle(self, text: str) -> bool:
        """Este plugin no maneja órdenes directamente."""
        return False

    def handle(self, text: str) -> str:
        """Habla el texto proporcionado."""
        self.speak(text)
        return text

    def speak(self, text: str) -> None:
        """Reproduce en voz el texto dado."""
        self.engine.say(text)
        self.engine.runAndWait()
