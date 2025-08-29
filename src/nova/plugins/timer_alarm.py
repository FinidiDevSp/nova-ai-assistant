"""Plugin to set timers or alarms."""
from __future__ import annotations

import re
import threading

from . import BasePlugin


def _alarm_action(message: str) -> None:
    """Print a message and emit a beep when the timer finishes."""
    print("\a" + message)


class Plugin(BasePlugin):
    """Launch a timer or alarm using ``threading.Timer``."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "temporizador" in text or "alarma" in text

    def handle(self, text: str) -> str:
        text = text.lower()
        match = re.search(r"(\d+)\s*(segundo|segundos|minuto|minutos)", text)
        if not match:
            return "No se especificó un tiempo para el temporizador"
        amount = int(match.group(1))
        unit = match.group(2)
        seconds = amount * 60 if "minuto" in unit else amount

        timer = threading.Timer(seconds, _alarm_action, args=("¡Tiempo cumplido!",))
        timer.daemon = True
        timer.start()
        return f"Temporizador iniciado por {amount} {unit}"
