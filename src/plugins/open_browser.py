"""Plugin to open a web browser."""
from __future__ import annotations

import webbrowser

from . import BasePlugin


class Plugin(BasePlugin):
    """Open a web browser when the user requests it."""

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        keywords = ["abre", "abrir"]
        targets = ["chrome", "navegador", "browser"]
        return any(k in text for k in keywords) and any(t in text for t in targets)

    def handle(self, text: str) -> str:
        webbrowser.open("https://www.google.com")
        return "Abriendo navegador"
