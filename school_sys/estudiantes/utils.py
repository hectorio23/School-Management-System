import os
import hashlib
import base64
from cryptography.fernet import Fernet
from django.conf import settings
#Función auxiliar (para la llave de cifrado)
def get_fernet_key():
    # Convertimos SECRET_KEY a bytes y generamos SHA-256
    sha = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    
    # Fernet necesita la llave en base64
    return base64.urlsafe_b64encode(sha)



#FUNCIÓN 1: Guardar archivos cifrados
def save_student_files(matricula: str, files: list, base_path: str):
    # 1. Generar SHA-256 de la matrícula
    folder_name = hashlib.sha256(matricula.encode()).hexdigest()

    # 2. Crear ruta completa del estudiante
    student_path = os.path.join(base_path, folder_name)
    os.makedirs(student_path, exist_ok=True)

    # 3. Crear objeto Fernet
    fernet = Fernet(get_fernet_key())

    # 4. Cifrar y guardar cada archivo
    for file in files:
        file_content = file.read()
        encrypted_content = fernet.encrypt(file_content)

        file_path = os.path.join(student_path, file.name)
        with open(file_path, "wb") as f:
            f.write(encrypted_content)

#FUNCIÓN 2: Leer y desencriptar archivo
def read_student_file(matricula: str, filename: str, base_path: str):
    # 1. Generar SHA-256 de la matrícula
    folder_name = hashlib.sha256(matricula.encode()).hexdigest()

    # 2. Ruta del archivo cifrado
    file_path = os.path.join(base_path, folder_name, filename)

    # 3. Crear objeto Fernet
    fernet = Fernet(get_fernet_key())

    # 4. Leer y desencriptar
    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data
