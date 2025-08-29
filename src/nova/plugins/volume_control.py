"""Plugin to control system volume."""
from __future__ import annotations

import subprocess

from . import BasePlugin


class Plugin(BasePlugin):
    """Adjust the system volume using pactl."""

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "volumen" in text or "volume" in text

    def handle(self, text: str) -> str:
        text = text.lower()
        if any(word in text for word in ["sube", "subir", "aumenta", "aumentar"]):
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"], check=False)
            return "Subiendo volumen"
        if any(word in text for word in ["baja", "bajar", "reduce", "reducir"]):
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"], check=False)
            return "Bajando volumen"
        if any(word in text for word in ["mute", "silencia", "silenciar"]):
            subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"], check=False)
            return "Silenciando volumen"
        if any(word in text for word in ["unmute", "sonido", "activa", "activar"]):
            subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"], check=False)
            return "Activando volumen"
        return "No se reconoció la orden de volumen"
