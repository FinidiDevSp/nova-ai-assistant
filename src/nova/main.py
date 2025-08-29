"""Entry point for the Nova voice assistant."""
from __future__ import annotations

import json
import time
from pathlib import Path

import keyboard
import speech_recognition as sr

from .plugins import load_plugins


class Memory:
    """Simple persistent conversation memory."""

    def __init__(self, path: Path) -> None:
        self.path = path
        if self.path.exists():
            with self.path.open(encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = []

    def add(self, role: str, text: str) -> None:
        self.data.append({"role": role, "text": text})
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)


def listen_loop(config: dict) -> None:
    """Continuously listen for commands starting with the activation word."""

    recognizer = sr.Recognizer()
    plugins = load_plugins(config.get("plugins", []), config)
    activation_word = config.get("activation_word", "NOVA").lower()
    deactivation_word = config.get("deactivation_word", "silencio").lower()
    memory_path = Path(__file__).resolve().parent / config.get("memory_file", "memory.json")
    memory = Memory(memory_path)
    listening = True

    def deactivate() -> None:
        nonlocal listening
        listening = False
        print("Modo silencio activado")

    def activate() -> None:
        nonlocal listening
        listening = True
        print("Escuchando de nuevo")

    keyboard.add_hotkey(config.get("deactivate_hotkey", "ctrl+shift+s"), deactivate)
    keyboard.add_hotkey(config.get("activate_hotkey", "ctrl+shift+l"), activate)

    with sr.Microphone() as source:
        print(f"Escuchando. Di '{activation_word}' para activar.")
        while True:
            if not listening:
                time.sleep(0.1)
                continue
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="es-ES").lower()
                if deactivation_word in text:
                    deactivate()
                    continue
                if activation_word in text:
                    command = text.replace(activation_word, "", 1).strip()
                    if not command:
                        continue
                    print(f"Comando detectado: {command}")
                    memory.add("user", command)
                    for plugin in plugins:
                        if plugin.can_handle(command):
                            response = plugin.handle(command)
                            memory.add("assistant", response)
                            print(response)
                            break
                    else:
                        response = "No se encontró un plugin para esa orden"
                        memory.add("assistant", response)
                        print(response)
            except sr.UnknownValueError:
                continue


def main() -> None:
    config_path = Path(__file__).resolve().parent / "config.json"
    with config_path.open(encoding="utf-8") as f:
        config = json.load(f)
    listen_loop(config)


if __name__ == "__main__":
    main()
