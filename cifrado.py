import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def obtener_llave(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def cifrar(mensaje, password, salt):
    key = obtener_llave(password, salt)
    return Fernet(key).encrypt(mensaje)

def descifrar(cifrado, password, salt):
    key = obtener_llave(password, salt)
    return Fernet(key).decrypt(cifrado)
