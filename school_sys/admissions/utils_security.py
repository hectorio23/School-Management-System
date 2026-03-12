import hashlib
import base64
from django.conf import settings
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- UTILIDADES DE SEGURIDAD PARA ADMISIONES ---

def generate_folio_hash(folio):
    """Genera un hash SHA-256 del folio o identificador para ocultar la estructura de archivos."""
    return hashlib.sha256(str(folio).encode()).hexdigest()

def get_fernet_key():
    """Deriva una llave de 32 bytes a partir de la SECRET_KEY de Django usando PBKDF2."""
    salt = b'admissions_salt_v1'  # Sal interna para derivación de llave
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    # Derivamos la llave para Fernet << AES-128 >>
    key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode()))
    return key

def encrypt_data(data):
    """Encripta datos binarios << bytes >> utilizando el algoritmo Fernet."""
    f = Fernet(get_fernet_key())
    return f.encrypt(data)

def decrypt_data(data):
    """Desencripta datos binarios << bytes >> utilizando la llave derivada del sistema."""
    f = Fernet(get_fernet_key())
    return f.decrypt(data)

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
        # Retornamos el original si no se puede desencriptar (ej. datos antiguos no cifrados)
        return encrypted_text

