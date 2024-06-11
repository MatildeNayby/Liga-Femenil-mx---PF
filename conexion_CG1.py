import csv
from pymongo import MongoClient

# Conectar a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')

# Nombre de la base de datos
db_name = 'BddJornadas_MX2023'

# Eliminar la base de datos si ya existe
if db_name in mongo_client.list_database_names():
    mongo_client.drop_database(db_name)
    print(f"La base de datos '{db_name}' ha sido eliminada.")

# Crear la base de datos
mongo_db = mongo_client[db_name]

# Función para cargar un CSV a una colección de MongoDB
def cargar_csv_a_mongo(archivo_csv, nombre_coleccion, hileras):
    collection = mongo_db[nombre_coleccion]
    with open(archivo_csv, 'r') as archivocsv:
        lectordedatos = csv.DictReader(archivocsv)

        print(f"Columnas en el archivo CSV '{archivo_csv}':", lectordedatos.fieldnames)

        for each in lectordedatos:
            filas = {}
            for campos in hileras:
                if campos in each:
                    filas[campos] = each[campos]
                else:
                    print(f"Advertencia: '{campos}' no encontrado en el archivo CSV.")
                    filas[campos] = None
            print(filas)
            collection.insert_one(filas)

# Definir los archivos y sus hileras respectivas
archivos_y_hileras = [
    ('Jornadas_2023.csv', 'jornadas', ['Posición', 'Equipo', 'JJ', 'JG', 'JE', 'JP', 'GF', 'GC', 'DG', 'PTS', 'Jornada', 'Id_Jornadas']),
    ('PG_Jornada.csv', 'pg_jornada', ['Id', 'Id_Equipo', 'PTS_Ganados', 'Jornada']),
    ('Progreso_porJornada.csv', 'progreso_por_jornada', ['Equipo', 'Jornada', 'Juegos Jugados', 'Juegos Ganados', 'Juegos Empatados', 'Juegos Perdidos', 'Id'])
]

# Cargar cada archivo CSV a su respectiva colección en MongoDB
for archivo_csv, nombre_coleccion, hileras in archivos_y_hileras:
    cargar_csv_a_mongo(archivo_csv, nombre_coleccion, hileras)

print("Colecciones en la base de datos MongoDB:")
print(mongo_db.list_collection_names())

# Mostrar el contenido de cada colección
for nombre_coleccion in mongo_db.list_collection_names():
    collection = mongo_db[nombre_coleccion]
    print(f"\nContenido de la colección '{nombre_coleccion}':")
    for document in collection.find():
        print(document)

# Cerrar la conexión
mongo_client.close()
