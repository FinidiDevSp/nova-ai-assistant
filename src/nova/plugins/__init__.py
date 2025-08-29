"""Plugin infrastructure for Nova assistant."""
from __future__ import annotations

import importlib
from typing import List, Type


class BasePlugin:
    """Base class for all plugins."""

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or {}

    def can_handle(self, text: str) -> bool:
        """Return True if plugin can handle the provided command."""
        raise NotImplementedError

    def handle(self, text: str) -> str:
        """Execute the plugin action and return a human readable result."""
        raise NotImplementedError


def load_plugins(plugin_names: List[str], config: dict | None = None) -> List[BasePlugin]:
    """Dynamically import and instantiate plugin classes."""
    plugins: List[BasePlugin] = []
    for name in plugin_names:
        module = importlib.import_module(f"{__name__}.{name}")
        plugin_cls: Type[BasePlugin] = getattr(module, "Plugin")
        try:
            plugins.append(plugin_cls(config))
        except TypeError:
            plugins.append(plugin_cls())
    return plugins
