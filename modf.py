import os
from datetime import datetime
from colorama import init, Fore, Style
from util import leer_archivo, sobre_escribir_archivo,agregar_registro_commit

def obtener_registros_actuales(ruta):
    fechas_modificaciones = []
    for carpeta_raiz, _, archivos in os.walk(ruta):
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta_raiz, archivo)
            timestamp = os.path.getmtime(ruta_completa)
            ruta_completa = ruta_completa.replace(ruta, '', 1)
            fecha_modificacion = datetime.fromtimestamp(timestamp)
            fechas_modificaciones.append({
                'ruta_completa': ruta_completa,
                'fecha_modificacion': fecha_modificacion
            })
    return fechas_modificaciones

def comparar_actuales_vs_guardados(registros_actuales,registros_guardadas):
    diferencia = []
    for registro_actual in registros_actuales:
        estado = ''
        for registro_guardado in registros_guardadas:
            if registro_actual['ruta_completa'] == registro_guardado['ruta_completa']:
                if registro_actual['fecha_modificacion'] == registro_guardado['fecha_modificacion']:
                    estado = 'archivo sin modificar.'
                    break
                else:
                    estado = 'archivo modificado.'
                    diferencia.append(('Modificado:',registro_actual['ruta_completa']))
                    break
        if estado == '':
            diferencia.append(('Archivo Agregado:',registro_actual['ruta_completa']))
    return diferencia
    
def comparar_guardados_vs_actuales(registros_guardadas,registros_actuales):
    diferencia = []
    archivos_actuales = set(archivo['ruta_completa'] for archivo in registros_actuales)
    
    for archivo_guardado in registros_guardadas:
        if archivo_guardado['ruta_completa'] not in archivos_actuales:
            diferencia.append(('Archivo Eliminado:', archivo_guardado['ruta_completa']))
            
    return diferencia

def obtener_cambios_en_version(fechas_modificaciones, fechas_guardadas):
    cambios_y_agregados = comparar_actuales_vs_guardados(fechas_modificaciones,fechas_guardadas)
    eliminados = comparar_guardados_vs_actuales(fechas_guardadas,fechas_modificaciones)
    cambios_de_version = cambios_y_agregados + eliminados
    return cambios_de_version

def obtener_registros_guardadas(ruta):
    fechas_modificaciones = []
    fechas_guardadas = leer_archivo(ruta)
    for linea in fechas_guardadas:
        try:
            ruta_completa, fecha_str = linea.strip().split(' - ')
            try:
                fecha_modificacion = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                fecha_modificacion = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
            fechas_modificaciones.append({
                'ruta_completa': ruta_completa,
                'fecha_modificacion': fecha_modificacion
            })
        except ValueError as e:
            print(f"Ocurrió un error al procesar el registro '{linea.strip()}': {e}")
    return fechas_modificaciones

def sobre_escribir_registros(ruta_guardados,ruta_web):
    text = ''
    registros_actuales = obtener_registros_actuales(ruta_web)
    for registro in registros_actuales:
        text += f"{registro['ruta_completa']} - {registro['fecha_modificacion']}\n"
    sobre_escribir_archivo(ruta_guardados,text)

def generar_registro_de_commit(nueva_version, ruta_guardados,ruta_web,ruta_registro_commit,commit):
    registros_guardadas = obtener_registros_guardadas(ruta_guardados)
    registros_actuales = obtener_registros_actuales(ruta_web)
    cambios = obtener_cambios_en_version(registros_actuales, registros_guardadas) 
    if(len(cambios)<1):
        print(Fore.LIGHTMAGENTA_EX +f"Sin cambios en archivos"+ Style.RESET_ALL)
    else:
        print(Fore.LIGHTMAGENTA_EX + f"La actualizacion modificó {len(cambios)} archivos"+ Style.RESET_ALL)
    agregar_registro_commit(ruta_registro_commit,commit,nueva_version,cambios)
    return len(cambios)

def leer_linea_con_version(nombre_archivo, version_buscada):
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                if version_buscada in linea:
                    return linea.strip()
        return None
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
    except IOError:
        print(f"Ocurrió un error al leer el archivo {nombre_archivo}.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None