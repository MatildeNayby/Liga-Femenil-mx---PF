# conexion_y_dataframes.py
import pandas as pd
from pymongo import MongoClient

# Nos conectamos a la BDD de Mongo
mongo_client = MongoClient('mongodb://localhost:27017/')
db_name = 'BddJornadas_MX2023'
mongo_db = mongo_client[db_name]

# Convertimos los datos a DATAFRAME
def conexion(ntabla, columnas=[]):
    tablas = mongo_db[ntabla]
    losdatos = list(tablas.find())
    df = pd.DataFrame(losdatos)
    for col in columnas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            print(f"Hay un error la  '{col}' no existe en la tabla '{ntabla}'")
    df['_id'] = df['_id'].astype(str)
    return df

# Cargamos los datos de las colecciones
df_jornadas = conexion('jornadas', ['JJ', 'JG', 'JE', 'JP', 'GF', 'GC',
                                    'DG', 'PTS', 'Jornada'])
df_pg_jornada = conexion('pg_jornada', ['PTS_Ganados', 'Jornada'])
df_progreso_por_jornada = conexion('progreso_por_jornada', ['Jornada', 'Juegos Ganados'])

df_sorted = df_jornadas.sort_values(by='PTS', ascending=False)
df_jornada_17 = df_jornadas[df_jornadas['Jornada'] == 17].sort_values(by='PTS', ascending=False)
df_jornada_17 = df_jornada_17.drop(columns=['_id', 'Posición', 'Jornada'])
df_main = df_jornadas.drop(columns=['_id', 'Posición'])

# Hacemos que la tabla solo agarre los 5 datos de la tabla con HEAD
top_5_teams = df_sorted.drop_duplicates(subset=['Equipo']).head(5)