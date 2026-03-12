import hashlib
import base64
from django.conf import settings
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_matricula_hash(matricula):
    """Genera un hash SHA-256 de la matrícula para ocultar la estructura de archivos."""
    return hashlib.sha256(str(matricula).encode()).hexdigest()

def get_fernet_key():
    """Deriva una llave de 32 bytes a partir de la SECRET_KEY de Django."""
    # Usamos la misma sal que en admisiones para consistencia si fuera necesario, 
    # aunque aquí manejamos datos de estudiantes inscritos.
    salt = b'estudiantes_salt_v1' 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode()))
    return key

def encrypt_string(text):
    """Encripta una cadena de texto y retorna un string Base64."""
    if not text:
        return text
    f = Fernet(get_fernet_key())
    return f.encrypt(text.encode('utf-8')).decode('utf-8')

def decrypt_string(encrypted_text):
    """Desencripta un string Base64 y retorna el texto original."""
    if not encrypted_text:
        return encrypted_text
    try:
        f = Fernet(get_fernet_key())
        return f.decrypt(encrypted_text.encode('utf-8')).decode('utf-8')
    except Exception:
        return encrypted_text
