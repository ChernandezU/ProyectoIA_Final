import os
import sys

ruta_src = os.path.dirname(os.path.abspath(__file__))
if ruta_src not in sys.path:
    sys.path.append(ruta_src)

from agent.claudia_agent import BancoGuatemaltecoAgent

print("============================================================")
print("  SISTEMA COGNITIVO DE TI - BANCO GUATEMALTECO (E2E)        ")
print("============================================================\n")

# Inicializar agente inteligente completo
agente_completo = BancoGuatemaltecoAgent()

try:
    # CASO 1: Consulta Técnica que requiere RAG Vectorial (ChromaDB) + Groq
    print("📋 [Empleado]: El sistema de préstamos no me carga, ¿qué hago?")
    respuesta_1 = agente_completo.responder_al_empleado("El sistema de préstamos no me carga, ¿qué hago?")
    print(f"\n🤖 [Groq Agent]:\n{respuesta_1}\n")
    print("="*70 + "\n")

    # CASO 2: Consulta de Infraestructura que requiere Graph RAG (Neo4j) + Groq
    print("📋 [Empleado]: ¿A qué servidor se conecta la impresora y con quién escalo?")
    respuesta_2 = agente_completo.responder_al_empleado("¿A qué servidor se conecta la impresora y con quién escalo?")
    print(f"\n🤖 [Groq Agent]:\n{respuesta_2}\n")
    print("="*70 + "\n")

finally:
    agente_completo.finalizar()

print("============================================================")
print("             FIN DE LA EVALUACIÓN DE CAPAS                  ")
print("============================================================\n")