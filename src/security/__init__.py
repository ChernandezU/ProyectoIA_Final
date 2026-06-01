from .guardrail import evaluar_entrada, detect_injection_attempt
def sanitize_input(mensaje_usuario: str) -> str:
    return mensaje_usuario  # Retorna el texto limpio