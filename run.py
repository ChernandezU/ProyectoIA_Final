"""
Script de Ejecución Principal
Ejecuta el servidor MCP con configuración automática
"""
import sys
import os
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def check_environment():
    """Verifica que el entorno esté configurado correctamente"""
    print("🔍 Verificando entorno...")
    
    # Verificar Python version
    if sys.version_info < (3, 10):
        print("❌ Se requiere Python 3.10 o superior")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Verificar estructura de carpetas
    required_dirs = ["data", "src", "src/security", "src/retrieval", "src/planner"]
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            print(f"❌ Falta carpeta: {dir_name}")
            return False
    
    print("✅ Estructura de carpetas correcta")
    
    # Verificar archivos de datos
    data_files = [
        "data/archivo1_documentos.json",
        "data/archivo2_grafo.csv"
    ]
    
    for file_name in data_files:
        if not Path(file_name).exists():
            print(f"⚠️  Archivo faltante: {file_name}")
    
    return True


def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        "chromadb",
        "neo4j",
        "pandas",
        "pydantic",
        "mcp"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - No instalado")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Faltan dependencias. Ejecuta:")
        print(f"   pip install -r requirements.txt")
        return False
    
    return True


def main():
    """Función principal"""
    print("=" * 70)
    print("HernandezCristian_ProyectoIA - MCP Server")
    print("=" * 70)
    print()
    
    # Verificar entorno
    if not check_environment():
        print("\n❌ Entorno no está correctamente configurado")
        return 1
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ Dependencias no están instaladas")
        return 1
    
    # Importar y ejecutar servidor
    print("\n" + "=" * 70)
    print("▶️  Iniciando servidor MCP...")
    print("=" * 70)
    
    try:
        from src.mcp_server import MCPServer
        
        # Crear servidor
        server = MCPServer()
        
        # Cargar datos
        data_file = Path("data/archivo1_documentos.json")
        if data_file.exists():
            print(f"\n📂 Cargando datos...")
            server.load_data_from_json(str(data_file))
        
        # Ejecutar
        print("\n" + "=" * 70)
        print("✅ Servidor MCP activo y listo")
        print("=" * 70)
        
        # Procesar consultas de ejemplo
        print("\n🧪 Ejecutando pruebas de ejemplo...\n")
        
        test_query = "¿Qué es el Graph RAG?"
        print(f"❓ {test_query}")
        
        result = server.process_query(test_query)
        
        if result["error"]:
            print(f"❌ Error: {result['error']}")
        else:
            print("✅ Procesado correctamente")
            print(f"\n📋 Resultado:")
            print(f"   - Documentos encontrados: {result.get('retrieved_documents', 0)}")
            print(f"   - Pasos completados: {len([s for s in result['steps'] if s['status'] == 'completed'])}")
            
            if result["response"]:
                print(f"\n📝 Respuesta:")
                print(f"{result['response']}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error al ejecutar servidor: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
