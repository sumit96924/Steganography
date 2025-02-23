import cv2
import os
import numpy as np
from cryptography.fernet import Fernet

# Generate or use a fixed encryption key
key = Fernet.generate_key()
cipher = Fernet(key)

# Load image with error handling
image_path = "C:/Users/sumit/Desktop/pyt/mypic.jpg"
img = cv2.imread(image_path)
if img is None:
    print("Error: Image not found. Check the file path.")
    exit()

msg = input("Enter secret message:")
password = input("Enter a passcode:")

# Encrypt the message
encrypted_msg = cipher.encrypt(msg.encode())
encrypted_msg = encrypted_msg.decode()

# Convert message to binary
binary_msg = ''.join(format(ord(c), '08b') for c in encrypted_msg)
msg_len = len(binary_msg)

# Embed message using LSB
h, w, _ = img.shape
idx = 0
for row in range(h):
    for col in range(w):
        for channel in range(3):
            if idx < msg_len:
                img[row, col, channel] = (img[row, col, channel] & ~1) | int(binary_msg[idx])
                idx += 1

cv2.imwrite("C:/Users/sumit/Desktop/pyt/encryptedImage.jpg", img)
os.system("start C:/Users/sumit/Desktop/pyt/encryptedImage.jpg")

# Decryption
pas = input("Enter passcode for Decryption: ")
if password == pas:
    extracted_bits = ""
    idx = 0
    for row in range(h):
        for col in range(w):
            for channel in range(3):
                if idx < msg_len:
                    extracted_bits += str(img[row, col, channel] & 1)
                    idx += 1

    decrypted_msg = ''.join(chr(int(extracted_bits[i:i+8], 2)) for i in range(0, len(extracted_bits), 8))
    decrypted_msg = cipher.decrypt(decrypted_msg.encode()).decode()
    print("Decryption message:", decrypted_msg)
else:
    print("YOU ARE NOT authorized")
