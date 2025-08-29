"""Plugin to take textual notes and append them to a local file."""
from __future__ import annotations

from pathlib import Path

from . import BasePlugin


class Plugin(BasePlugin):
    """Append dictated text to ``notes.txt`` in the project root."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)
        # ``notes.txt`` lives at the repository root
        self.notes_path = Path(__file__).resolve().parents[3] / "notes.txt"

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "toma nota" in text or "anota" in text

    def handle(self, text: str) -> str:
        text = text.lower()
        note = ""
        if "toma nota" in text:
            note = text.split("toma nota", 1)[1].strip()
        elif "anota" in text:
            note = text.split("anota", 1)[1].strip()
        else:
            note = text
        if not note:
            return "No se proporcionó contenido para anotar"
        self.notes_path.parent.mkdir(parents=True, exist_ok=True)
        with self.notes_path.open("a", encoding="utf-8") as f:
            f.write(note + "\n")
        return "Nota guardada"
