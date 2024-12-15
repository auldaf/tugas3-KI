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

# RSA Key Pair Server
server_public_key = None
server_private_key = None

async def register_to_pka():
    async with websockets.connect("ws://localhost:8766") as websocket:
        # Kirim permintaan registrasi
        await websocket.send("REGISTER_SERVER")

        # Terima kunci publik PKA
        pka_public_key = await websocket.recv()
        print(f"PKA Public Key diterima: {pka_public_key}")

        # Kirim kunci publik server
        server_public_key = "7,3233"  # Contoh kunci publik server
        await websocket.send(server_public_key)

        # Terima balasan konfirmasi
        confirmation = await websocket.recv()
        print(f"Konfirmasi diterima: {confirmation}")

async def handle_client(websocket):
    print("Client terhubung.")
    # Terima pesan terenkripsi DES
    encrypted_message = await websocket.recv()
    print(f"Pesan terenkripsi diterima: {encrypted_message}")

    # Dekripsi pesan menggunakan DES
    des_key = b"simplekey"  # Contoh key DES
    decrypted_message = des_decrypt(bytes.fromhex(encrypted_message), des_key)
    print(f"Pesan didekripsi: {decrypted_message.decode()}")

    # Kirim balasan ke client
    reply = input("Masukkan balasan untuk Client: ").encode()
    encrypted_reply = des_encrypt(reply, des_key)
    await websocket.send(encrypted_reply.hex())
    print("Balasan terenkripsi berhasil dikirim.")

async def main():
    await register_to_pka()
    async with websockets.serve(handle_client, "localhost", 8765):
        print("Server berjalan di ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
