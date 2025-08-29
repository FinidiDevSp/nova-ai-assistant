"""Plugin to perform basic file system tasks."""
from __future__ import annotations

import os
import shutil

from . import BasePlugin


class Plugin(BasePlugin):
    """Handle simple file management commands."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return (
            "crear carpeta" in text
            or "lista archivos" in text
            or "borra archivo" in text
        )

    def handle(self, text: str) -> str:
        original = text
        text = text.lower()
        if "crear carpeta" in text:
            folder = original[text.index("crear carpeta") + len("crear carpeta") :].strip()
            if not folder:
                return "No se especificó la carpeta a crear"
            os.makedirs(folder, exist_ok=True)
            return f"Carpeta '{folder}' creada"
        if "lista archivos" in text:
            path = original[text.index("lista archivos") + len("lista archivos") :].strip() or "."
            try:
                files = os.listdir(path)
            except OSError:
                return f"No se pudo listar '{path}'"
            return ", ".join(files) if files else f"No hay archivos en '{path}'"
        if "borra archivo" in text:
            target = original[text.index("borra archivo") + len("borra archivo") :].strip()
            if not target:
                return "No se especificó el archivo a borrar"
            if os.path.isdir(target):
                shutil.rmtree(target)
                return f"Directorio '{target}' borrado"
            if os.path.isfile(target):
                os.remove(target)
                return f"Archivo '{target}' borrado"
            return "Ruta no encontrada"
        return "Comando no reconocido"
