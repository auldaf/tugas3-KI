from flask import Flask, request, jsonify
from pka import PublicKeyAuthority

app = Flask(__name__)
pka = PublicKeyAuthority()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    server_id = data["server_id"]
    public_key = data["public_key"]
    pka.register_server(server_id, public_key)
    return jsonify({"message": f"Server {server_id} registered successfully"}), 200

@app.route('/public_key/<server_id>', methods=['GET'])
def get_public_key(server_id):
    public_key = pka.get_server_public_key(server_id)
    if public_key:
        return jsonify({"public_key": public_key}), 200
    return jsonify({"error": "Server not found"}), 404

if __name__ == "__main__":
    app.run(port=5000)
