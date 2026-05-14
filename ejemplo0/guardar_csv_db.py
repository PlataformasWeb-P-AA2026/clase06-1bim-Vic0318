import sqlite3
import csv
import os

def guardar_csv_en_db():
    # Buscar la base de datos
    ruta_db = 'base_ejemplo.db'
    if not os.path.exists(ruta_db):
        ruta_db = os.path.join(os.path.dirname(__file__), '..', 'base_ejemplo.db')
        
    # Buscar el CSV en la carpeta data
    ruta_csv = os.path.join(os.path.dirname(__file__), 'data', 'info.csv')
    
    if not os.path.exists(ruta_csv):
        print(f"No se encontró el archivo CSV en: {ruta_csv}")
        return
        
    if not os.path.exists(ruta_db):
        print(f"No se encontró la base de datos en: {ruta_db}")
        return

    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()
        
        with open(ruta_csv, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            
            registros_insertados = 0
            
            for fila in lector:
                nombre = fila.get('nombre', '')
                apellido = fila.get('apellido', '')
                cedula = fila.get('cedula', '')
                edad_str = fila.get('edad', '0')
                
                try:
                    edad = int(edad_str)
                except ValueError:
                    edad = 0
                
                # Crear la sentencia SQL de inserción
                cadena_sql = """INSERT INTO Autor (nombre, apellido, cedula, edad) \
VALUES ('%s', '%s', '%s', %d);""" % (nombre, apellido, cedula, edad)
                
                # Ejecutar la inserción
                cursor.execute(cadena_sql)
                registros_insertados += 1
                
        # Confirmar los cambios
        conn.commit()
        print(f"¡Éxito! Se han insertado {registros_insertados} registros desde el CSV a la tabla 'Autor' en la base de datos.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error durante el proceso: {e}")

if __name__ == '__main__':
    guardar_csv_en_db()
