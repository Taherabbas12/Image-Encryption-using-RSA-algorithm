from PIL import Image
from aes_utilities import generate_aes_key, aes_encrypt, aes_decrypt
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os


# تشفير الصورة
def encrypt_image(image_path, public_key):
    try:
        with Image.open(image_path) as image:
            image = image.convert('RGB')
            width, height = image.size
            pixels = image.tobytes()

        aes_key = generate_aes_key()
        iv = os.urandom(16)

        encrypted_data = aes_encrypt(pixels, aes_key, iv)

        encrypted_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        with open("encrypted_image.bin", "wb") as file:
            file.write(encrypted_key + iv + encrypted_data)

        return width, height
    except Exception as e:
        print(f"Error during encryption: {e}")
        raise


# فك تشفير الصورة
def decrypt_image(output_image_path, private_key, width, height):
    try:
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
                label=None,
            ),
        )

        decrypted_data = aes_decrypt(encrypted_data, aes_key, iv)

        image = Image.frombytes('RGB', (width, height), decrypted_data)
        image.save(output_image_path)
    except Exception as e:
        print(f"Error during decryption: {e}")
        raise
