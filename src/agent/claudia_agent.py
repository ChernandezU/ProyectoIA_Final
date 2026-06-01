import os
from groq import Groq
from dotenv import load_dotenv

# Configurar rutas automáticas
RUTA_AGENT = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(RUTA_AGENT))
RUTA_ENV = os.path.join(RAIZ_PROYECTO, ".env")

load_dotenv(RUTA_ENV)

class BancoGuatemaltecoAgent:
    def __init__(self):
        """Inicializa el agente con bypass de base de datos para evitar descargas trabadas."""
        # Colocamos tu clave de Groq autorizada directamente
        api_key = "GROQ_API_KEY_DE_TU_CUENTA"  # <-- Reemplaza con tu clave real de Groq    ESTÁ EN WHATSAPPY COMIENZA CON ESTO         api_key = "gsk_Jf"
        self.client = Groq(api_key=api_key)

    def responder_al_empleado(self, mensaje_usuario: str) -> str:
        """
        Detecta la consulta y simula el retorno estructurado de ChromaDB y Neo4j
        para enviarlo directamente a Groq sin congelar el sistema.
        """
        mensaje_min = mensaje_usuario.lower()
        
        # 1. Simulación de recuperación RAG (Bypass para saltar Hugging Face)
        if "prest" in mensaje_min or "préstamo" in mensaje_min:
            fuente = "Vector_RAG (ChromaDB - Local Cache)"
            contexto_recuperado = (
                "Título: Manual de software - Sistema de préstamos\n"
                "Procedimiento: Si el sistema de préstamos no carga, se debe limpiar la caché "
                "del navegador del empleado, verificar que los certificados SSL locales estén vigentes "
                "y, si la falla persiste por más de 10 minutos, reportar al equipo de administración de Bases de Datos."
            )
        else:
            fuente = "Graph_RAG (Neo4j Cloud Graph)"
            contexto_recuperado = (
                "🔗 Impresora_Oficina_Central ==(CONECTADO_A)==> Servidor_Impresion_Central\n"
                "🔗 Servidor_Impresion_Central ==(CONECTADO_A)==> Servidor_Core_Principal\n"
                "🔗 Servidor_Impresion_Central ==(DEPENDEN_DE)==> Soporte_Tecnico_Nivel_1\n"
                "👥 Contacto de Escalabilidad: Equipo de Soporte Técnico Nivel 1 (Ext. 4500)"
            )

        # 2. Diseñar el Prompt del Sistema idéntico al de producción
        prompt_sistema = f"""
        Eres el Asistente Virtual Inteligente de Soporte de TI del Banco Guatemalteco.
        Tu trabajo es resolver dudas técnicas de los empleados del banco de forma muy amable, clara y profesional.
        
        Para responder, debes basarte ESTRICTAMENTE en la información real extraída de nuestros sistemas de TI:
        ---
        FUENTE DE INFORMACIÓN: {fuente}
        CONTEXTO RECOLECTADO: {contexto_recuperado}
        ---
        
        Instrucciones:
        - Si el contexto contiene manuales o procedimientos, explícalos paso a paso amablemente.
        - Si el contexto contiene nodos/relaciones de red, explícale al usuario cómo está interconectado su equipo y a quién debe contactar o reportar según el flujo del grafo.
        - Mantén siempre un tono corporativo, educado y servicial. No inventes datos que no estén en el contexto.
        """

        # 3. Llamar a Groq con el modelo totalmente actualizado y activo
        try:
            intercambio = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": mensaje_usuario}
                ],
                model="llama-3.3-70b-versatile",  # <-- Este es el modelo definitivo
                temperature=0.2,
                max_tokens=500
            )
            return intercambio.choices[0].message.content
        except Exception as e:
            return f"❌ Error al generar respuesta con Groq: {e}"

    def finalizar(self):
        """Simula el cierre de conexiones limpia."""
        pass