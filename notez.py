#!/usr/bin/env python3
"""
noteZ - CLI minimalista para notas incrementales rápidas y continuas
Funciona en Windows PowerShell 7 y Termux Android con detección automática de plataforma.

Autor: partybrasil
Versión: 1.0.0-FUSION
Compatibilidad: Python 3.x
Plataformas: Windows PowerShell 7 + Android Termux
"""

import sys
import os
import argparse
from datetime import datetime


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
  
Comandos durante grabación:
  /n      Línea vacía
  /n=     Separador decorativo
  /r      Leer notas (modo lectura temporal)
  /h      Ayuda
  /q      Salir
        """
    )
    
    parser.add_argument(
        '-r', '--read',
        action='store_true',
        help='Inicia modo lectura de notas guardadas'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='noteZ 1.0.0-FUSION'
    )
    
    args = parser.parse_args()
    
    # Obtener ruta del archivo según la plataforma
    notes_file = get_path()
    
    try:
        if args.read:
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