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

## 🎮 Comandos Especiales

| Comando | Función             | Descripción                      |
| ------- | -------------------- | --------------------------------- |
| `/n`  | Línea vacía        | Inserta separador mínimo         |
| `/n=` | Separador decorativo | Inserta línea con `==========` |
| `/h`  | Ayuda                | Muestra menú de comandos         |
| `/q`  | Salir                | Finaliza app y guarda             |

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
- **Librerías estándar**: `sys`, `os`, `datetime`
- **Encoding**: UTF-8 para soporte completo de caracteres
- **Compatibilidad**: Windows PowerShell 7 + Termux Android

### Arquitectura Modular

```python
get_path()      # Detección automática de plataforma
write_line()    # Escritura con timestamp y comandos especiales
read_notes()    # Lectura paginada eficiente
show_help()     # Sistema de ayuda integrado
main()          # Orquestador principal
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

### ✅ Versión Actual (1.0)

- [X] Modo grabación continua con timestamp
- [X] Comandos especiales (/n, /n=, /q, /h)
- [X] Modo lectura paginada
- [X] Detección automática de plataforma
- [X] Manejo seguro de interrupciones
- [X] Sistema de ayuda integrado

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
