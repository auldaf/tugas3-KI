import asyncio
import websockets

# Fungsi dasar RSA
def rsa_encrypt(message, key):
    e, n = key
    return [pow(char, e, n) for char in message]

def rsa_decrypt(ciphertext, key):
    d, n = key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

# Fungsi DES sederhana
def des_encrypt(message, key):
    return bytes([message[i] ^ key[i % len(key)] for i in range(len(message))])

def des_decrypt(ciphertext, key):
    return bytes([ciphertext[i] ^ key[i % len(key)] for i in range(len(ciphertext))])

# RSA Key Pair Client
client_public_key = (11, 3233)  # Contoh
client_private_key = (413, 3233)  # Contoh

async def register_to_pka():
    async with websockets.connect("ws://localhost:8766") as websocket:
        # Kirim permintaan registrasi
        await websocket.send("REGISTER_CLIENT")

        # Terima kunci publik PKA
        pka_public_key = await websocket.recv()
        print(f"PKA Public Key diterima: {pka_public_key}")

        # Kirim kunci publik server
        server_public_key = "7,3233"  # Contoh kunci publik server
        await websocket.send(server_public_key)

        # Terima balasan konfirmasi
        confirmation = await websocket.recv()
        print(f"Konfirmasi diterima: {confirmation}")

async def communicate_with_server():
    async with websockets.connect("ws://localhost:8765") as websocket:
        # DES Key
        des_key = b"simplekey"

        # Pesan yang akan dikirim
        message = input("Masukkan pesan untuk server: ").encode()
        encrypted_message = des_encrypt(message, des_key)

        # Kirim pesan terenkripsi ke server
        await websocket.send(encrypted_message.hex())
        print("Pesan terenkripsi dikirim ke server.")

        # Terima balasan dari server
        encrypted_reply = await websocket.recv()
        decrypted_reply = des_decrypt(bytes.fromhex(encrypted_reply), des_key)
        print(f"Balasan dari server: {decrypted_reply.decode()}")

async def main():
    await register_to_pka()
    await communicate_with_server()

asyncio.run(main())
