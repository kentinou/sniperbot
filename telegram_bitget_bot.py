from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🏠 Serveur actif", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📩 Webhook reçu :", data)
    return "OK ✅", 200

if __name__ == "__main__":
    print("🚀 Serveur webhook test lancé")
    app.run(host="0.0.0.0", port=8080)
