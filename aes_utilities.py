import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_aes_key():
    return os.urandom(32)

def aes_encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

# فك تشفير باستخدام AES
def aes_decrypt(encrypted_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()
