from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import socket

def receive_des_key():
    # Load PKA's private key
    with open("pka_private.pem", "rb") as key_file:
        pka_private_key = RSA.import_key(key_file.read())

    # Start server to receive encrypted DES key
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 9999))
        s.listen(1)
        print("Receiver is waiting for connection...")
        conn, addr = s.accept()
        with conn:
            print(f"Connection established with {addr}")
            encrypted_des_key = conn.recv(256)
            print(f"Received Encrypted DES Key: {encrypted_des_key.hex()}")

            # Decrypt DES key using RSA
            cipher_rsa = PKCS1_OAEP.new(pka_private_key)
            des_key = cipher_rsa.decrypt(encrypted_des_key)
            print(f"Decrypted DES Key: {des_key.hex()}")

if __name__ == "__main__":
    receive_des_key()
