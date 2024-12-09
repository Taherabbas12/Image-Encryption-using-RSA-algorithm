import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from PIL import Image

# توليد وحفظ المفاتيح
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # حفظ المفتاح الخاص
    with open("private_key.pem", "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # حفظ المفتاح العام
    with open("public_key.pem", "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

# تحميل المفاتيح
def load_keys():
    try:
        with open("private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)

        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        return private_key, public_key
    except FileNotFoundError:
        print("Error: Key files not found. Please generate keys first.")
        raise

# تشفير البيانات باستخدام المفتاح العام
def encrypt_data(data, public_key):
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return encrypted_data

# فك تشفير البيانات باستخدام المفتاح الخاص
def decrypt_data(encrypted_data, private_key):
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted_data

# تشفير الصورة باستخدام RSA
def encrypt_image(image_path, public_key):
    try:
        with Image.open(image_path) as image:
            image = image.convert('RGB')
            width, height = image.size
            pixels = image.tobytes()

        # تشفير البيانات باستخدام المفتاح العام
        encrypted_data = encrypt_data(pixels, public_key)

        # حفظ البيانات المشفرة
        with open("encrypted_image.bin", "wb") as file:
            file.write(encrypted_data)

        return width, height
    except Exception as e:
        print(f"Error during encryption: {e}")
        raise

# فك تشفير الصورة باستخدام RSA
def decrypt_image(output_image_path, private_key, width, height):
    try:
        with open("encrypted_image.bin", "rb") as file:
            encrypted_data = file.read()

        # فك تشفير البيانات باستخدام المفتاح الخاص
        decrypted_data = decrypt_data(encrypted_data, private_key)

        # إعادة بناء الصورة باستخدام البيانات المفكوكة
        image = Image.frombytes('RGB', (width, height), decrypted_data)
        image.save(output_image_path)
    except Exception as e:
        print(f"Error during decryption: {e}")
        raise
