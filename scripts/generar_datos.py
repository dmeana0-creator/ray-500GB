import pandas as pd
import numpy as np
from faker import Faker
import random
import os

# 1. Configuración inicial
fake = Faker('es_ES')
np.random.seed(42)  # Semilla para reproducibilidad

# --- CONFIGURACIÓN DE RUTAS Y DIRECTORIOS ---
# Detectamos la ruta absoluta de ESTE script (dentro de 'scripts/')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construimos la ruta apuntando a la carpeta hermana '../data'
RUTA_DATA = os.path.join(BASE_DIR, '..', 'data')

# Definimos la ruta completa del archivo final
FILENAME = os.path.join(RUTA_DATA, 'archivo_sucio_ray50MB.csv')

# Crea la carpeta 'data' si no existe (robustez extra)
os.makedirs(RUTA_DATA, exist_ok=True)

# --- Constantes de Generación ---
CIUDADES_BASE = ["Madrid", "Barcelona", "Sevilla", "Valencia"]
CIUDADES_SUCIAS = {
    'Madrid': 'Mdrid',
    'Barcelona': 'Barcleona',
    'Sevilla': 'Sevia',
    'Valencia': 'Valenca'
}

def generar_datos_crm(n=850000):
    """
    Genera una lista de diccionarios con datos 'sucios' de CRM.
    n=850000 genera aprox 50MB de datos.
    """
    data = []
    
    # Pre-generamos opciones para hacerlo más rápido dentro del bucle
    formatos_fecha = ["iso", "europeo", "us"]
    
    print(f"Generando {n} registros en memoria...")
    
    id_actual = 1
    
    for _ in range(n):
        
        # --- Generación de datos con Faker y Numpy ---
        
        # Nombre (String)
        nombre = fake.name()
        
        # Edad (Integer, rango 18-90)
        edad = np.random.randint(18, 91)
        
        # Ciudad (Categórica Sucia)
        ciudad_elegida = np.random.choice(CIUDADES_BASE)
        
        # 3% de probabilidad de error tipográfico
        if np.random.random() < 0.03:
            ciudad = CIUDADES_SUCIAS.get(ciudad_elegida, ciudad_elegida)
        else:
            ciudad = ciudad_elegida
            
        # Fecha de Registro (Formato Inconsistente)
        fecha_obj = fake.date_between(start_date='-5y', end_date='today')
        formato = np.random.choice(formatos_fecha)
        
        if formato == 'iso':
            fecha_str = fecha_obj.strftime('%Y-%m-%d')
        elif formato == 'europeo':
            fecha_str = fecha_obj.strftime('%d/%m/%Y')
        else:
            fecha_str = fecha_obj.strftime('%m-%d-%y')
            
        # --- Construcción del registro ---
        registro = {
            "id_cliente": id_actual,
            "nombre": nombre,
            "edad": edad,
            "ciudad": ciudad,
            "fecha_registro": fecha_str
        }
        
        data.append(registro)
        
        # --- Anomalía: Duplicidad (1%) ---
        if np.random.random() < 0.01:
            data.append(registro)
        
        id_actual += 1

    return data

# --- Bloque Principal ---

if __name__ == "__main__":
    # Calculamos n para aprox 50MB (aprox 850k filas)
    lista_datos = generar_datos_crm(n=850000)

    print(f"Ejemplo de registro: {lista_datos[0]}")
    print(f"Guardando en: {FILENAME} ...")

    # Usamos Pandas para volcar la lista a CSV eficientemente
    df = pd.DataFrame(lista_datos)
    
    # Guardamos en la ruta construida dinámicamente
    df.to_csv(FILENAME, index=False, encoding='utf-8')

    print(f"Archivo generado exitosamente.")
    print(f"Dimensiones finales: {df.shape}")