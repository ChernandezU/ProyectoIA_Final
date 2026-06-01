import os
import sys

ruta_src = os.path.dirname(os.path.abspath(__file__))
if ruta_src not in sys.path:
    sys.path.append(ruta_src)

from retrieval.graph_rag import GraphRAG

print("============================================================")
print("TEST GRAPH RAG - Conexión y Mapeo en Neo4j")
print("============================================================\n")

try:
    # 1. Conectarse a Neo4j
    print("🔄 Conectándose a la instancia de Neo4j...")
    grafo = GraphRAG()
    
    # 2. Poblar la base de datos con tu CSV
    print("📦 Cargando relaciones desde archivo2_grafo.csv...")
    grafo.cargar_grafo_desde_csv()
    
    # 3. Hacer una consulta de prueba de relaciones (Ej: buscar qué está conectado a 'Impresora')
    elemento_buscar = "impresora"
    print(f"\n🔍 Buscando conexiones del mapa de TI para: \"{elemento_buscar}\"")
    conexiones = grafo.consultar_vecinos(elemento_buscar)
    
    if conexiones:
        print(f"✅ Conexiones del grafo encontradas:")
        for con in conexiones:
            print(f"🔗 [{con['tipo_origen']}] {con['origen']} ──({con['relacion']})──> [{con['tipo_destino']}] {con['destino']}")
    else:
        print(f"⚠️ No se encontraron conexiones directas para '{elemento_buscar}' en el grafo.")
        
    grafo.close()

except Exception as e:
    print(f"\n❌ Error de ejecución: {e}")
print("\n============================================================\n")