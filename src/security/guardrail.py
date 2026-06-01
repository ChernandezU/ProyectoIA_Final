import re

# Lista de expresiones o intenciones prohibidas (Ataques de Jailbreak comunes)
PATRONES_MALICIOSOS = [
    r"ignora\s+las\s+políticas",
    r"omite\s+las\s+reglas",
    r"actúa\s+como\s+un\s+sistema\s+sin\s+restricciones",
    r"desbloquear\s+.*sin\s+autorización",
    r"bypass\s+security",
    r"saltarse\s+los\s+protocolos",
    r"olvida\s+tus\s+instrucciones"
]

def evaluar_entrada(mensaje_usuario: str) -> dict:
    """
    Analiza el texto del usuario. Si detecta un intento de saltarse
    las reglas del banco, bloquea la consulta de inmediato.
    """
    mensaje_minusculas = mensaje_usuario.lower()
    
    # Buscar si el mensaje coincide con alguna frase de la lista negra
    for patron in PATRONES_MALICIOSOS:
        if re.search(patron, mensaje_minusculas):
            return {
                "seguro": False,
                "mensaje_error": "Acción no permitida por los protocolos de seguridad de TI del Banco Guatemalteco. El intento ha sido registrado en la bitácora de auditoría."
            }
            
    return {"seguro": True, "mensaje_error": None}


# 💡 FUNCIÓN DE COMPATIBILIDAD: Agregada para satisfacer tu archivo __init__.py
def detect_injection_attempt(mensaje_usuario: str) -> bool:
    """
    Retorna True si detecta un intento de inyección/jailbreak (no es seguro),
    y False si la consulta es limpia.
    """
    resultado = evaluar_entrada(mensaje_usuario)
    return not resultado["seguro"]  # Si seguro es False, retorna True (intento detectado)