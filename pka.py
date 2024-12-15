import asyncio
import websockets

# RSA sederhana tanpa library
def rsa_keygen():
    p, q = 61, 53  # Bilangan prima
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17  # Public exponent
    d = pow(e, -1, phi)  # Private exponent
    return (e, n), (d, n)

# PKA Key Pair
pka_public_key, pka_private_key = rsa_keygen()

# Simpan kunci publik yang akan diberikan ke client/server
server_public_key = None
client_public_key = None

async def handle_request(websocket, path):
    global server_public_key, client_public_key

    # Menerima permintaan (registrasi server atau client)
    request = await websocket.recv()

    print(f"Permintaan diterima: {request}")

    if request == "REGISTER_SERVER":
        # Kirim kunci publik PKA ke server
        await websocket.send(f"{pka_public_key[0]},{pka_public_key[1]}")

        # Terima kunci publik server
        server_public_key = await websocket.recv()
        print(f"Server Public Key diterima: {server_public_key}")

        # Kirim balasan konfirmasi ke server
        await websocket.send("Server key registered successfully")

    elif request == "REGISTER_CLIENT":
        # Kirim kunci publik PKA ke client
        await websocket.send(f"{pka_public_key[0]},{pka_public_key[1]}")

        # Terima kunci publik client
        client_public_key = await websocket.recv()
        print(f"Client Public Key diterima: {client_public_key}")

        # Kirim balasan konfirmasi ke client
        await websocket.send("Client key registered successfully")

    elif request == "GET_SERVER_KEY":
        # Kirim kunci publik server ke client
        if server_public_key:
            await websocket.send(server_public_key)
        else:
            await websocket.send("Server key not available")

    elif request == "GET_CLIENT_KEY":
        # Kirim kunci publik client ke server
        if client_public_key:
            await websocket.send(client_public_key)
        else:
            await websocket.send("Client key not available")

    else:
        # Menangani permintaan yang tidak dikenali
        await websocket.send("Invalid request")

async def main():
    async with websockets.serve(handle_request, "localhost", 8766):
        print("PKA berjalan di ws://localhost:8766")
        await asyncio.Future()  # Menjaga server tetap berjalan

asyncio.run(main())
