import sqlite3
import time
import random
import string

def setup_database():
    conn = sqlite3.connect('tokens.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tokens (
                        token VARCHAR(255) PRIMARY KEY,
                        last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
                        status TEXT)''')
    conn.commit()
    return conn, cursor

def generate_random_token(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def populate_database(cursor, count=1000000):
    cursor.execute("DELETE FROM tokens")
    for _ in range(count):
        token = generate_random_token()
        cursor.execute("INSERT INTO tokens (token, status) VALUES (?, ?)", (token, 'active'))
    cursor.connection.commit()

def load_hash_table(cursor):
  """
  Carga los tokens desde la base de datos SQLite en una tabla hash.

  Args:
      cursor (sqlite3.Cursor): Cursor conectado a la base de datos SQLite.

  Returns:
      set: Conjunto de tokens cargados desde la tabla 'tokens'.
  """
  # Ejecuta una consulta SQL para obtener todos los tokens de la base de datos
  cursor.execute("SELECT token FROM tokens")
  
  # Convierte los resultados de la consulta en un conjunto para una búsqueda eficiente
  tokens_set = set()
  for row in cursor.fetchall():
      tokens_set.add(row[0])
  
  return tokens_set

def query_sqlite(cursor, token):
    start = time.perf_counter()
    cursor.execute("SELECT 1 FROM tokens WHERE token = ?", (token,))
    result = cursor.fetchone()
    elapsed = time.perf_counter() - start
    return result is not None, elapsed

def query_hash_table(hash_table, token):
    start = time.perf_counter()
    result = token in hash_table
    elapsed = time.perf_counter() - start
    return result, elapsed

def performance_test(cursor, hash_table, num_queries=10000):
    tokens = list(hash_table)
    sqlite_times, hash_times = [], []
    for _ in range(num_queries):
        token = random.choice(tokens)
        _, sqlite_time = query_sqlite(cursor, token)
        _, hash_time = query_hash_table(hash_table, token)
        sqlite_times.append(sqlite_time)
        hash_times.append(hash_time)
    return sum(sqlite_times) / num_queries, sum(hash_times) / num_queries

def main():
    conn, cursor = setup_database()
    populate_database(cursor, count=1000000)
    print("Cargando tabla hash...")
    hash_table = load_hash_table(cursor)
    print(f"Tabla hash cargada con {len(hash_table)} registros.")
    print("Iniciando prueba de rendimiento...")
    sqlite_avg, hash_avg = performance_test(cursor, hash_table, num_queries=10000)
    print(f"SQLite promedio: {sqlite_avg:.6f} segundos")
    print(f"Hash Table promedio: {hash_avg:.6f} segundos")
    conn.close()

if __name__ == "__main__":
    main()