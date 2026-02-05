import hashlib

def generate_matricula_hash(matricula):
    """Genera un hash SHA-256 de la matrícula para ocultar la estructura de archivos."""
    return hashlib.sha256(str(matricula).encode()).hexdigest()
