"""Plugin to control system volume."""
from __future__ import annotations
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from networkx import volume
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


from . import BasePlugin


class Plugin(BasePlugin):
    """Adjust the system volume using pactl."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "volumen" in text or "volume" in text

    def handle(self, text: str) -> str:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # Leer volumen actual (escala -65 a 0)
        current_db = volume.GetMasterVolumeLevel()
        print("Volumen actual (dB):", current_db)

        text = text.lower()
        if any(word in text for word in ["sube", "subir", "aumenta", "aumentar"]):
            volume.SetMasterVolumeLevelScalar(volume.GetMasterVolumeLevelScalar() + 0.1, None)
            return "Subiendo volumen"
        if any(word in text for word in ["baja", "bajar", "reduce", "reducir"]):
            volume.SetMasterVolumeLevelScalar(volume.GetMasterVolumeLevelScalar() - 0.1, None)
            return "Bajando volumen"
        if any(word in text for word in ["mute", "silencia", "silenciar"]):
            volume.SetMute(1, None)
            return "Silenciando volumen"
        if any(word in text for word in ["unmute", "sonido", "activa", "activar"]):
            volume.SetMute(0, None)  # 0 para desmutear
            return "Activando volumen"
        return "No se reconoció la orden de volumen"
