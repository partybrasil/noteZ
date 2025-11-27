#!/usr/bin/env python3
"""
noteZ - CLI minimalista para notas incrementales rápidas y continuas
Funciona en Windows PowerShell 7 y Termux Android con detección automática de plataforma.

Autor: partybrasil
Versión: 1.1.0-FUSION
Compatibilidad: Python 3.x
Plataformas: Windows PowerShell 7 + Android Termux
"""

import sys
import os
import argparse
import shutil
from datetime import datetime


# ============================================================================
# CONFIGURACIÓN DEL MODO DUAL
# ============================================================================
# Porcentaje del terminal reservado para el panel de lectura (panel superior)
# Valor entre 0.1 (10%) y 0.9 (90%). Default: 0.80 (80%)
DUAL_READ_PANEL_RATIO = 0.80


def get_path():
    """
    Detecta la plataforma y retorna la ruta apropiada para el archivo de notas.
    
    Returns:
        str: Ruta completa al archivo notas.txt según la plataforma detectada
    """
    # Detección de Termux en Android
    if sys.platform.startswith('linux') and 'ANDROID_ROOT' in os.environ:
        notes_path = os.path.expanduser("~/notez/notas.txt")
    else:
        # Windows PowerShell 7 y otros sistemas
        notes_path = os.path.join(os.path.expanduser("~"), "notez", "notas.txt")
    
    # Crear directorio si no existe
    notes_dir = os.path.dirname(notes_path)
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir, exist_ok=True)
    
    return notes_path


def get_terminal_size():
    """
    Obtiene el tamaño actual del terminal de forma portable.
    
    Returns:
        tuple: (columnas, filas) del terminal
    """
    try:
        size = shutil.get_terminal_size(fallback=(80, 24))
        return size.columns, size.lines
    except Exception:
        return 80, 24


def clear_screen():
    """
    Limpia la pantalla del terminal de forma portable.
    Funciona en Windows y Unix/Linux/Termux.
    """
    # Usar secuencia ANSI que funciona en PowerShell 7 y Termux
    print("\033[2J\033[H", end="", flush=True)


def move_cursor(row, col=1):
    """
    Mueve el cursor a una posición específica del terminal.
    
    Args:
        row (int): Número de fila (1-indexed)
        col (int): Número de columna (1-indexed, default=1)
    """
    print(f"\033[{row};{col}H", end="", flush=True)


def clear_line():
    """
    Limpia la línea actual del cursor.
    """
    print("\033[2K", end="", flush=True)


def show_help():
    """
    Muestra el menú de ayuda básico con los comandos disponibles.
    Regresa al prompt de grabación tras mostrar la información.
    """
    help_text = """
╭─────────────────────────────────────────╮
│            noteZ - Ayuda Rápida         │
├─────────────────────────────────────────┤
│ COMANDOS ESPECIALES:                    │
│                                         │
│  /n      → Línea vacía (separador)     │
│  /n=     → Línea decorativa =====      │
│  /r      → Leer notas (modo lectura)   │
│  /h      → Mostrar esta ayuda          │
│  /q      → Salir y guardar             │
│                                         │
│ MODOS DE USO:                          │
│                                         │
│  notez           → Modo grabación      │
│  notez -r        → Modo lectura        │
│  notez --read    → Modo lectura        │
│  notez -dual     → Modo dual (split)   │
│  notez --dual    → Modo dual (split)   │
│                                         │
│ MODO DUAL:                             │
│                                         │
│  Panel superior: Notas en tiempo real  │
│  Panel inferior: Escribir nuevas notas │
│  Las notas aparecen arriba al guardar  │
│                                         │
│ TIPS:                                   │
│                                         │
│  • Cada nota se guarda con timestamp    │
│  • Ctrl+C guarda automáticamente       │
│  • Pegar texto funciona transparente   │
│                                         │
╰─────────────────────────────────────────╯

Presiona Enter para continuar...
    """.strip()
    
    print(help_text)
    input()  # Esperar Enter para continuar


def write_line(line, file_path):
    """
    Escribe una línea al archivo con timestamp automático y maneja comandos especiales.
    
    Args:
        line (str): Línea de texto a escribir o comando especial
        file_path (str): Ruta completa al archivo de notas
        
    Returns:
        str: 'quit' si debe salir (/q), 'read' si debe activar lectura (/r), 'continue' si continúa
    """
    # Manejar comandos especiales
    if line == '/q':
        # Escribir línea decorativa final y salir
        timestamp = datetime.now().strftime("[%d-%m-%Y | %H:%M]")
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} ============================ Sesión finalizada ===========================\n")
        except Exception as e:
            print(f"Error al guardar: {e}")
        return 'quit'
        
    elif line == '/r':
        # Activar modo lectura temporal
        return 'read'
        
    elif line == '/n':
        # Línea vacía como separador mínimo
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write("\n")
        except Exception as e:
            print(f"Error al guardar: {e}")
        return 'continue'
        
    elif line == '/n=':
        # Línea decorativa con separador
        timestamp = datetime.now().strftime("[%d-%m-%Y | %H:%M]")
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} ==========================================================================\n")
        except Exception as e:
            print(f"Error al guardar: {e}")
        return 'continue'
        
    elif line == '/h':
        # Mostrar ayuda y continuar
        show_help()
        return 'continue'
        
    else:
        # Línea normal de nota con timestamp
        if line.strip():  # Solo escribir si no está vacía
            timestamp = datetime.now().strftime("[%d-%m-%Y | %H:%M]")
            try:
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f"{timestamp} {line}\n")
            except Exception as e:
                print(f"Error al guardar: {e}")
        return 'continue'


def read_notes(file_path, return_to_recording=False):
    """
    Modo lectura interactivo con paginación eficiente.
    Muestra las últimas 10 líneas inicialmente, +5 por cada Enter.
    
    Args:
        file_path (str): Ruta completa al archivo de notas
        return_to_recording (bool): Si True, indica que debe volver al modo grabación al salir
    """
    if not os.path.exists(file_path):
        print("No hay notas guardadas aún. Usa 'notez' para empezar a escribir.")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        return
    
    if not all_lines:
        print("El archivo de notas está vacío.")
        return
    
    total_lines = len(all_lines)
    current_end = total_lines
    lines_per_page = 10
    lines_per_scroll = 5
    
    context_info = " (desde grabación)" if return_to_recording else ""
    print(f"\n╭── noteZ READ MODE{context_info} ── {total_lines} líneas totales ──╮")
    
    # Mostrar últimas 10 líneas inicialmente
    start_idx = max(0, current_end - lines_per_page)
    for i in range(start_idx, current_end):
        print(f"{i+1:4d} │ {all_lines[i].rstrip()}")
    
    current_end = start_idx
    
    while True:
        if current_end <= 0:
            prompt = "[noteZ READ MODE] -- Inicio del archivo -- /q para salir --"
        else:
            prompt = "[noteZ READ MODE] -- Enter para más, /q para salir --"
        
        try:
            user_input = input(f"\n{prompt} ")
            
            if user_input.strip() == '/q':
                break
            elif user_input.strip() == '/h':
                show_help()
                continue
            else:
                # Mostrar 5 líneas adicionales hacia atrás
                if current_end > 0:
                    new_start = max(0, current_end - lines_per_scroll)
                    # Preservar contexto: mostrar últimas 5 líneas anteriores también
                    context_start = max(0, min(current_end, new_start + lines_per_scroll) - lines_per_scroll)
                    
                    print()  # Línea en blanco para separación
                    for i in range(new_start, min(current_end, new_start + lines_per_scroll)):
                        print(f"{i+1:4d} │ {all_lines[i].rstrip()}")
                    
                    current_end = new_start
                else:
                    print("\n── Ya estás en el inicio del archivo ──")
                    
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
    
    if return_to_recording:
        print("\nVolviendo al modo grabación...")
    else:
        print("\nSaliendo del modo lectura...")


def render_dual_read_panel(file_path, read_lines, term_width):
    """
    Renderiza el panel de lectura para el modo dual.
    
    Args:
        file_path (str): Ruta al archivo de notas
        read_lines (int): Número de líneas disponibles para el panel de lectura
        term_width (int): Ancho del terminal
    
    Returns:
        list: Lista de líneas formateadas para mostrar
    """
    display_lines = []
    
    # Línea de encabezado
    header = "╭── noteZ DUAL MODE ── Panel de Lectura (tiempo real) ──╮"
    display_lines.append(header[:term_width])
    
    # Líneas disponibles para contenido (descontar header y separador)
    content_lines = read_lines - 2
    
    if not os.path.exists(file_path):
        display_lines.append("│ (No hay notas guardadas aún)")
        # Rellenar con líneas vacías
        for _ in range(content_lines - 1):
            display_lines.append("│")
    else:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            
            if not all_lines:
                display_lines.append("│ (El archivo está vacío)")
                for _ in range(content_lines - 1):
                    display_lines.append("│")
            else:
                # Mostrar las últimas N líneas que quepan
                total = len(all_lines)
                start_idx = max(0, total - content_lines)
                
                for i in range(start_idx, total):
                    line_content = all_lines[i].rstrip()
                    # Truncar si es muy larga
                    max_content_width = term_width - 7  # "1234 │ "
                    if len(line_content) > max_content_width:
                        line_content = line_content[:max_content_width - 3] + "..."
                    formatted_line = f"{i+1:4d} │ {line_content}"
                    display_lines.append(formatted_line[:term_width])
                
                # Rellenar con líneas vacías si no hay suficientes notas
                lines_shown = total - start_idx
                for _ in range(content_lines - lines_shown):
                    display_lines.append("│")
        except Exception:
            display_lines.append("│ (Error al leer archivo)")
            for _ in range(content_lines - 1):
                display_lines.append("│")
    
    # Línea separadora
    separator = "╰" + "─" * (term_width - 2) + "╯"
    display_lines.append(separator[:term_width])
    
    return display_lines


def run_dual_mode(file_path):
    """
    Ejecuta el modo dual con panel de lectura arriba y grabación abajo.
    El panel superior muestra las notas en tiempo real (80% del espacio).
    El panel inferior permite escribir nuevas notas (20% del espacio).
    
    Args:
        file_path (str): Ruta completa al archivo de notas
    """
    def refresh_display():
        """Refresca la pantalla completa del modo dual."""
        term_width, term_height = get_terminal_size()
        
        # Calcular líneas para el panel de lectura
        read_panel_lines = max(5, int(term_height * DUAL_READ_PANEL_RATIO))
        
        # Limpiar pantalla
        clear_screen()
        
        # Renderizar panel de lectura
        read_display = render_dual_read_panel(file_path, read_panel_lines, term_width)
        for line in read_display:
            print(line)
        
        # Línea de información del panel de escritura
        write_header = f"╭── Panel de Escritura ── /h ayuda ── /q salir ──╮"
        print(write_header[:term_width])
        
        return term_width, term_height, read_panel_lines
    
    # Mostrar pantalla inicial
    term_width, term_height, read_panel_lines = refresh_display()
    
    # Bucle principal de escritura
    while True:
        try:
            user_input = input("[noteZ DUAL] > ")
            
            # Manejar comandos especiales
            if user_input == '/q':
                # Escribir línea decorativa final y salir
                timestamp = datetime.now().strftime("[%d-%m-%Y | %H:%M]")
                try:
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f"{timestamp} ============================ Sesión finalizada ===========================\n")
                except Exception as e:
                    print(f"Error al guardar: {e}")
                clear_screen()
                print("\n¡Notas guardadas! Hasta luego.")
                break
                
            elif user_input == '/h':
                # Mostrar ayuda
                clear_screen()
                show_help()
                term_width, term_height, read_panel_lines = refresh_display()
                continue
                
            elif user_input == '/n':
                # Línea vacía como separador mínimo
                try:
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write("\n")
                except Exception as e:
                    print(f"Error al guardar: {e}")
                # Refrescar display para mostrar cambio
                term_width, term_height, read_panel_lines = refresh_display()
                continue
                
            elif user_input == '/n=':
                # Línea decorativa con separador
                timestamp = datetime.now().strftime("[%d-%m-%Y | %H:%M]")
                try:
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write(f"{timestamp} ==========================================================================\n")
                except Exception as e:
                    print(f"Error al guardar: {e}")
                # Refrescar display para mostrar cambio
                term_width, term_height, read_panel_lines = refresh_display()
                continue
                
            elif user_input == '/r':
                # En modo dual, /r no hace nada especial (ya estamos viendo las notas)
                print("(Ya estás en modo dual - las notas se muestran arriba en tiempo real)")
                continue
                
            else:
                # Línea normal de nota con timestamp
                if user_input.strip():  # Solo escribir si no está vacía
                    timestamp = datetime.now().strftime("[%d-%m-%Y | %H:%M]")
                    try:
                        with open(file_path, 'a', encoding='utf-8') as f:
                            f.write(f"{timestamp} {user_input}\n")
                    except Exception as e:
                        print(f"Error al guardar: {e}")
                    # Refrescar display para mostrar nueva nota
                    term_width, term_height, read_panel_lines = refresh_display()
                
        except KeyboardInterrupt:
            # Ctrl+C: guardar línea de cierre y salir limpiamente
            print("\n\nGuardando y cerrando...")
            timestamp = datetime.now().strftime("[%d-%m-%Y | %H:%M]")
            try:
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f"{timestamp} ========== Interrupción del usuario ==========\n")
                clear_screen()
                print("¡Notas guardadas! Hasta luego.")
            except Exception as e:
                print(f"Error al guardar: {e}")
            break
        except EOFError:
            # EOF (Ctrl+D en Unix): salir limpiamente
            clear_screen()
            print("\n\n¡Hasta luego!")
            break


def main():
    """
    Función principal que maneja argumentos y ejecuta el bucle apropiado.
    """
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description="noteZ - CLI minimalista para notas incrementales",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  notez           Modo grabación (default)
  notez -r        Modo lectura
  notez --read    Modo lectura
  notez -dual     Modo dual (split-screen)
  notez --dual    Modo dual (split-screen)
  
Comandos durante grabación:
  /n      Línea vacía
  /n=     Separador decorativo
  /r      Leer notas (modo lectura temporal)
  /h      Ayuda
  /q      Salir
  
Modo Dual:
  Panel superior (80%): Muestra notas en tiempo real
  Panel inferior (20%): Escribir nuevas notas
  Las notas aparecen arriba automáticamente al guardar
        """
    )
    
    parser.add_argument(
        '-r', '--read',
        action='store_true',
        help='Inicia modo lectura de notas guardadas'
    )
    
    parser.add_argument(
        '-dual', '--dual',
        action='store_true',
        help='Inicia modo dual: panel lectura arriba (80%%) + escritura abajo (20%%)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='noteZ 1.1.0-FUSION'
    )
    
    args = parser.parse_args()
    
    # Obtener ruta del archivo según la plataforma
    notes_file = get_path()
    
    try:
        if args.dual:
            # Modo dual: split-screen con lectura arriba y escritura abajo
            run_dual_mode(notes_file)
        elif args.read:
            # Modo lectura
            read_notes(notes_file)
        else:
            # Modo grabación (default)
            print("╭─────────────────────────────────────────╮")
            print("│     noteZ - Notas Rápidas Continuas     │")
            print("│                                         │")
            print("│  Escribe tus notas y presiona Enter     │")
            print("│  Comandos: /n /n= /r /h /q               │")
            print("│  Ctrl+C para salir seguro              │")
            print("╰─────────────────────────────────────────╯")
            print(f"\nArchivo: {notes_file}\n")
            
            # Bucle principal de grabación
            while True:
                try:
                    user_input = input("[noteZ] > ")
                    
                    # write_line retorna 'quit', 'read', o 'continue'
                    result = write_line(user_input, notes_file)
                    
                    if result == 'quit':
                        print("\n¡Notas guardadas! Hasta luego.")
                        break
                    elif result == 'read':
                        # Activar modo lectura temporal desde grabación
                        read_notes(notes_file, return_to_recording=True)
                        # Continúa con el bucle de grabación tras salir de lectura
                        continue
                    # Si result == 'continue', simplemente continúa el bucle
                        
                except KeyboardInterrupt:
                    # Ctrl+C: guardar línea de cierre y salir limpiamente
                    print("\n\nGuardando y cerrando...")
                    timestamp = datetime.now().strftime("[%d-%m-%Y | %H:%M]")
                    try:
                        with open(notes_file, 'a', encoding='utf-8') as f:
                            f.write(f"{timestamp} ========== Interrupción del usuario ==========\n")
                        print("¡Notas guardadas! Hasta luego.")
                    except Exception as e:
                        print(f"Error al guardar: {e}")
                    break
                except EOFError:
                    # EOF (Ctrl+D en Unix): salir limpiamente
                    print("\n\n¡Hasta luego!")
                    break
                    
    except Exception as e:
        print(f"Error crítico: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()