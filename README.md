# ray-500GB

# Estructura del Dataset: `archivo_sucio_ray50MB.csv`

**Información General**
* **Volumen estimado:** ~50 MB.
* **Objetivo:** Simular datos "crudos" de un CRM heredado con baja calidad de datos para probar la robustez del pipeline de limpieza y normalización.
* **Estructura general**: El dataset se distribuye en formato de texto plano (CSV), utilizando codificación UTF-8 y la coma (,) como delimitador de columnas.

---

## 1. Estructura de Columnas

* **`id_cliente`** *(Integer)*
    * Identificador único secuencial.

* **`nombre`** *(String)*
    * Nombre y apellido del cliente (Generado sintéticamente).

* **`edad`** *(Integer)*
    * Edad del cliente (Rango 18-90).

* **`ciudad`** *(String - Categórica Sucia)*
    * Ciudad de residencia.
    * **Desafío:** El 97% son valores correctos (`Madrid`, `Barcelona`, `Sevilla`, `Valencia`). El **3%** restante contiene errores tipográficos deliberados (ej. `Mdrid`, `Barcleona`, `Valenca`) para testear algoritmos de *fuzzy matching* o diccionarios de corrección.

* **`fecha_registro`** *(String - Formato Inconsistente)*
    * Fecha de alta del cliente.
    * **Desafío:** Simula la fusión de tres bases de datos distintas con formatos incompatibles. Requiere normalización a ISO 8601.
    * **Formatos presentes:**
        * ISO: `2023-11-15`
        * Europeo: `15/01/2024`
        * US Short: `03-20-24`

---

## 2. Anomalías Inyectadas

Para efectos de la prueba técnica, el dataset contiene los siguientes defectos intencionales:

1.  **Duplicidad:** 1% de filas completamente duplicadas (para validar funciones tipo `drop_duplicates`).
2.  **Inconsistencia Temporal:** 3 formatos de fecha mezclados aleatoriamente.
3.  **Ruido en Categorías:** Errores ortográficos aleatorios en el campo `ciudad`.