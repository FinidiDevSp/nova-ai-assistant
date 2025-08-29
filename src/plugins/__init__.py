"""Plugin infrastructure for Nova assistant."""
from __future__ import annotations

import importlib
from typing import List, Type


class BasePlugin:
    """Base class for all plugins."""

    def can_handle(self, text: str) -> bool:
        """Return True if plugin can handle the provided command."""
        raise NotImplementedError

    def handle(self, text: str) -> str:
        """Execute the plugin action and return a human readable result."""
        raise NotImplementedError


def load_plugins(plugin_names: List[str]) -> List[BasePlugin]:
    """Dynamically import and instantiate plugin classes."""
    plugins: List[BasePlugin] = []
    for name in plugin_names:
        module = importlib.import_module(f"plugins.{name}")
        plugin_cls: Type[BasePlugin] = getattr(module, "Plugin")
        plugins.append(plugin_cls())
    return plugins
