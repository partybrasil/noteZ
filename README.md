# noteZ 📝

> **Aplicación CLI minimalista para notas incrementales rápidas y continuas**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Android-green.svg)](https://github.com/partybrasil/noteZ)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 ¿Qué es noteZ?

**noteZ** es una herramienta de línea de comandos ultra-ligera diseñada para eliminar completamente la fricción entre tener una idea y guardarla permanentemente. Funciona en **Windows PowerShell 7** y **Termux (Android)** con detección automática de plataforma.

### ✨ Filosofía de Diseño

- **Zero-friction**: Escribir y guardar instantáneamente
- **Flujo continuo**: Sin interrupciones en tu workflow
- **Multiplataforma**: Mismo comportamiento en Windows y Android
- **Minimalista**: Solo lo esencial, nada más

## 🚀 Instalación

#### Windows (PowerShell 7)

```powershell
# Clona el repositorio
git clone https://github.com/partybrasil/noteZ.git
cd noteZ

# Ejecuta directamente
python notez.py

# O crea un alias para acceso global
# Añade a tu $PROFILE (alias para incluir en tu perfil de Powershell en Terminal de Windows):
function notez { python "C:\Users\usuario\proyectos\noteZ\notez.py" $args }
```

### Android (Termux)

```bash
# Instala Python si no lo tienes
pkg install python git

# Clona el repositorio
git clone https://github.com/partybrasil/noteZ.git
cd noteZ

# Ejecuta directamente
python notez.py

# O crea un alias
echo 'alias notez="python ~/noteZ/notez.py"' >> ~/.bashrc
source ~/.bashrc
```

## 📖 Uso

### 🖊️ Modo Grabación (Default)

```bash
# Inicia sesión de notas continuas
notez
```

**Prompt de grabación:**

```
[noteZ] > Tu primera nota aquí
[noteZ] > Otra nota inmediatamente
[noteZ] > /n    # Inserta línea vacía
[noteZ] > /n=   # Inserta separador decorativo
[noteZ] > /h    # Muestra ayuda
[noteZ] > /q    # Salir y guardar
```

### 👁️ Modo Lectura

```bash
# Lee tus notas guardadas
notez -r
# o
notez --read
```

**Navegación en lectura:**

- `Enter` → Muestra 5 líneas más
- `/q` → Salir del modo lectura

### 🔀 Modo Dual (Split-Screen)

```bash
# Inicia modo dual con panel dividido
notez -dual
# o
notez --dual
```

**Interfaz split-screen:**

```
╭── noteZ DUAL MODE ── Panel de Lectura (tiempo real) ──╮
│   1 │ [27-11-2025 | 10:30] Primera nota guardada      │
│   2 │ [27-11-2025 | 10:31] Segunda nota automática    │
│   3 │ [27-11-2025 | 10:32] Nueva nota aparece aquí    │
│                    (80% del terminal)                 │
╰───────────────────────────────────────────────────────╯
╭── Panel de Escritura ── /h ayuda ── /q salir ──╮
[noteZ DUAL] > Escribe tu nota aquí...
              (20% del terminal)
```

**Características del Modo Dual:**

- 📊 **Panel Superior (80%)**: Muestra las últimas notas en tiempo real
- ✏️ **Panel Inferior (20%)**: Área de escritura con prompt
- 🔄 **Actualización Automática**: Al guardar una nota, aparece arriba instantáneamente
- ⚙️ **Configurable**: Ratio de paneles ajustable en código (`DUAL_READ_PANEL_RATIO`)

### 🔒 Modo Hide (Privacidad)

```bash
# Inicia modo privacidad desde terminal
notez -hide
# o
notez --hide

# También puedes activarlo desde el modo grabación normal
[noteZ] > /hide
```

**Interfaz modo privacidad:**

```
╭─────────────────────────────────────────╮
│       noteZ - MODO PRIVACIDAD 🔒       │
│                                         │
│  La pantalla se limpia tras cada nota   │
│  Comandos: /n /n= /r /h /q               │
│  Ctrl+C para salir seguro              │
╰─────────────────────────────────────────╯

[noteZ HIDE] > Tu nota privada aquí...

# Tras presionar Enter, la pantalla se limpia:
╭─────────────────────────────────────────╮
│       noteZ - MODO PRIVACIDAD 🔒       │
╰─────────────────────────────────────────╯

✓ Nota guardada
```

**Características del Modo Hide:**

- 🔒 **Privacidad Ampliada**: La pantalla se limpia automáticamente tras guardar cada nota
- 👁️ **Información Protegida**: Lo que escribes no queda expuesto en el terminal
- 🔄 **Activación Flexible**: Desde parámetro `-hide` o comando `/hide`
- ✅ **Confirmación Visual**: Muestra "✓ Nota guardada" tras cada entrada
- 🏢 **Ideal para**: Entornos compartidos, información sensible, notas confidenciales

## 🎮 Comandos Especiales

| Comando | Función             | Descripción                          |
| ------- | -------------------- | ------------------------------------ |
| `/n`    | Línea vacía        | Inserta separador mínimo             |
| `/n=`   | Separador decorativo | Inserta línea con `==========`     |
| `/r`    | Leer notas           | Modo lectura temporal                |
| `/h`    | Ayuda                | Muestra menú de comandos             |
| `/hide` | Modo privacidad      | Activa limpieza de pantalla tras nota|
| `/q`    | Salir                | Finaliza app y guarda                 |

## 📁 Estructura de Archivos

### Rutas Automáticas por Plataforma

| Plataforma        | Ruta del archivo de notas              |
| ----------------- | -------------------------------------- |
| **Windows** | `C:\Users\<Usuario>\notez\notas.txt` |
| **Android** | `~/notez/notas.txt`                  |

### Formato de Notas

```
[24-10-2025 | 14:30] Esta es tu primera nota
[24-10-2025 | 14:31] Otra nota con timestamp automático
==========
[24-10-2025 | 14:32] Nueva sección tras separador
```

## 🔧 Características Técnicas

### Stack Tecnológico

- **Python 3.x** puro (sin dependencias externas)
- **Librerías estándar**: `sys`, `os`, `datetime`, `shutil`, `argparse`
- **Encoding**: UTF-8 para soporte completo de caracteres
- **Compatibilidad**: Windows PowerShell 7 + Termux Android

### Arquitectura Modular

```python
get_path()              # Detección automática de plataforma
get_terminal_size()     # Obtiene dimensiones del terminal
clear_screen()          # Limpieza de pantalla portable
move_cursor()           # Posicionamiento de cursor ANSI
clear_line()            # Limpieza de línea actual
write_line()            # Escritura con timestamp y comandos especiales
read_notes()            # Lectura paginada eficiente
run_dual_mode()         # Modo dual split-screen
run_hide_mode()         # Modo privacidad con limpieza de pantalla
render_dual_read_panel()# Renderizado del panel de lectura
show_help()             # Sistema de ayuda integrado
main()                  # Orquestador principal
```

### Gestión de Memoria

- **Escritura**: Append inmediato al archivo (no acumula en RAM)
- **Lectura**: Carga paginada (no carga archivo completo)
- **Escalabilidad**: Maneja archivos de cualquier tamaño

## 💡 Casos de Uso

### 🔬 Desarrollo y Debugging

```bash
[noteZ] > Bug encontrado en función login()
[noteZ] > Problema con validación de email regex
[noteZ] > /n=
[noteZ] > Solución: cambiar pattern de email
```

### 📝 Journal Técnico

```bash
[noteZ] > Iniciando implementación de feature X
[noteZ] > Decidí usar approach A en lugar de B
[noteZ] > Razón: mejor performance en casos edge
```

### 🎯 Capture Rápido de Ideas

```bash
[noteZ] > Idea: integrar AI para auto-categorización
[noteZ] > Considerar: modo offline vs online
[noteZ] > /q
```

### 📞 Notas de Reunión

```bash
[noteZ] > Meeting con equipo frontend
[noteZ] > Decisión: migrar a React 18
[noteZ] > Action item: actualizar dependencies
```

## 🛠️ Desarrollo

### Estructura del Proyecto

```
noteZ/
├── notez.py                    # Aplicación principal
├── README.md                   # Esta documentación
├── LICENSE                     # Licencia MIT
├── noteZ prototype.md          # Documento de diseño original
└── .github/
    ├── chatmodes/
    │   └── noteZ-Agent.chatmode.md    # Agente especializado
    └── project-memory.md              # Memoria extendida del proyecto
```

### Agente de Desarrollo Especializado

Este proyecto incluye un **agente de desarrollo especializado** (`noteZ-Agent.chatmode.md`) que:

- 🧠 **Domina completamente** el proyecto noteZ
- 🔄 **Mantiene memoria extendida** de todos los cambios
- ⚡ **Implementa modificaciones** con máxima eficiencia
- 📊 **Rastrea evolución** del proyecto automáticamente

## 🔄 Roadmap

### ✅ Versión Actual (1.2.0)

- [X] Modo grabación continua con timestamp
- [X] Comandos especiales (/n, /n=, /q, /h, /r, /hide)
- [X] Modo lectura paginada
- [X] Detección automática de plataforma
- [X] Manejo seguro de interrupciones
- [X] Sistema de ayuda integrado
- [X] **Modo Dual** (`-dual`/`--dual`): Split-screen con lectura en tiempo real
- [X] **Modo Hide** (`-hide`/`--hide` o `/hide`): Privacidad con limpieza de pantalla tras cada nota

### 🚧 Próximas Funcionalidades

- [ ] Búsqueda en notas (`notez -s "término"`)
- [ ] Exportación a diferentes formatos
- [ ] Categorización con tags
- [ ] Sincronización opcional con cloud
- [ ] Themes para output colorizado

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Clona** tu fork: `git clone https://github.com/partybrasil/noteZ.git`
3. **Crea** una rama: `git checkout -b feature/nueva-funcionalidad`
4. **Implementa** tus cambios usando el agente especializado
5. **Commit**: `git commit -m "feat: descripción del cambio"`
6. **Push**: `git push origin feature/nueva-funcionalidad`
7. **Pull Request** con descripción detallada

### 🎯 Usando el Agente Especializado

Para desarrollar en noteZ eficientemente:

```bash
# Activa el agente especializado en tu entorno de desarrollo
# El agente mantiene memoria completa del proyecto y puede:
# - Implementar nuevas funcionalidades
# - Refactorizar código existente  
# - Actualizar documentación automáticamente
# - Mantener consistencia arquitectónica
```

## 📜 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 🔗 Enlaces

- **Repositorio**: https://github.com/partybrasil/noteZ
- **Issues**: https://github.com/partybrasil/noteZ/issues
- **Releases**: https://github.com/partybrasil/noteZ/releases

## ⭐ Simple Gratitud

noteZ = ❤️ + código + mucha pasión por la simplicidad.
Si te sirvió = 🌟 para seguir creando magia.
¡Así de simple!

---

**noteZ** - *Donde las ideas se convierten instantáneamente en persistencia.*

> *Desarrollado con ❤️ para eliminar la fricción entre pensamiento y documentación.*
