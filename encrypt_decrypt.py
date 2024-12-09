import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PIL import Image

def generate_aes_key():
    return os.urandom(32)

def aes_encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def aes_decrypt(encrypted_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()

def load_keys():
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )

    return private_key, public_key

def encrypt_image(image_path, public_key):
    with Image.open(image_path) as image:
        image = image.convert('RGB')
        pixels = image.tobytes()

    aes_key = generate_aes_key()
    iv = os.urandom(16)

    encrypted_data = aes_encrypt(pixels, aes_key, iv)

    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open("encrypted_image.bin", "wb") as file:
        file.write(encrypted_key + iv + encrypted_data)

def decrypt_image(output_image_path, private_key):
    with open("encrypted_image.bin", "rb") as file:
        encrypted_content = file.read()

    encrypted_key = encrypted_content[:256]
    iv = encrypted_content[256:272]
    encrypted_data = encrypted_content[272:]

    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    decrypted_data = aes_decrypt(encrypted_data, aes_key, iv)

    image = Image.frombytes('RGB', (256, 256), decrypted_data)
    image.save(output_image_path)

if __name__ == "__main__":
    private_key, public_key = load_keys()
    encrypt_image("input_image.png", public_key)
    decrypt_image("output_image.png", private_key)
