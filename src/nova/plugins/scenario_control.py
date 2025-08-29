"""Plugin to execute predefined scenarios."""
from __future__ import annotations

import json
import subprocess
import webbrowser
from pathlib import Path

from . import BasePlugin


class Plugin(BasePlugin):
    """Execute actions defined for a given scenario."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)
        scenarios_file = self.config.get("scenarios_config", "scenarios.json")
        base_path = Path(__file__).resolve().parents[1]
        path = base_path / scenarios_file
        self.scenarios = {}
        if path.exists():
            with path.open(encoding="utf-8") as f:
                self.scenarios = json.load(f)

    def can_handle(self, text: str) -> bool:
        return "modo" in text.lower()

    def handle(self, text: str) -> str:
        text = text.lower()
        for name, data in self.scenarios.items():
            if name in text:
                for action in data.get("actions", []):
                    self._run_action(action)
                return f"Ejecutando escenario {name}"
        return "Escenario no encontrado"

    def _run_action(self, action: dict) -> None:
        atype = action.get("type")
        if atype == "open_program":
            cmd = action.get("command")
            if cmd:
                subprocess.Popen(cmd, shell=True)
        elif atype == "open_urls":
            for url in action.get("urls", []):
                webbrowser.open(url)
        elif atype == "run":
            cmd = action.get("command")
            if cmd:
                subprocess.Popen(cmd, shell=True)
