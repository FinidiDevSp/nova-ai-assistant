"""Plugin to manage basic system power commands."""
from __future__ import annotations

import subprocess

from . import BasePlugin


class Plugin(BasePlugin):
    """Handle power and session control commands."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        keywords = [
            "apaga",
            "apagar",
            "suspende",
            "suspender",
            "hiberna",
            "hibernar",
            "reinicia",
            "reiniciar",
        ]
        return any(k in text for k in keywords)

    def handle(self, text: str) -> str:
        text = text.lower()
        if "apaga" in text or "apagar" in text:
            subprocess.run(["shutdown", "now"], check=False)
            return "Apagando el sistema"
        if "suspende" in text or "suspender" in text:
            subprocess.run(["systemctl", "suspend"], check=False)
            return "Suspendiendo el sistema"
        if "hiberna" in text or "hibernar" in text:
            subprocess.run(["systemctl", "hibernate"], check=False)
            return "Hibernando el sistema"
        if "reinicia" in text or "reiniciar" in text:
            subprocess.run(["reboot"], check=False)
            return "Reiniciando el sistema"
        return "No se reconoció la orden del sistema"
