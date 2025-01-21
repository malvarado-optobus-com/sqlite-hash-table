# Requerimientos y Configuración para la Evaluación de SQLite y una tabla hash

Este repositorio contiene los archivos necesarios para replicar una prueba de concepto que evalúa el rendimiento entre una base de datos SQLite y una tabla hash en Python. El propósito es medir la eficiencia y escalabilidad de ambas estructuras al manejar hasta un millón de tokens.

---

## Propósito

Esta prueba permite cuantificar y comparar el rendimiento de SQLite y una tabla hash en operaciones de consulta y actualización dinámica. Los resultados sirven como referencia para desarrollar soluciones que requieran sincronización de datos y alta persistencia en entornos embebidos.

---

## Requerimientos

### 1. **Estructura de los Datos**

- **Token:** Identificador alfanumérico único de 16 caracteres (`VARCHAR`).
- **Fecha de Modificación:** Registro temporal de última actualización (`DATETIME`).
- **Estado:** Indica si el token está "activo" o "inactivo" (`TEXT`).

### 2. **Operaciones Principales**

- Consultas ejecutadas cada 5 segundos.
- Actualizaciones dinámicas, incluyendo inserciones y eliminaciones sincronizadas en SQLite y la tabla hash.
- Persistencia de datos garantizada mediante SQLite.

### 3. **Escalabilidad**

- Volumen máximo: 1 millón de registros.

### 4. **Entorno del Sistema**

- **Dispositivo:** Lector Feig cVEND plug flex II.
- **Lenguaje:** Python en sistemas Windows.
- **Bibliotecas Utilizadas:** Todas las bibliotecas son estándar de Python.

---

## Solución Técnica

### 1. **Base de Datos SQLite**

- Diseño de tabla optimizado:

  ```sql
  CREATE TABLE tokens (
      token VARCHAR(255) PRIMARY KEY,
      last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
      status TEXT
  );
  ```

### 2. **Tabla Hash en Python**

- Implementada utilizando un `set`, proporcionando accesos rápidos para consultas en memoria.

### 3. **Sincronización entre SQLite y la Tabla Hash**

Se implementan los siguientes pasos para garantizar la consistencia de datos:

- **Carga Inicial:** Los datos existentes en SQLite se transfieren completamente a la tabla hash al iniciar.
- **Sincronización Dinámica:** Inserciones y eliminaciones se reflejan simultáneamente en ambas estructuras.
- **Validación de Consultas:** Cada consulta verifica la existencia de un token en ambas estructuras.
- **Actualización Continua:** Cambios realizados durante la ejecución del sistema se aplican en tiempo real para mantener la integridad de los datos.

---

## Configuración del Entorno

### 1. **Instalación de Python**

Descarga Python desde [python.org](https://www.python.org/downloads/) y selecciona la opción "Add Python to PATH" durante la instalación. Verifica la instalación:

```bash
python --version
```

### 2. **Creación de un Entorno Virtual**

- Navega al directorio del proyecto:
  ```bash
  cd /ruta/a/tu/proyecto
  ```
- Crea y activa un entorno virtual:
  - **Windows:**
    ```bash
    python -m venv env
    env\Scripts\activate
    ```
  - **Linux/macOS:**
    ```bash
    python -m venv env
    source env/bin/activate
    ```

### 3. **Ejecución del Código**

El archivo principal es `test_sqlite_vs_hash.py`. El script realiza lo siguiente:

- Configura la base de datos SQLite.
- Genera un millón de registros simulados.
- Carga los tokens en una tabla hash en memoria.
- Realiza pruebas de rendimiento para comparar los tiempos promedio de consulta en ambas estructuras.

Ejecuta el script con:

```bash
python test_sqlite_vs_hash.py
```

---

## Comentarios sobre los Métodos

1. **setup_database:** Configura la base de datos SQLite creando la tabla `tokens` si no existe.
2. **generate_random_token:** Genera tokens alfanuméricos aleatorios para simular datos reales.
3. **populate_database:** Llena la base de datos con un número específico de registros aleatorios.
4. **load_hash_table:** Carga todos los tokens de SQLite en un conjunto (`set`) para consultas rápidas en memoria.
5. **query_sqlite:** Consulta SQLite para verificar si un token existe y mide el tiempo necesario.
6. **query_hash_table:** Verifica la existencia de un token en la tabla hash y mide el tiempo necesario.
7. **performance_test:** Realiza consultas múltiples en ambas estructuras y calcula tiempos promedio.
8. **main:** Es el flujo principal que configura todo, ejecuta las pruebas y muestra los resultados.

---

## Resultados

### 1. **Rendimiento**

- **SQLite:** Tiempo promedio por consulta ~5-10 ms.
- **Tabla Hash:** Tiempo promedio por consulta ~0.01-0.05 ms.

### 2. **Escalabilidad**

- La tabla hash mantiene un rendimiento constante incluso con un millón de registros.

### C++

La implementación en C++ utiliza una simulación de base de datos en memoria (`SimulatedDatabase`) en lugar de una conexión real a SQLite. Este enfoque permite ejecutar la prueba de concepto sin dependencias externas.

#### Comentarios sobre el Código

1. **SimulatedDatabase:**
   - Simula una base de datos en memoria utilizando un `std::unordered_set` para almacenar tokens.
   - Métodos principales:
     - `insert`: Inserta un token en la base de datos simulada.
     - `exists`: Verifica si un token existe en la base de datos.
     - `clear`: Limpia todos los registros.
     - `getAllTokens`: Retorna todos los tokens almacenados.

2. **generateRandomToken:**
   - Genera un token aleatorio de longitud fija utilizando caracteres alfanuméricos.
   - Emplea `std::random_device` y `std::mt19937` para garantizar aleatoriedad.

3. **populateDatabase:**
   - Llena la base de datos simulada con un número definido de tokens aleatorios.
   - Garantiza una base limpia antes de cada prueba al usar `clear`.

4. **loadHashTable:**
   - Carga todos los tokens de la base de datos simulada a una tabla hash (`std::unordered_set`).
   - Permite consultas rápidas en memoria.

5. **queryHashTable:**
   - Consulta la tabla hash para verificar si un token existe.
   - Mide el tiempo necesario utilizando `std::chrono`.

6. **queryDatabase:**
   - Consulta la base de datos simulada para verificar si un token existe.
   - También mide el tiempo necesario con `std::chrono`.

7. **performanceTest:**
   - Realiza consultas aleatorias tanto en la base de datos simulada como en la tabla hash.
   - Calcula los tiempos promedio para cada estructura.

8. **main:**
   - Controla el flujo principal de la prueba:
     1. Llena la base de datos simulada con un millón de registros.
     2. Carga los tokens en la tabla hash.
     3. Ejecuta las pruebas de rendimiento y muestra los resultados.

#### Ejecución

Puede probar este código en entornos online como [https://onlinegdb.com/JUg0Yf8iH]. Simplemente ingrese al link anterior.



---

## Conclusión

Esta prueba de concepto demuestra que las tablas hash son significativamente más rápidas que SQLite para consultas frecuentes. Sin embargo, SQLite sigue siendo esencial para la persistencia de datos. Este repositorio proporciona una guía integral para replicar y analizar estos resultados.
