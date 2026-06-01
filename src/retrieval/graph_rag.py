import os
import csv
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Configurar rutas automáticas
RUTA_RETRIEVAL = os.path.dirname(os.path.abspath(__file__))
RUTA_SRC = os.path.dirname(RUTA_RETRIEVAL)
RAIZ_PROYECTO = os.path.dirname(RUTA_SRC)
CARPETA_DATA = os.path.join(RAIZ_PROYECTO, "data")
RUTA_ENV = os.path.join(RAIZ_PROYECTO, ".env")

# Cargar variables de entorno del archivo .env
load_dotenv(RUTA_ENV)

class GraphRAG:
    def __init__(self):
        """Inicializa la conexión con el clúster de Neo4j usando variables de entorno."""
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")
        
        if not uri or not password:
            raise ValueError("❌ Error: Faltan las variables NEO4J_URI o NEO4J_PASSWORD en el archivo .env")
            
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Cierra la conexión con la base de datos."""
        self.driver.close()

    def cargar_grafo_desde_csv(self):
        """Lee el archivo2_grafo.csv e inyecta los nodos y relaciones en Neo4j."""
        path_csv = os.path.join(CARPETA_DATA, "archivo2_grafo.csv")
        
        if not os.path.exists(path_csv):
            print(f"❌ No se encontró archivo2_grafo.csv en la ruta: {path_csv}")
            return

        # Query de Cypher para limpiar la base de datos antes de cargar (evita duplicados)
        limpiar_query = "MATCH (n) DETACH DELETE n"
        
        # Query de Cypher para crear nodos y la relación dirigida entre ellos
        crear_relacion_query = """
        MERGE (a:Elemento {nombre: $origen, tipo: $tipo_origen})
        MERGE (b:Elemento {nombre: $destino, tipo: $tipo_destino})
        MERGE (a)-[r:CONECTADO_A {relacion: $tipo_relacion}]->(b)
        """

        with self.driver.session() as session:
            # 1. Limpiar grafo anterior
            session.run(limpiar_query)
            
            # 2. Leer CSV e insertar fila por fila
            with open(path_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f) # Lee usando las cabeceras del CSV
                contador = 0
                for fila in reader:
                    session.run(
                        crear_relacion_query,
                        origen=fila["origen"],
                        tipo_origen=fila["tipo_origen"],
                        destino=fila["destino"],
                        tipo_destino=fila["tipo_destino"],
                        tipo_relacion=fila["relacion"]
                    )
                    contador += 1
            print(f"✅ Éxito: Se han cargado e interconectado {contador} relaciones en Neo4j.")

    def consultar_vecinos(self, nombre_nodo: str) -> list:
        """Busca qué elementos están directamente conectados a un nodo en específico."""
        query = """
        MATCH (a:Elemento)-[r:CONECTADO_A]->(b:Elemento)
        WHERE toLower(a.nombre) CONTAINS toLower($nombre) OR toLower(b.nombre) CONTAINS toLower($nombre)
        RETURN a.nombre AS origen, a.tipo AS tipo_origen, r.relacion AS relacion, b.nombre AS destino, b.tipo AS tipo_destino
        LIMIT 5
        """
        relaciones_encontradas = []
        with self.driver.session() as session:
            resultado = session.run(query, nombre=nombre_nodo)
            for registro in resultado:
                relaciones_encontradas.append({
                    "origen": registro["origen"],
                    "tipo_origen": registro["tipo_origen"],
                    "relacion": registro["relacion"],
                    "destino": registro["destino"],
                    "tipo_destino": registro["tipo_destino"]
                })
        return relaciones_encontradas