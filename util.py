from datetime import datetime
from colorama import init, Fore, Style

def reemplazar_palabra_en_archivo(nombre_archivo, palabra_vieja, palabra_nueva):
    try:
        with open(nombre_archivo, 'r') as archivo:
            contenido = archivo.read()

        contenido_modificado = contenido.replace(palabra_vieja, palabra_nueva)
        
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(contenido_modificado)

    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def leer_variable_desde_archivo(line, nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            for _ in range(line - 1):
                archivo.readline()
            variable = archivo.readline().strip()
        return variable
    except Exception as e:
        print(f"Ocurrió un error al cargar la variable de version: {e}")
        return None
    
def sobrescribir_linea_en_archivo(line, nuevo_valor, nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
        if 1 <= line <= len(lineas):
            lineas[line - 1] = nuevo_valor + '\n'
            with open(nombre_archivo, 'w') as archivo:
                archivo.writelines(lineas)
    except Exception as e:
        print(f"Ocurrió un error al sobrescribir la línea en el archivo: {e}")

def agregar_commit(nombre_archivo,comentario, nueva_version):
    try:
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_a_agregar = f"{fecha_actual} - {nueva_version} - {comentario}"
        
        with open(nombre_archivo, 'a') as archivo:
            archivo.write(linea_a_agregar + '\n')
        
        print(Fore.GREEN + "Se agrego un nuevo registro: "+ Style.RESET_ALL + linea_a_agregar)
    except Exception as e:
        print(f"Ocurrió un error al agregar la línea al archivo: {e}")

def agregar_registro_commit(nombre_archivo, comentario, nueva_version,registro):
    try:
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_a_agregar = f"{nueva_version};{fecha_actual};{comentario}"

        text = ''
        for k in registro:
            text += f";{k[0]}{k[1]}"
        with open(nombre_archivo, 'a') as archivo:
            archivo.write(f"{linea_a_agregar}{text}\n")
        
    except Exception as e:
        print(f"Ocurrió un error al agregar la línea al archivo: {e}")

def es_version_valida(version_antigua, version_nueva):
    def convertir_version(version):
        return list(map(int, version.split('.')))
    
    try:
        if version_nueva.count('.') != 2:
            return False
        
        antigua = convertir_version(version_antigua)
        nueva = convertir_version(version_nueva)

        if nueva > antigua:
            return True
        else:
            return False
    except ValueError:
        return False

def leer_y_imprimir_archivo(nombre_archivo):
    contenido = leer_archivo(nombre_archivo)
    imprimir_por_consola(contenido)

def leer_archivo (nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            return archivo.readlines()
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
    except IOError:
        print(f"Ocurrió un error al leer el archivo {nombre_archivo}.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def imprimir_por_consola(contenido):
    colores = [Fore.WHITE, Fore.LIGHTBLACK_EX]
    
    for i, linea in enumerate(contenido):
        color = colores[i % len(colores)]
        print(color + linea.strip() + Style.RESET_ALL)

def sobre_escribir_archivo(nombre_archivo,nuevo_contenido):
    try:
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(nuevo_contenido)
    except Exception as e:
        print(f"Ocurrió un error al sobrescribir el archivo {nombre_archivo}: {e}")

def es_version_valida2(version):
    partes = version.split('.')
    if len(partes) == 3 and all(p.isdigit() for p in partes):
        return True
    return False