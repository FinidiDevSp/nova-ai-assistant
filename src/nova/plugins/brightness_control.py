"""Plugin to control screen brightness."""
from __future__ import annotations

import re
import subprocess
from shutil import which

from . import BasePlugin


class Plugin(BasePlugin):
    """Adjust screen brightness using brightnessctl or xbacklight."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)
        if which("brightnessctl"):
            self.backend = "brightnessctl"
        elif which("xbacklight"):
            self.backend = "xbacklight"
        else:
            self.backend = None

    def can_handle(self, text: str) -> bool:
        return "brillo" in text.lower()

    def handle(self, text: str) -> str:
        text = text.lower()
        if not self.backend:
            return "No se encontró herramienta de control de brillo"

        if any(word in text for word in ["sube", "subir", "aumenta", "aumentar"]):
            if self.backend == "brightnessctl":
                subprocess.run(["brightnessctl", "set", "+10%"], check=False)
            else:
                subprocess.run(["xbacklight", "-inc", "10"], check=False)
            return "Subiendo brillo"
        if any(word in text for word in ["baja", "bajar", "reduce", "reducir"]):
            if self.backend == "brightnessctl":
                subprocess.run(["brightnessctl", "set", "10%-"], check=False)
            else:
                subprocess.run(["xbacklight", "-dec", "10"], check=False)
            return "Bajando brillo"
        match = re.search(r"brillo.*?(\d+)", text)
        if match:
            value = match.group(1)
            if self.backend == "brightnessctl":
                subprocess.run(["brightnessctl", "set", f"{value}%"], check=False)
            else:
                subprocess.run(["xbacklight", "-set", value], check=False)
            return f"Ajustando brillo al {value}%"
        return "No se reconoció la orden de brillo"
