"""
Servidor MCP Principal
Integra todos los módulos: Guardrails, Vector RAG, Graph RAG, Action Planner
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Importar módulos locales
from src.security.guardrail import validate_query, apply_content_filter
from src.retrieval.vector_rag import VectorRAG
from src.retrieval.graph_rag import GraphRAG
from src.planner.action_planner import ActionPlanner, Action, ActionType


class MCPServer:
    """Servidor MCP que integra todos los componentes"""
    
    def __init__(self, config_path: str = None):
        """
        Inicializa el servidor MCP
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config = self.load_config(config_path)
        self.vector_rag = VectorRAG(
            collection_name=self.config.get("vector_collection", "documentos"),
            persist_dir=self.config.get("vector_persist", "./chroma_data")
        )
        
        # GraphRAG se inicializa solo si hay credenciales
        self.graph_rag = None
        if self.config.get("neo4j_uri"):
            self.graph_rag = GraphRAG(
                uri=self.config["neo4j_uri"],
                username=self.config.get("neo4j_user", "neo4j"),
                password=self.config.get("neo4j_password", "")
            )
        
        self.planner = ActionPlanner()
        self.query_history: List[Dict] = []
    
    def load_config(self, config_path: str = None) -> Dict:
        """
        Carga configuración desde archivo o crea por defecto
        
        Args:
            config_path: Ruta al archivo de configuración
            
        Returns:
            Diccionario de configuración
        """
        default_config = {
            "vector_collection": "documentos",
            "vector_persist": "./chroma_data",
            "neo4j_uri": None,
            "neo4j_user": "neo4j",
            "neo4j_password": "",
            "max_results": 5,
            "temperature": 0.7,
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                loaded = json.load(f)
                default_config.update(loaded)
        
        return default_config
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Procesa una consulta del usuario
        
        Args:
            query: Consulta del usuario
            
        Returns:
            Respuesta procesada
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "steps": [],
            "response": None,
            "error": None
        }
        
        # Paso 1: Validar entrada (Guardrails)
        result["steps"].append({"step": "validation", "status": "in_progress"})
        is_valid, validation_msg = validate_query(query)
        
        if not is_valid:
            result["error"] = validation_msg
            result["steps"][-1]["status"] = "failed"
            result["steps"][-1]["reason"] = validation_msg
            return result
        
        result["steps"][-1]["status"] = "completed"
        
        # Paso 2: Planificación
        result["steps"].append({"step": "planning", "status": "in_progress"})
        plan = self.planner.build_plan(query)
        result["plan"] = [action.to_dict() for action in plan]
        result["steps"][-1]["status"] = "completed"
        
        # Paso 3: Recuperación de información
        result["steps"].append({"step": "retrieval", "status": "in_progress"})
        retrieved_docs = self._retrieve_documents(query)
        result["retrieved_documents"] = len(retrieved_docs)
        result["steps"][-1]["status"] = "completed"
        
        # Paso 4: Exploración de grafo (si está disponible)
        if self.graph_rag:
            result["steps"].append({"step": "graph_exploration", "status": "in_progress"})
            try:
                if self.graph_rag.connect():
                    graph_results = self.graph_rag.query("MATCH (n) RETURN n LIMIT 5")
                    result["graph_results"] = len(graph_results)
                    self.graph_rag.close()
                result["steps"][-1]["status"] = "completed"
            except Exception as e:
                result["steps"][-1]["status"] = "skipped"
                result["steps"][-1]["reason"] = f"GraphRAG no disponible: {str(e)}"
        
        # Paso 5: Síntesis de respuesta
        result["steps"].append({"step": "synthesis", "status": "in_progress"})
        response = self._generate_response(query, retrieved_docs)
        response = apply_content_filter(response)
        result["response"] = response
        result["steps"][-1]["status"] = "completed"
        
        # Guardar en historial
        self.query_history.append(result)
        
        return result
    
    def _retrieve_documents(self, query: str) -> List[Dict]:
        """
        Recupera documentos similares
        
        Args:
            query: Consulta de búsqueda
            
        Returns:
            Lista de documentos
        """
        try:
            self.vector_rag.create_collection()
            results = self.vector_rag.search(query, top_k=self.config["max_results"])
            return results
        except Exception as e:
            print(f"⚠️  Error en recuperación: {e}")
            return []
    
    def _generate_response(self, query: str, context: List[Dict]) -> str:
        """
        Genera respuesta basada en contexto
        
        Args:
            query: Consulta original
            context: Contexto recuperado
            
        Returns:
            Respuesta generada
        """
        response = f"Basándome en tu pregunta: '{query}'\n\n"
        
        if context:
            response += "He encontrado la siguiente información relevante:\n"
            for i, doc in enumerate(context, 1):
                response += f"\n{i}. {doc.get('contenido', 'N/A')[:200]}..."
                if 'metadata' in doc:
                    response += f"\n   [Fuente: {doc['metadata'].get('categoria', 'general')}]"
        else:
            response += "No encontré documentos específicos, pero aquí está mi análisis:\n"
            response += "Este es un tema interesante que requiere investigación adicional."
        
        return response
    
    def load_data_from_json(self, json_path: str) -> bool:
        """
        Carga datos desde archivo JSON
        
        Args:
            json_path: Ruta al archivo JSON
            
        Returns:
            True si se cargó exitosamente
        """
        try:
            self.vector_rag.load_from_json(json_path)
            return True
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return False
    
    def get_status(self) -> Dict:
        """
        Obtiene estado del servidor
        
        Returns:
            Estado del servidor
        """
        return {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "modules": {
                "guardrails": "active",
                "vector_rag": "active",
                "graph_rag": "available" if self.graph_rag else "unavailable",
                "planner": "active"
            },
            "queries_processed": len(self.query_history),
            "config": self.config
        }


def main():
    """Función principal para pruebas"""
    print("=" * 70)
    print("MCP Server - Graph RAG + Claude Integration")
    print("=" * 70)
    
    # Crear servidor
    server = MCPServer()
    
    # Mostrar estado
    print("\n📡 Estado del servidor:")
    status = server.get_status()
    for module, state in status["modules"].items():
        print(f"   {module}: {state}")
    
    # Cargar datos de ejemplo
    data_file = Path(__file__).parent / "data" / "archivo1_documentos.json"
    if data_file.exists():
        print(f"\n📂 Cargando datos desde {data_file}")
        if server.load_data_from_json(str(data_file)):
            print("✅ Datos cargados exitosamente")
    
    # Procesar consultas de ejemplo
    test_queries = [
        "¿Qué es el Graph RAG?",
        "¿Cómo funciona ChromaDB?",
        "¿Cuál es la importancia de la IA?",
    ]
    
    print("\n" + "=" * 70)
    print("Procesando consultas de prueba...")
    print("=" * 70)
    
    for query in test_queries:
        print(f"\n❓ {query}")
        result = server.process_query(query)
        
        if result["error"]:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Respuesta generada")
            print(f"   Documentos recuperados: {result.get('retrieved_documents', 0)}")
            print(f"   Pasos completados: {len([s for s in result['steps'] if s['status'] == 'completed'])}")
            if result["response"]:
                print(f"   Preview: {result['response'][:200]}...")
    
    print("\n" + "=" * 70)
    print("✅ Servidor MCP inicializado correctamente")
    print("=" * 70)


if __name__ == "__main__":
    main()
