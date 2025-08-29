"""Entry point for the Nova voice assistant."""
from __future__ import annotations

import json
from pathlib import Path

import speech_recognition as sr

from plugins import load_plugins


def listen_loop(activation_word: str, plugin_names):
    """Continuously listen for commands starting with the activation word."""
    recognizer = sr.Recognizer()
    plugins = load_plugins(plugin_names)
    activation_word = activation_word.lower()

    with sr.Microphone() as source:
        print(f"Escuchando. Di '{activation_word}' para activar.")
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="es-ES").lower()
                if activation_word in text:
                    command = text.replace(activation_word, "", 1).strip()
                    print(f"Comando detectado: {command}")
                    for plugin in plugins:
                        if plugin.can_handle(command):
                            response = plugin.handle(command)
                            print(response)
                            break
                    else:
                        print("No se encontró un plugin para esa orden")
            except sr.UnknownValueError:
                continue


def main():
    config_path = Path(__file__).resolve().parent / "config.json"
    with config_path.open(encoding="utf-8") as f:
        config = json.load(f)
    listen_loop(config.get("activation_word", "NOVA"), config.get("plugins", []))


if __name__ == "__main__":
    main()
