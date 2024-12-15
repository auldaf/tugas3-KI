from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import socket

def send_des_key():
    # Generate DES key
    des_key = get_random_bytes(8)  # 8 bytes for DES key
    print(f"Generated DES Key: {des_key.hex()}")

    # Load PKA's public key
    with open("pka_public.pem", "rb") as key_file:
        pka_public_key = RSA.import_key(key_file.read())

    # Encrypt DES key using RSA
    cipher_rsa = PKCS1_OAEP.new(pka_public_key)
    encrypted_des_key = cipher_rsa.encrypt(des_key)
    print(f"Encrypted DES Key: {encrypted_des_key.hex()}")

    # Send encrypted DES key via socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 9999))
        s.sendall(encrypted_des_key)
        print("Encrypted DES key sent to receiver.")

if __name__ == "__main__":
    send_des_key()
