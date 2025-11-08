from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Python backend on Cloud Run!"

@app.route("/products")
def products():
    return jsonify([
        {"id": 1, "name": "Shoes", "price": 100},
        {"id": 2, "name": "Hat", "price": 40}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
