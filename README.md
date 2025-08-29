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
3. Para el plugin de brillo instala `brightnessctl` o `xbacklight`.

## Configuración

El archivo `src/config.json` define la palabra de activación, la palabra de
desactivación, combinaciones de teclas y los plugins a cargar. También permite
configurar un fichero de memoria persistente y los escenarios disponibles.

```json
{
  "activation_word": "NOVA",
  "deactivation_word": "silencio",
  "deactivate_hotkey": "ctrl+shift+s",
  "activate_hotkey": "ctrl+shift+l",
  "memory_file": "memory.json",
  "scenarios_config": "scenarios.json",
  "plugins": [
    "open_browser",
    "system_control",
    "volume_control",
    "media_control",
    "scenario_control",
    "brightness_control",
    "timer_alarm",
    "note_taker",
    "file_manager"
  ]
}
```

La memoria se guarda en `memory.json` y conserva el historial de órdenes y
respuestas. Los escenarios se definen en `scenarios.json`, donde cada modo puede
especificar acciones a ejecutar (abrir programas, páginas web, etc.).

## Uso

Ejecuta el asistente con:

```bash
python src/main.py
```

El programa permanece escuchando y, cuando se detecta la palabra de activación,
intenta interpretar la orden con alguno de los plugins disponibles.

Puedes desactivar la escucha diciendo la palabra de desactivación o usando la
combinación `Ctrl+Shift+S`. Para volver a escuchar de forma continua utiliza
`Ctrl+Shift+L`.

Los escenarios permiten ejecutar varias acciones predefinidas, por ejemplo:
"NOVA modo trabajo" abrirá los programas y páginas configuradas para ese modo.

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
- **Control de brillo**
  - "NOVA sube el brillo"
  - "NOVA baja el brillo"
  - "NOVA brillo al 50%"
- **Control multimedia**
  - "NOVA reproduce"
  - "NOVA pausa la música"
  - "NOVA siguiente canción"
  - "NOVA canción anterior"
- **Temporizadores y alarmas**
  - "NOVA temporizador de 5 minutos"
  - "NOVA pon una alarma de 10 segundos"
- **Toma de notas**
  - "NOVA toma nota de comprar leche"
  - "NOVA anota llamar al doctor"
- **Gestión de archivos**
  - "NOVA crear carpeta proyectos"
  - "NOVA lista archivos /tmp"
  - "NOVA borra archivo demo.txt"
  - *Asegúrate de tener permisos suficientes y revisa las rutas antes de ejecutar estas acciones.*

Las notas se almacenan en `notes.txt` en la raíz del proyecto.

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
