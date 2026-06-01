from security.guardrail import evaluar_entrada
from retrieval.vector_rag import VectorRAG
from retrieval.graph_rag import GraphRAG

class AgentePlanificador:
    def __init__(self):
        """Inicializa los motores de búsqueda semántica y relacional."""
        self.vector_rag = VectorRAG()
        self.graph_rag = GraphRAG()

    def procesar_consulta(self, mensaje_usuario: str) -> dict:
        """
        Orquesta la consulta pasando por el escudo de seguridad
        y seleccionando la herramienta adecuada de recuperación de información.
        """
        # 1. Validar Capa de Seguridad (Guardrail)
        verificacion = evaluar_entrada(mensaje_usuario)
        if not verificacion["seguro"]:
            return {
                "estatus": "BLOQUEADO",
                "fuente": "Guardrail_Seguridad",
                "contexto": verificacion["mensaje_error"]
            }

        mensaje_min = mensaje_usuario.lower()

        # 2. Enrutador lógico (Routing)
        # Si la pregunta involucra conexiones, dependencias, quién es responsable o infraestructura:
        if any(palabra in mensaje_min for palabra in ["conectado", "depende", "servidor", "quien", "equipo", "infraestructura", "reporta"]):
            # Intentar extraer una palabra clave del mensaje para buscar en el grafo
            palabras = mensaje_min.split()
            # Buscar una palabra clave que no sea común (ej. impresora, prestamos, soporte)
            palabra_clave = next((p for p in palabras if len(p) > 5 and p not in ["tengo", "problemas", "con", "sistema"]), "impresora")
            
            conexiones = self.graph_rag.consultar_vecinos(palabra_clave)
            
            if conexiones:
                return {
                    "estatus": "EXITOSO",
                    "fuente": "Graph_RAG (Neo4j)",
                    "contexto": conexiones
                }

        # 3. Por defecto, si busca procedimientos o manuales de "cómo hacer algo", usamos Vector RAG
        documentos = self.vector_rag.buscar_documentos_relevantes(mensaje_usuario, resultados_maximos=1)
        if documentos:
            return {
                "estatus": "EXITOSO",
                "fuente": "Vector_RAG (ChromaDB)",
                "contexto": documentos[0]["texto"]
            }

        return {
            "estatus": "EXITOSO",
            "fuente": "Conversacional",
            "contexto": "No se requirió información externa de manuales o infraestructura."
        }
        
    def cerrar_conexiones(self):
        """Cierra de forma segura el driver de Neo4j."""
        self.graph_rag.close()