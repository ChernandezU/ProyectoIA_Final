import os
import json
import chromadb
from chromadb.utils import embedding_functions

# ─── CORRECCIÓN DE RUTAS DE DOBLE PROFUNDIDAD ──────────────────────
# __file__ es: raíz/src/retrieval/vector_rag.py
RUTA_RETRIEVAL = os.path.dirname(os.path.abspath(__file__))  # raíz/src/retrieval
RUTA_SRC = os.path.dirname(RUTA_RETRIEVAL)                  # raíz/src
RAIZ_PROYECTO = os.path.dirname(RUTA_SRC)                   # raíz (HernandezCristianProyectoIA)

CARPETA_DATA = os.path.join(RAIZ_PROYECTO, "data")
DB_DIR = os.path.join(RAIZ_PROYECTO, "chroma_db")
# ──────────────────────────────────────────────────────────────────

class VectorRAG:
    def __init__(self):
        """Inicializa el cliente de ChromaDB y el modelo de embeddings local."""
        self.cliente_chroma = chromadb.PersistentClient(path=DB_DIR)
        self.modelo_embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.coleccion = self.cliente_chroma.get_or_create_collection(
            name="bg_politicas_ti", 
            embedding_function=self.modelo_embeddings
        )

    def indexar_documentos(self):
        """Lee archivo1_documentos.json y guarda los vectores si la BD está vacía."""
        path_json = os.path.join(CARPETA_DATA, "archivo1_documentos.json")
        
        if not os.path.exists(path_json):
            print(f"❌ No se encontró archivo1_documentos.json en la ruta: {path_json}")
            return

        with open(path_json, "r", encoding="utf-8") as f:
            documentos = json.load(f)

        # Si ya tiene datos indexados, evitamos duplicarlos
        if self.coleccion.count() > 0:
            print(f"📦 La base de datos vectorial ya contiene {self.coleccion.count()} documentos indexados.")
            return

        print("🧠 Convirtiendo documentos a vectores (Embeddings)... Por favor espera.")
        
        ids = []
        textos = []
        metadatos = []

        for doc in documentos:
            texto_completo = f"Título: {doc['titulo']}\nContenido: {doc['contenido']}"
            ids.append(doc["id"])
            textos.append(texto_completo)
            metadatos.append({"categoria": doc["categoria"], "titulo": doc["titulo"]})

        self.coleccion.add(ids=ids, documents=textos, metadatas=metadatos)
        print(f"✅ ¡Éxito! Se han indexado {len(ids)} documentos en ChromaDB local.")

    def buscar_documentos_relevantes(self, consulta: str, resultados_maximos: int = 2) -> list:
        """Busca en ChromaDB los documentos más parecidos semánticamente a la consulta."""
        self.indexar_documentos() # Asegurar carga de datos
        
        resultado = self.coleccion.query(
            query_texts=[consulta],
            n_results=resultados_maximos
        )
        
        documentos_encontrados = []
        if resultado and resultado['documents'] and len(resultado['documents'][0]) > 0:
            for i in range(len(resultado['documents'][0])):
                documentos_encontrados.append({
                    "id": resultado['ids'][0][i],
                    "texto": resultado['documents'][0][i],
                    "metadatos": resultado['metadatas'][0][i]
                })
                
        return documentos_encontrados