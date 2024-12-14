import os
from encrypt_decrypt import load_keys, encrypt_image, decrypt_image

os.environ['TCL_LIBRARY'] = r'C:\Users\ma610\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\ma610\AppData\Local\Programs\Python\Python313\tcl\tk8.6'
import os
from tkinter import Tk, Button, Label, filedialog, Frame
from PIL import Image, ImageTk
import numpy as np
from generate_keys import generate_keys, load_keys
from image_encryption import encrypt_image, decrypt_image


def apply_heavy_noise(image):
    """
    Apply a heavy noise effect to the image to completely obscure it.
    """
    # Get image dimensions
    width, height = image.size

    # Generate random noise
    noise = np.random.randint(0, 256, (height, width, 3), dtype='uint8')

    # Convert noise array to a PIL Image
    noisy_image = Image.fromarray(noise)
    return noisy_image


class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption & Decryption")
        self.root.geometry("900x500")

        self.selected_image_path = None
        self.width = None
        self.height = None

        # إنشاء الإطارات لعرض الصور
        self.image_frames = Frame(root)
        self.image_frames.pack(pady=10)

        self.original_image_label = Label(self.image_frames, text="Original Image")
        self.original_image_label.grid(row=0, column=0, padx=10)

        self.encrypted_image_label = Label(self.image_frames, text="Encrypted Image")
        self.encrypted_image_label.grid(row=0, column=1, padx=10)

        self.decrypted_image_label = Label(self.image_frames, text="Decrypted Image")
        self.decrypted_image_label.grid(row=0, column=2, padx=10)

        self.original_image_canvas = Label(self.image_frames)
        self.original_image_canvas.grid(row=1, column=0, padx=10)

        self.encrypted_image_canvas = Label(self.image_frames)
        self.encrypted_image_canvas.grid(row=1, column=1, padx=10)

        self.decrypted_image_canvas = Label(self.image_frames)
        self.decrypted_image_canvas.grid(row=1, column=2, padx=10)

        # أزرار التحكم
        self.select_button = Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=5)

        self.encrypt_button = Button(root, text="Encrypt Image", command=self.encrypt_image, state="disabled")
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = Button(root, text="Decrypt Image", command=self.decrypt_image, state="disabled")
        self.decrypt_button.pack(pady=5)

        self.status_label = Label(root, text="")
        self.status_label.pack(pady=10)

        # إنشاء المفاتيح إذا لم تكن موجودة
        if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem"):
            generate_keys()
            self.status_label.config(text="Keys generated successfully.")

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.selected_image_path = file_path
            image = Image.open(file_path)
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)
            self.original_image_canvas.config(image=photo)
            self.original_image_canvas.image = photo
            self.encrypt_button.config(state="normal")
            self.status_label.config(text=f"Selected Image: {os.path.basename(file_path)}")

    def encrypt_image(self):
        if not self.selected_image_path:
            self.status_label.config(text="No image selected.")
            return

        try:
            # Load keys
            private_key, public_key = load_keys()

            # Encrypt the image (placeholder for actual encryption logic)
            self.width, self.height = encrypt_image(self.selected_image_path, public_key)

            # Apply heavy noise effect to the original image
            original_image = Image.open(self.selected_image_path)
            noisy_image = apply_heavy_noise(original_image)

            # Resize the noisy image to fit the canvas
            noisy_image.thumbnail((200, 200))
            noisy_photo = ImageTk.PhotoImage(noisy_image)

            # Display the noisy image as the "encrypted" image
            self.encrypted_image_canvas.config(image=noisy_photo)
            self.encrypted_image_canvas.image = noisy_photo

            self.status_label.config(text="Image encrypted successfully.")
            self.decrypt_button.config(state="normal")
        except Exception as e:
            self.status_label.config(text=f"Error during encryption: {e}")

    def decrypt_image(self):
        try:
            private_key, _ = load_keys()
            output_image_path = "decrypted_image.png"
            decrypt_image(output_image_path, private_key, self.width, self.height)

            decrypted_image = Image.open(output_image_path)
            decrypted_image.thumbnail((200, 200))
            decrypted_photo = ImageTk.PhotoImage(decrypted_image)

            self.decrypted_image_canvas.config(image=decrypted_photo)
            self.decrypted_image_canvas.image = decrypted_photo

            self.status_label.config(text="Image decrypted successfully.")
        except Exception as e:
            self.status_label.config(text=f"Error during decryption: {e}")


if __name__ == "__main__":
    root = Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()
