import sys
import subprocess
import importlib

# ==========================================
# PASO 0: PREPARAR LA COCINA (INSTALACIÓN)
# ==========================================
# Antes de empezar a cocinar, necesitamos asegurarnos de tener los ingredientes.
# Esta función revisa si tu ordenador tiene las librerías necesarias.
# Si no las tiene, las descarga e instala automáticamente.
def verificar_e_instalar_librerias():
    requeridas = ["pandas", "numpy", "faker"] # Lista de herramientas necesarias
    necesita_reinicio = False
    
    for libreria in requeridas:
        try:
            importlib.import_module(libreria) # Intenta usar la herramienta
        except ImportError:
            # Si falla, es que no la tienes. El programa intenta instalarla por ti.
            print(f"    [AVISO] No encontré '{libreria}'. Instalándola ahora...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])
                necesita_reinicio = True
            except:
                # Si esto falla, el programa se detiene para evitar errores peores.
                sys.exit(1)
    
    if necesita_reinicio: print("--> [SISTEMA] Herramientas instaladas y listas.")

# Ejecutamos la verificación antes de nada
verificar_e_instalar_librerias()

# ==========================================
# PASO 1: TRAER LAS HERRAMIENTAS
# ==========================================
import pandas as pd     # Es como el Excel de Python. Maneja tablas gigantes.
import numpy as np      # Una calculadora superrápida para listas de números.
from faker import Faker # Un "actor" que se inventa nombres, emails y direcciones falsas.
import random           # Sirve para tirar dados y elegir cosas al azar.
import os               # Nos deja ver cosas del sistema, como cuánto pesa un archivo.

# ==========================================
# PASO 2: CONFIGURACIÓN (LOS MANDOS)
# ==========================================
FILENAME = "archivo_sucio_ray50MB.csv" # Nombre del archivo que vamos a crear
OBJETIVO_MB = 50 

# Las computadoras miden el peso en Bytes.
# 1 Megabyte = 1024 Kilobytes. 1 Kilobyte = 1024 Bytes.
# Multiplicamos para saber cuántos bytes son 50MB exactos.
BYTES_EXACTOS = OBJETIVO_MB * 1024 * 1024 # Total: 52,428,800 bytes

# ESTRATEGIA PARA EL PESO EXACTO:
# Es muy difícil calcular cuántas filas necesitamos para llegar justo a 50MB.
# TRUCO: Generamos un poco MENOS (780.000 filas) y luego rellenamos lo que falte
# con espacios en blanco invisibles al final del archivo.
FILAS_BASE = 780_000 

# CONFIGURACIÓN DE LA "SUCIEDAD" (ERRORES A PROPÓSITO):
ERROR_RATE_CITIES = 0.03 # El 3% de las ciudades estarán mal escritas (para practicar corrección).
DUPLICATE_RATE = 0.01    # El 1% de los clientes estarán repetidos (para practicar deduplicación).

# SEMILLA (SEED):
# Esto sirve para "congelar el azar". Si pones seed(42), los números aleatorios
# serán siempre los mismos cada vez que ejecutes el programa.
# Útil para que al profesor le salga el mismo resultado que a ti.
fake = Faker('es_ES') # Configuramos al inventor de nombres en Español de España
np.random.seed(42)    
random.seed(42)

def generar_dataset_final():
    print(f"--> Generando {FILAS_BASE} filas de datos falsos. Esto puede tardar un poco...")

    # A. CREAR IDs (DNI o Identificador)
    # Crea una lista de números del 100 al 780.100 de golpe.
    ids = np.arange(100, 100 + FILAS_BASE)
    
    # B. CREAR EDADES
    # Genera 780.000 números al azar entre 18 y 90.
    edades = np.random.randint(18, 90, size=FILAS_BASE)
    
    # C. CREAR NOMBRES ÚNICOS (Garantizado sin repetidos)
    # Imagina que tienes que invitar a 780.000 personas distintas a una fiesta.
    # Usamos un 'set' (conjunto), que es una bolsa mágica en Python que elimina duplicados automáticamente.
    nombres_unicos = set() 
    
    # Seguimos inventando nombres hasta llenar la lista.
    while len(nombres_unicos) < FILAS_BASE:
        faltan = FILAS_BASE - len(nombres_unicos)
        # Pedimos a Faker que invente los nombres que faltan
        nuevos_nombres = [fake.name() for _ in range(faltan)]
        # Los metemos en la bolsa (si alguno estaba repe, el set lo borra solo)
        nombres_unicos.update(nuevos_nombres)

    # Convertimos la bolsa en una lista ordenada para poder usarla en la tabla
    nombres = list(nombres_unicos)

    # D. CIUDADES Y ERRORES DE ORTOGRAFÍA
    ciudades_limpias = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla']
    
    # Diccionario de errores: Si toca Madrid, a veces escribiremos 'Mdrid'.
    typos_map = {
        'Madrid': ['Mdrid', 'Madird'], 
        'Barcelona': ['Barcleona', 'Brcelona'],
        'Valencia': ['Valenca', 'Vlencia'], 
        'Sevilla': ['Svilla', 'Sevila']
    }
    
    # 1. Asignamos ciudades bien escritas a todo el mundo.
    # (Madrid sale más veces (35%) que Sevilla (15%))
    col_ciudades = np.random.choice(ciudades_limpias, size=FILAS_BASE, p=[0.35, 0.3, 0.2, 0.15])
    
    # 2. Elegimos al azar a las "víctimas" (el 3% de las filas).
    lista_ciudades = col_ciudades.tolist()
    num_errores = int(FILAS_BASE * ERROR_RATE_CITIES)
    indices_rotos = np.random.choice(FILAS_BASE, size=num_errores, replace=False)
    
    # 3. Vamos fila por fila (solo las elegidas) y cambiamos el nombre bueno por uno malo.
    for i in indices_rotos:
        ciudad_real = lista_ciudades[i] # Mira qué ciudad es (ej: Madrid)
        lista_ciudades[i] = random.choice(typos_map[ciudad_real]) # La cambia por una mala (ej: Mdrid)

    # E. FECHAS (CAOS DE FORMATOS)
    # En la vida real, cada persona escribe la fecha como quiere. Simulamos eso.
    # Primero generamos fechas válidas de los últimos 2 años.
    fechas_raw = [fake.date_between(start_date='-2y', end_date='today') for _ in range(FILAS_BASE)]
    fechas_fmt = []
    
    # Tiramos un dado para decidir cómo escribir cada fecha.
    for f in fechas_raw:
        r = random.random()
        if r < 0.33: fechas_fmt.append(f.strftime('%Y-%m-%d'))   # Formato Internacional (2024-01-30)
        elif r < 0.66: fechas_fmt.append(f.strftime('%d/%m/%Y')) # Formato Español (30/01/2024)
        else: fechas_fmt.append(f.strftime('%m-%d-%y'))          # Formato USA (01-30-24)

    # F. MONTAR LA TABLA (DATAFRAME)
    # Juntamos todas las columnas que hemos creado en una sola tabla.
    df = pd.DataFrame({
        'id_cliente': ids,
        'nombre': nombres,
        'edad': edades,
        'ciudad': lista_ciudades,
        'fecha_registro': fechas_fmt
    })

    # G. DUPLICADOS Y ORDEN
    # Cogemos una muestra aleatoria (1%) y la pegamos al final de la tabla.
    # Así simulamos que se han metido datos repetidos por error.
    df_duplicados = df.sample(frac=DUPLICATE_RATE)
    df_final = pd.concat([df, df_duplicados], ignore_index=True)
    
    # Ordenamos por ID para que los duplicados queden cerca de los originales.
    df_final = df_final.sort_values(by='id_cliente')

    # H. GUARDAR EL ARCHIVO INICIAL
    df_final.to_csv(FILENAME, index=False)

    # ==========================================
    # PASO 3: EL AJUSTE PERFECTO (PADDING)
    # ==========================================
    # Aquí hacemos la magia para que el archivo pese 50.00 MB clavados.
    
    size_actual = os.path.getsize(FILENAME) # Pesamos el archivo actual
    diferencia = BYTES_EXACTOS - size_actual # Calculamos cuánto falta

    if diferencia < 0:
        print(f"    [ERROR] ¡Nos pasamos! El archivo pesa demasiado. Reduce FILAS_BASE.")
    else:
        # Si falta peso, abrimos el archivo y le añadimos espacios en blanco al final.
        # Es como rellenar una caja con papel de burbujas para que ajuste bien.
        with open(FILENAME, 'ab') as f:
            f.write(b' ' * diferencia)

    # REPORTE FINAL
    size_final = os.path.getsize(FILENAME)
    print(f"--> ¡LISTO! Archivo generado: {FILENAME}")
    print(f"--> Peso Final: {size_final / (1024*1024):.2f} MB")
    print(f"--> Total de filas: {len(df_final):,} (incluyendo duplicados)")
    print("Primeras filas (Ordenadas):")
    print(df_final.head(5))
# Esta línea le dice a Python: "Si ejecutas este archivo, arranca la función generar_dataset_final"
if __name__ == "__main__":
    generar_dataset_final()