import os
import sys

# Asegurar que Python reconozca la carpeta interna 'src' para resolver los imports de forma limpia
ruta_src = os.path.dirname(os.path.abspath(__file__))
if ruta_src not in sys.path:
    sys.path.append(ruta_src)

from retrieval.vector_rag import VectorRAG

print("============================================================")
print("TEST VECTOR RAG - Búsqueda Semántica en ChromaDB")
print("============================================================\n")

# 1. Instanciar el componente de la plantilla
rag_sistema = VectorRAG()

# 2. Definir una consulta de prueba
consulta_empleado = "Tengo problemas con la impresora, no puedo sacar mis comprobantes de pago."
print(f"🔍 Consulta del Empleado: \"{consulta_empleado}\"\n")

# 3. Ejecutar búsqueda mediante el método de la clase
documentos_encontrados = rag_sistema.buscar_documentos_relevantes(consulta_empleado, resultados_maximos=1)

if documentos_encontrados:
    doc = documentos_encontrados[0]
    print("✅ Documento Relevante Encontrado de forma Semántica:")
    print(f"📌 ID: {doc['id']}")
    print(f"📌 {doc['texto']}\n")
else:
    print("❌ No se encontraron documentos relacionados en ChromaDB.")
print("============================================================\n")