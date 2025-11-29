```markdown
# CONTEXTO DEL PROYECTO

[prompt

1. Quiero que analices el prompt de la propuesta de implantacion y lo implementes, recuerda debe ser minimalista, la app sin dependencias externas, la funcion de cloud sync  es una interaccion con Github CLI, para crear el repositorio de notas syncronizadas, actualizar, subir y descargar las notas. Sin usar esta funcion la app funciona localmente y manualmente sin problemas

Explicame lo que has entendido para no liarnos y te confirmo para que prosigas


2. Esta perfecto, puedes proceder directamente con la implantacion. Pero recuerda que cuando vaya hacer login con gh cli debe verificar si este ya se encuentra logueado con gh auth status, si ya esta logueado salta el login y continua con el flujo]

noteZ es una aplicación CLI minimalista para notas rápidas que funciona en Windows PowerShell 7 y Termux Android. Actualmente guarda las notas localmente en:
- Windows: C:\Users\<usuario>\notez\notas.txt
- Android: ~/notez/notas.txt

El archivo principal es notez.py (Python 3.x puro, sin dependencias externas).

---

# OBJETIVO DE LA IMPLEMENTACIÓN

Añadir una funcionalidad OPCIONAL de sincronización en la nube que permita al usuario:
1. Guardar sus notas en un repositorio Git privado
2. Sincronizar cambios entre múltiples máquinas
3. Mantener un backup automático versionado de sus notas

**IMPORTANTE**: La funcionalidad local sigue siendo la principal. La sincronización es completamente opcional y no debe requerir configuración si el usuario no la usa.

---

# ARQUITECTURA DE LA SOLUCIÓN

## Separación de Repositorios

Debe existir una clara separación entre:
- **Repo de la aplicación** (partybrasil/noteZ): Código público de la app
- **Repo de notas del usuario** (usuario/notez-sync): Datos privados del usuario

La sincronización SOLO afecta al repo de notas del usuario, NUNCA al código de la app.

## Ubicación de Archivos

```
# Estructura en el sistema:

# Repo de la app (instalado por el usuario)
C:\proyectos\noteZ\
├── notez.py          # Código de la aplicación
├── README.md
└── .git/             # Git del repo de la app

# Carpeta de datos del usuario (creada por la app)
C:\Users\usuario\notez\
├── notas.txt         # Archivo de notas del usuario
├── .git/             # Git del repo de NOTAS (separado)
├── .gitignore        # Ignora archivos temporales
└── .notez-sync.json  # Configuración local del sync (no se sube)
```

---

# MÉTODO DE AUTENTICACIÓN: GitHub CLI

La autenticación debe usar GitHub CLI (`gh`) porque:
- Es la solución más minimalista (una dependencia externa)
- Login una vez, funciona siempre automáticamente
- No requiere configurar SSH keys manualmente
- No requiere crear/gestionar Personal Access Tokens
- Funciona idénticamente en Windows y Termux
- Git usa la autenticación de `gh` de forma transparente

## Detección de GitHub CLI

La app debe:
1. Detectar si `gh` está instalado en el sistema (comando disponible en PATH)
2. Verificar si el usuario está autenticado (`gh auth status`)
3. Ofrecer guías de instalación/autenticación si no está disponible
4. Funcionar sin GitHub CLI pero informar que el sync no estará disponible

---

# CLASE SyncManager

Crear una nueva clase `SyncManager` que encapsule toda la lógica de sincronización.

## Atributos de la Clase

```
- notes_path: Ruta completa a notas.txt
- notes_dir: Directorio que contiene notas.txt
- config_file: Ruta a .notez-sync.json
- sync_enabled: Boolean que indica si hay sync configurado
- gh_available: Boolean que indica si GitHub CLI está disponible y autenticado
```

## Archivo de Configuración (.notez-sync.json)

Debe guardarse en la carpeta de notas (no se sube al repo) con:
```
{
  "repo_url": "https://github.com/usuario/notez-sync.git",
  "auth_method": "gh-cli",
  "setup_date": "2025-11-29T09:00:00",
  "last_sync": "2025-11-29T09:30:00"
}
```

---

# MÉTODOS PRINCIPALES

## 1. _check_gh_cli()

**Propósito**: Verificar disponibilidad de GitHub CLI

**Lógica**:
1. Usar `shutil.which('gh')` para verificar si el comando existe
2. Si existe, ejecutar `gh auth status` con capture_output y timeout de 5 segundos
3. Retornar True si returncode es 0, False en cualquier otro caso
4. Manejar excepciones de timeout o comando no encontrado

**Consideraciones**:
- Debe ser rápido (no más de 5 segundos)
- No debe interrumpir el flujo si `gh` no está disponible
- Debe capturar stderr donde `gh auth status` devuelve información

---

## 2. _prompt_gh_install()

**Propósito**: Mostrar instrucciones de instalación de GitHub CLI

**Lógica**:
1. Detectar el sistema operativo (sys.platform)
2. Mostrar instrucciones específicas para:
   - Windows: `winget install --id GitHub.cli` o `choco install gh`
   - Termux: `pkg install gh`
3. Incluir instrucciones de autenticación: `gh auth login`
4. Usar formato visual con marcos (╭─╮│╰─╯) consistente con el estilo de noteZ

**No debe**:
- Interrumpir el flujo de la aplicación
- Instalar nada automáticamente
- Requerir respuesta del usuario (solo informativo)

---

## 3. setup(repo_url)

**Propósito**: Configurar sincronización por primera vez

**Validaciones previas**:
1. Verificar que repo_url no sea el repo de la app (partybrasil/noteZ)
2. Si no es SSH ni HTTPS válido, mostrar error
3. Detectar estado de GitHub CLI con _check_gh_cli()

**Flujo principal**:

### 3.1. Verificación de Autenticación

Si GitHub CLI NO está disponible:
- Mostrar mensaje de advertencia (no error)
- Llamar a _prompt_gh_install()
- Preguntar si quiere continuar de todas formas
- Si acepta, continuar con setup pero marcar auth_method como 'manual'

Si GitHub CLI está disponible:
- Mostrar confirmación visual de autenticación exitosa
- Extraer y mostrar el usuario de GitHub autenticado del output de `gh auth status`

### 3.2. Inicialización del Repositorio Git

Ejecutar en orden (todos con check=True para detectar errores):

1. `git init <notes_dir>` - Inicializar Git en la carpeta de notas
2. `git -C <notes_dir> remote add origin <repo_url>` - Configurar remote

### 3.3. Crear .gitignore

Crear archivo .gitignore en notes_dir con:
```
# noteZ - Archivos ignorados
__pycache__/
*.pyc
.DS_Store
*.swp
.notez-sync.json
```

**Importante**: .notez-sync.json NO debe subirse (es configuración local)

### 3.4. Commit Inicial

1. `git -C <notes_dir> add notas.txt .gitignore`
2. `git -C <notes_dir> commit -m "[noteZ] Configuración inicial"`
3. `git -C <notes_dir> branch -M main` - Asegurar rama main

### 3.5. Push Inicial de Verificación

1. Ejecutar `git -C <notes_dir> push -u origin main`
2. Si returncode == 0: Éxito total
3. Si falla con error de autenticación:
   - Verificar si GitHub CLI está instalado pero no autenticado
   - Mostrar instrucciones claras según el caso
   - NO crear el config si falla (setup incompleto)

### 3.6. Guardar Configuración

Solo si el push fue exitoso:
1. Crear diccionario con: repo_url, auth_method, setup_date, last_sync
2. Guardar como JSON en .notez-sync.json con formato legible (indent=2)

**Mensajes finales**:
- Éxito: Mostrar repo configurado, método de autenticación, próximos pasos
- Error: Explicar qué falló y cómo resolverlo sin tecnicismos

---

## 4. push()

**Propósito**: Subir cambios locales al repo remoto

**Validaciones previas**:
1. Verificar que sync_enabled sea True (existe .git/)
2. Si no está configurado, mostrar mensaje: "Usa: notez --setup-sync [URL]"

**Flujo principal**:

### 4.1. Agregar Cambios

1. `git -C <notes_dir> add notas.txt` - SOLO agregar notas.txt
2. No agregar otros archivos automáticamente

### 4.2. Verificar si Hay Cambios

1. Ejecutar `git -C <notes_dir> status --porcelain`
2. Si stdout está vacío: Informar "Sin cambios para sincronizar" y retornar
3. Esto evita commits vacíos

### 4.3. Crear Commit

1. Generar timestamp: `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`
2. Ejecutar `git -C <notes_dir> commit -m "[noteZ] Sync <timestamp>"`
3. Usar capture_output para no mostrar output de Git

### 4.4. Push al Remoto

1. Ejecutar `git -C <notes_dir> push -u origin main`
2. Capturar stdout y stderr

**Manejo de resultados**:

Si returncode == 0 (éxito):
- Mostrar "✅ Notas sincronizadas"
- Actualizar last_sync en config con timestamp actual
- Guardar config actualizado

Si falla con error de autenticación:
- Detectar keywords en stderr: 'authentication', 'permission denied', 'authorization'
- Verificar si GitHub CLI está disponible
- Mensajes diferenciados:
  - Si gh no está: Guía de instalación
  - Si gh está pero no autenticado: `gh auth login`
  - Si gh está autenticado: Error de permisos del repo

Si falla por otros motivos:
- Mostrar stderr capturado
- Sugerir verificar conexión a internet
- Mencionar `notez --sync-status` para diagnóstico

---

## 5. pull()

**Propósito**: Descargar cambios del repo remoto

**Validaciones previas**:
1. Verificar sync_enabled
2. Si no está configurado, mostrar mensaje alternativo:
   - En máquina nueva: `gh repo clone usuario/notez-sync ~/notez`
   - Si ya existe: Configurar primero con --setup-sync

**Flujo principal**:

### 5.1. Verificar Estado Local

1. Ejecutar `git -C <notes_dir> status --porcelain`
2. Si hay cambios locales sin commit:
   - Advertir al usuario: "Tienes cambios locales sin sincronizar"
   - Preguntar: "¿Hacer commit automático antes de pull? (s/n)"
   - Si acepta: Ejecutar commit automático con mensaje "[noteZ] Auto-save antes de pull"
   - Si rechaza: Abortar pull y sugerir `notez --push` primero

### 5.2. Pull con Merge Automático

1. Ejecutar `git -C <notes_dir> pull origin main`
2. Git intentará merge automático

**Manejo de conflictos**:

Si hay conflictos de merge:
- Detectar líneas con markers de conflicto en notas.txt (<<<<<<, ======, >>>>>>)
- Mostrar mensaje claro: "Conflicto detectado en notas.txt"
- Opciones para el usuario:
  1. Abrir notas.txt para resolver manualmente
  2. Mantener versión local (git checkout --ours)
  3. Usar versión remota (git checkout --theirs)
  4. Cancelar pull (git merge --abort)
- Implementar prompts interactivos para cada opción
- Después de resolver: `git add notas.txt` y `git commit --no-edit`

Si pull es exitoso sin conflictos:
- Mostrar "✅ Notas descargadas y sincronizadas"
- Actualizar last_sync en config

---

## 6. sync()

**Propósito**: Sincronización bidireccional inteligente (push + pull)

**Flujo principal**:

### 6.1. Fetch Primero

1. Ejecutar `git -C <notes_dir> fetch origin main`
2. Esto descarga cambios sin aplicarlos

### 6.2. Comparar Estados

1. `git -C <notes_dir> rev-parse HEAD` - Commit local
2. `git -C <notes_dir> rev-parse origin/main` - Commit remoto
3. `git -C <notes_dir> merge-base HEAD origin/main` - Ancestro común

**Escenarios**:

a) **Local == Remoto**: 
   - Informar "Ya sincronizado"
   - No hacer nada

b) **Local está adelante, remoto igual al ancestro**:
   - Solo hay cambios locales
   - Ejecutar push()

c) **Remoto está adelante, local igual al ancestro**:
   - Solo hay cambios remotos
   - Ejecutar pull()

d) **Ambos adelantados (divergencia)**:
   - Hay cambios en ambos lados
   - Intentar pull (merge automático)
   - Si hay conflictos: Usar lógica de resolución de pull()
   - Después: Ejecutar push()

### 6.3. Confirmación Final

- Mostrar resumen: "Cambios subidos: X commits, Cambios descargados: Y commits"
- Actualizar last_sync

---

## 7. status()

**Propósito**: Mostrar estado actual de la sincronización

**Información a mostrar**:

### 7.1. Estado de GitHub CLI
- Instalado: Sí/No
- Autenticado: Sí/No
- Usuario: (extraer de gh auth status)

### 7.2. Estado del Sync
- Configurado: Sí/No
- Repo URL: (mostrar si existe)
- Último sync: (fecha/hora legible)

### 7.3. Estado Git Local
- Ejecutar `git -C <notes_dir> status --porcelain`
- Si hay cambios: "⚠️ Cambios locales sin sincronizar"
- Si está limpio: "✅ Sincronizado"

### 7.4. Comparación con Remoto
- `git fetch` silencioso
- Comparar commits local vs remoto
- Mostrar: "X commits locales pendientes", "Y commits remotos disponibles"

**Formato visual**:
```
╭────────────────────────────────────────╮
│   noteZ - Estado de Sincronización     │
├────────────────────────────────────────┤
│ GitHub CLI: ✅ Autenticado (usuario)   │
│ Repo: github.com/usuario/notez-sync    │
│ Último sync: 29-11-2025 09:30          │
│ Estado: ✅ Sincronizado                │
│         (Sin cambios pendientes)       │
╰────────────────────────────────────────╯
```

---

# INTEGRACIÓN CON main()

## Nuevos Argumentos de CLI

Añadir al parser de argparse:

```
--login
  Descripción: Iniciar sesión en GitHub usando GitHub CLI
  Acción: Ejecutar wrapper de gh auth login con instrucciones

--setup-sync REPO_URL
  Descripción: Configurar repositorio para sincronización
  Metavar: REPO_URL
  Ejemplo: https://github.com/usuario/notez-sync.git
  Acción: Llamar a SyncManager.setup()

--push
  Descripción: Subir cambios locales al repositorio remoto
  Acción: Llamar a SyncManager.push()

--pull
  Descripción: Descargar cambios del repositorio remoto
  Acción: Llamar a SyncManager.pull()

--sync
  Descripción: Sincronización bidireccional (push + pull inteligente)
  Acción: Llamar a SyncManager.sync()

--sync-status
  Descripción: Mostrar estado de la sincronización
  Acción: Llamar a SyncManager.status()
```

## Orden de Procesamiento

Estos comandos deben procesarse ANTES del flujo principal de la app:

```
# En main(), después de parsear args y antes de los modos (read/dual/write):

if args.login:
    # Manejar login de GitHub CLI
    sys.exit(0)

if args.setup_sync:
    # Manejar configuración de sync
    sys.exit(0)

if args.push:
    # Manejar push
    sys.exit(0)

if args.pull:
    # Manejar pull
    sys.exit(0)

if args.sync:
    # Manejar sync bidireccional
    sys.exit(0)

if args.sync_status:
    # Mostrar estado
    sys.exit(0)

# Después continuar con flujo normal (read/dual/write)
```

---

# MANEJO DE ERRORES

## Principios Generales

1. **Nunca crashear la app**: Todos los errores de sync deben capturarse
2. **Mensajes claros**: Sin jerga técnica, explicar qué pasó y cómo resolverlo
3. **Degradación elegante**: Si sync falla, la app local debe seguir funcionando
4. **Timeouts**: Comandos de red deben tener timeout de 10 segundos máximo

## Errores Específicos a Manejar

### Error: GitHub CLI no instalado
```
⚠️  GitHub CLI no está instalado

La sincronización en la nube requiere GitHub CLI.

Instalación:
  Windows: winget install --id GitHub.cli
  Termux:  pkg install gh

Después ejecuta: notez --login
```

### Error: No autenticado con GitHub CLI
```
⚠️  No has iniciado sesión en GitHub

Ejecuta: notez --login
O manualmente: gh auth login
```

### Error: Repo no existe
```
❌ El repositorio no existe o no tienes acceso

1. Verifica que el repo existe: github.com/usuario/notez-sync
2. Asegúrate de que es privado y tú eres el propietario
3. Verifica tu autenticación: notez --sync-status
```

### Error: Sin conexión a internet
```
❌ No se puede conectar con GitHub

Verifica tu conexión a internet e intenta de nuevo.
```

### Error: Conflictos de merge
```
⚠️  Conflicto detectado en notas.txt

Tienes cambios en ambos lados (local y remoto).

Opciones:
  1. Resolver manualmente: Edita notas.txt y elimina los markers
  2. Mantener versión local: notez --force-local
  3. Usar versión remota: notez --force-remote

Después ejecuta: notez --push
```

---

# MENSAJES DE AYUDA Y EDUCACIÓN

## Ayuda del Comando --login

Cuando el usuario ejecuta `notez --login`:

```
╭────────────────────────────────────────────────────╮
│   Autenticación con GitHub                         │
├────────────────────────────────────────────────────┤
│                                                    │
│  Se iniciará el asistente de GitHub CLI.          │
│                                                    │
│  Pasos:                                            │
│  1. Selecciona: GitHub.com                         │
│  2. Protocolo: HTTPS (más simple)                  │
│  3. Autenticación: Login with web browser         │
│  4. Copia el código de 8 dígitos                   │
│  5. Presiona Enter (se abre el navegador)          │
│  6. Pega el código en la página                    │
│  7. Autoriza GitHub CLI                            │
│                                                    │
│  Después podrás usar:                              │
│  -  notez --setup-sync [URL]                        │
│  -  notez --push                                    │
│  -  notez --pull                                    │
│                                                    │
╰────────────────────────────────────────────────────╯

Presiona Enter para continuar...
```

## Ayuda del Comando --setup-sync

Cuando el usuario ejecuta sin argumentos o con URL inválida:

```
Uso: notez --setup-sync REPO_URL

REPO_URL debe ser un repositorio Git privado en GitHub.

Pasos previos:
  1. Crea un repo privado en github.com/new
     Nombre sugerido: notez-sync
     Privacidad: Private ✓
     NO añadas README ni .gitignore

  2. Copia la URL del repo:
     https://github.com/tu-usuario/notez-sync.git

  3. Ejecuta:
     notez --setup-sync https://github.com/tu-usuario/notez-sync.git

Nota: Este repo es SOLO para tus notas, no el repo de la app.
```

---

# CONSIDERACIONES DE SEGURIDAD

## Privacidad de las Notas

1. **Nunca usar repos públicos**: Validar que el usuario entiende que debe ser privado
2. **No hardcodear credenciales**: Siempre usar GitHub CLI o SSH, nunca tokens en código
3. **Archivo .notez-sync.json**: Debe estar en .gitignore (no subirse al repo)

## Validaciones

1. **URL del repo**: No permitir usar partybrasil/noteZ
2. **Permisos**: Verificar acceso antes de configurar completamente
3. **Conflictos**: Nunca sobrescribir cambios sin confirmación del usuario

---

# TESTING MANUAL

Implementar estos escenarios de prueba:

1. **Setup inicial sin GitHub CLI**
   - Verificar mensajes de instalación
   - No debe fallar, solo advertir

2. **Setup inicial con GitHub CLI**
   - Debe detectar autenticación
   - Crear repo Git correctamente
   - Hacer push inicial exitoso

3. **Push con cambios locales**
   - Crear notas
   - Ejecutar push
   - Verificar en GitHub que se subieron

4. **Pull sin cambios locales**
   - Modificar notas en GitHub (web)
   - Ejecutar pull
   - Verificar que se descargaron

5. **Sync con cambios en ambos lados**
   - Cambios locales y remotos diferentes
   - No deben haber conflictos (líneas diferentes)
   - Debe hacer merge automático

6. **Conflicto real**
   - Cambiar la misma línea local y remotamente
   - Ejecutar sync
   - Debe detectar conflicto y pedir resolución

7. **Máquina nueva**
   - Clonar repo de notas: `gh repo clone usuario/notez-sync ~/notez`
   - Ejecutar noteZ
   - Debe tener todas las notas

---

# COMPATIBILIDAD MULTIPLATAFORMA

## Windows PowerShell 7

- Todos los comandos de Git deben usar rutas con barras `/` o `os.path.join()`
- GitHub CLI funciona nativamente
- Usar `subprocess.run()` con lista de argumentos, no strings

## Termux Android

- GitHub CLI disponible via `pkg install gh`
- Rutas Unix-style
- Mismo código debe funcionar sin cambios
- Probar timeout en conexiones lentas

---

# DOCUMENTACIÓN EN CÓDIGO

## Docstrings

Cada método debe tener docstring con:
- Propósito en una línea
- Args: Tipo y descripción de parámetros
- Returns: Qué retorna y cuándo
- Raises: Excepciones que puede lanzar (si aplica)
- Ejemplo de uso (si es complejo)

## Comentarios Inline

Explicar decisiones no obvias:
- Por qué se usa un timeout específico
- Por qué se ignora un error particular
- Lógica de detección de conflictos

---

# ACTUALIZACIÓN DEL README.md

Añadir nueva sección después de "Uso":

## 🔐 Sincronización en la Nube (Opcional)

Documenta:
1. Requisitos (GitHub CLI)
2. Instalación de GitHub CLI
3. Setup paso a paso
4. Comandos disponibles
5. Troubleshooting común
6. FAQs sobre privacidad

Formato: Markdown claro con ejemplos de comandos

---

# PRIORIZACIÓN DE IMPLEMENTACIÓN

## Fase 1 (MVP)
- Clase SyncManager básica
- Métodos: _check_gh_cli, setup, push, pull
- Argumentos CLI: --login, --setup-sync, --push, --pull
- Manejo básico de errores

## Fase 2 (Mejoras)
- Método sync() bidireccional
- Método status() con diagnóstico
- Resolución de conflictos interactiva
- Mensajes de ayuda completos

## Fase 3 (Pulido)
- Testing exhaustivo
- Documentación completa
- Validaciones adicionales
- Optimización de timeouts

---

# RESULTADOS ESPERADOS

Al finalizar, el usuario debe poder:

1. **Setup en 3 comandos**:
   ```
   notez --login
   notez --setup-sync https://github.com/usuario/notez-sync.git
   notez --push
   ```

2. **Uso diario simple**:
   ```
   notez  # Escribir notas
   notez --push  # Sincronizar cuando quiera
   ```

3. **Máquina nueva en 2 comandos**:
   ```
   notez --login
   gh repo clone usuario/notez-sync ~/notez
   ```

4. **Diagnóstico fácil**:
   ```
   notez --sync-status
   ```

**La sincronización debe ser tan invisible y fluida que el usuario olvide que está usando Git.**

---

# NOTAS FINALES

- Mantener el estilo minimalista de noteZ (sin dependencias Python adicionales)
- Todos los mensajes en español consistente con la app
- Formato visual con marcos (╭─╮│╰─╯) para consistencia
- Priorizar experiencia de usuario sobre funcionalidades técnicas
- Si algo falla, la app local debe seguir funcionando perfectamente
- GitHub CLI es un requisito, pero opcional: la app funciona sin él

---

# VERIFICACIÓN FINAL

Antes de considerar completa la implementación, verificar:

✅ La app funciona sin GitHub CLI instalado (no crashea)
✅ La app funciona sin configurar sync (modo local)
✅ Sync funciona en Windows y Termux
✅ Conflictos se manejan sin perder datos
✅ Mensajes de error son claros y accionables
✅ Documentación está actualizada
✅ No hay credenciales hardcodeadas
✅ .notez-sync.json está en .gitignore
✅ El repo de la app y el repo de notas están separados
✅ Todos los comandos tienen --help descriptivo
```