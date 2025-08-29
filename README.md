# Nova AI Assistant

Pequeño asistente de voz que se activa mediante una palabra clave y ejecuta
acciones mediante un sistema de _plugins_. Está pensado como base para un
proyecto estilo **J.A.R.V.I.S.**

## Instalación

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Asegúrate de que tu sistema dispone de un micrófono accesible por Python.

## Configuración

El archivo `src/config.json` define la palabra de activación y los plugins a
cargar.

```json
{
  "activation_word": "NOVA",
  "plugins": ["open_browser", "system_control", "volume_control"]
}
```

Puedes modificar `activation_word` y añadir tus propios plugins.

## Uso

Ejecuta el asistente con:

```bash
python src/main.py
```

El programa permanece escuchando y, cuando se detecta la palabra de activación,
intenta interpretar la orden con alguno de los plugins disponibles.

### Comandos soportados

- **Abrir navegador**
  - "NOVA abre Chrome"
  - "NOVA quiero que abras el navegador"
- **Control del sistema**
  - "NOVA apaga el ordenador"
  - "NOVA suspende el equipo"
- **Control de volumen**
  - "NOVA sube el volumen"
  - "NOVA baja el volumen"

## Extensión mediante plugins

Cada plugin se ubica en `src/plugins/` y hereda de `BasePlugin`. Debe implementar
los métodos `can_handle` y `handle`.

Ejemplo mínimo:

```python
from plugins import BasePlugin

class Plugin(BasePlugin):
    def can_handle(self, text: str) -> bool:
        return "hola" in text

    def handle(self, text: str) -> str:
        print("Hola mundo")
        return "Saludando"
```

Añade el nombre del módulo a la lista `plugins` de `config.json` para activarlo.
