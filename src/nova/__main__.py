"""Command line interface for the Nova assistant."""
from __future__ import annotations

from .main import main


def run() -> None:
    """Entry point for ``python -m nova``."""
    import argparse

    parser = argparse.ArgumentParser(description="Nova voice assistant")
    parser.add_argument("--config", help="Path to configuration file", default=None)
    parser.parse_args()
    main()


if __name__ == "__main__":  # pragma: no cover
    run()
