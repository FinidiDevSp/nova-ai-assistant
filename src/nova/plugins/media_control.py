"""Plugin to control media playback using playerctl."""
from __future__ import annotations

import subprocess

from . import BasePlugin


class Plugin(BasePlugin):
    """Control media playback with playerctl."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        keywords = ["reproduce", "pausa", "siguiente", "anterior"]
        return any(k in text for k in keywords)

    def handle(self, text: str) -> str:
        text = text.lower()
        if "reproduce" in text:
            subprocess.run(["playerctl", "play"], check=False)
            return "Reproduciendo"
        if "pausa" in text:
            subprocess.run(["playerctl", "pause"], check=False)
            return "Pausando"
        if "siguiente" in text:
            subprocess.run(["playerctl", "next"], check=False)
            return "Siguiente pista"
        if "anterior" in text:
            subprocess.run(["playerctl", "previous"], check=False)
            return "Pista anterior"
        return "No se reconoció la orden multimedia"
