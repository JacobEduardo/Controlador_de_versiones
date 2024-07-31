from colorama import init, Fore, Style
import sys
import time
from util import (
    reemplazar_palabra_en_archivo,
    leer_variable_desde_archivo,
    sobrescribir_linea_en_archivo,
    agregar_commit,
    es_version_valida,
    leer_y_imprimir_archivo
)
from modf import (
    sobre_escribir_registros,
    generar_registro_de_commit,
    leer_linea_con_version,
    obtener_cambios_en_version,
    obtener_registros_guardadas,
    obtener_registros_actuales
)

init(autoreset=True)

ARCHIVOS_JAVASCRIPT = ['web/index.js', 'web/sub/pagina.js']
ARCHIVOS_HTML = ['web/index.html', 'web/sub/pagina.html']
RUTA_WEB = 'web/'
RUTA_REGISTROS_DE_VERSION = 'registros_de_commit.txt'

def mostrar_version_actual():
    version_actual = leer_variable_desde_archivo(1, "versiones")
    version_actual_en_archivos = leer_variable_desde_archivo(2, "versiones")
    print(Fore.YELLOW + f"\nVersión actual: {version_actual}" + Style.RESET_ALL)
    return version_actual, version_actual_en_archivos

def procesar_actualizacion(version_actual, version_actual_en_archivos):
    while True:
        nueva_version = input(Style.RESET_ALL + "Introduce la nueva versión: " + Fore.YELLOW)
        if es_version_valida(version_actual, nueva_version):
            break
        else:
            print(Fore.RED + f"La versión {nueva_version} no es válida. Por favor, introduce una versión mayor que {version_actual}." + Style.RESET_ALL)
    
    while True:
        comentario = input(Style.RESET_ALL + "Agrega un comentario: \n" + Fore.CYAN)
        if comentario != '':
            break
        else:
            print(Fore.RED + "Ingrese un comentario válido." + Style.RESET_ALL) 
    
    while True:
        forzar = input(Style.RESET_ALL + "¿Desea forzar la actualización? Inserte 'si' o 'no': " + Fore.YELLOW)
        if forzar == 'si' or forzar == 'no':
            break
        else:
            print(Fore.RED + "Ingrese una opción válida." + Style.RESET_ALL) 
    
    while True:   
        confirmar = input(Style.RESET_ALL + "Inserte 'confirmar' para cambiar versión o 'no' para cancelar: " + Fore.YELLOW)
        if confirmar == 'confirmar' or confirmar == 'no':
            break
        else:
            print(Fore.RED + "Ingrese una opción válida." + Style.RESET_ALL) 

    if confirmar == 'confirmar':
        cantidad_de_cambios = generar_registro_de_commit(nueva_version, 'modified.txt', RUTA_WEB, RUTA_REGISTROS_DE_VERSION, comentario)
        agregar_commit('commit.txt', comentario, nueva_version,cantidad_de_cambios)

        if forzar == 'si':
            n = 0
            for archivo in ARCHIVOS_HTML:
                reemplazar_palabra_en_archivo(archivo, "App." + version_actual_en_archivos, "App." + nueva_version)
                n += 1
            print(Fore.GREEN + f"Se modificó la versión en {n} archivos HTML." + Style.RESET_ALL)

            n = 0
            for archivo in ARCHIVOS_JAVASCRIPT:
                reemplazar_palabra_en_archivo(archivo, "v=" + version_actual_en_archivos, "v=" + nueva_version)
                n += 1
            print(Fore.GREEN + f"Se modificó la versión en {n} archivos JavaScript." + Style.RESET_ALL)

            sobrescribir_linea_en_archivo(2, nueva_version, "versiones")

        sobrescribir_linea_en_archivo(1, nueva_version, "versiones")
        sobre_escribir_registros('modified.txt', RUTA_WEB)

def procesar_chequeo(solicitud):
    version = solicitud.split("chequear ")[1].strip()
    try:
        registro = leer_linea_con_version(RUTA_REGISTROS_DE_VERSION, version)
        registro = registro.split(';')
        for i, elemento in enumerate(registro):
            if i == 0:
                print(Fore.LIGHTWHITE_EX + f"\n{elemento}" + Style.RESET_ALL)
            elif i == 1:
                print(Fore.LIGHTWHITE_EX + f"{elemento}" + Style.RESET_ALL)
            elif i == 2:
                print(Fore.CYAN + f"{elemento}" + Style.RESET_ALL)
            else:
                if "Archivo Agregado" in elemento:
                    print(Fore.GREEN + f"{elemento}" + Style.RESET_ALL)
                elif "Archivo Eliminado" in elemento:
                    print(Fore.RED + f"{elemento}" + Style.RESET_ALL)
                elif "Modificado" in elemento:
                    print(Fore.WHITE + f"{elemento}" + Style.RESET_ALL)
                else:
                    print(Fore.WHITE + f"{elemento}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "La versión ingresada no es válida o no tiene registros." + Style.RESET_ALL)

def main():
    while True:
        version_actual, version_actual_en_archivos = mostrar_version_actual()
        solicitud = input("Inserte 'actualizar', 'chequear', 'chequear X.X.X' o 'salir': " + Fore.YELLOW)

        if solicitud == 'chequear':
            leer_y_imprimir_archivo('commit.txt')
        elif solicitud.startswith("chequear "):
            procesar_chequeo(solicitud)
        elif solicitud == 'actualizar':
            procesar_actualizacion(version_actual, version_actual_en_archivos)
        elif solicitud == 'salir':
            print(Fore.GREEN + "Saliendo del programa..." + Style.RESET_ALL)
            time.sleep(1) 
            sys.exit(0)
            break
        elif solicitud == 'cambios':
            registros_guardadas = obtener_registros_guardadas('modified.txt')
            registros_actuales = obtener_registros_actuales(RUTA_WEB)
            cambios_sin_guardar = obtener_cambios_en_version(registros_actuales, registros_guardadas)
            for registro in cambios_sin_guardar:
                if registro[0] == "Archivo Agregado:":
                    print(Fore.GREEN + f'{registro[0]} {registro[1]}' + Style.RESET_ALL)
                if registro[0] == "Archivo Eliminado:":
                    print(Fore.GREEN + f'{registro[0]} {registro[1]}' + Style.RESET_ALL)
                if registro[0] == "Modificado:":
                    print(Fore.GREEN + f'{registro[0]} {registro[1]}' + Style.RESET_ALL)
        else:
            print(Fore.RED + "Opción no válida. Por favor, inserte 'actualizar', 'chequear' o 'salir'." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
