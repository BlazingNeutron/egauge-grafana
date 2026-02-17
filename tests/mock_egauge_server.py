import random
import json
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

def _random_float(min_val: float, max_val: float) -> float:
    return round(random.uniform(min_val, max_val), 2)

def generate_egauge_payload() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "ts": now,
        "registers": [
            { "name": "V1", "type": "V", "idx": 3, "did": 31, "rate": _random_float(110.0, 240.0) },
            { "name": "grid", "type": "P", "idx": 7, "did": 6, "rate": _random_float(0.0, 30.0) },
            { "name": "temp", "type": "T", "idx": 8, "did": 7, "rate": _random_float(0.0, 200.0) },
            { "name": "mask", "type": "#", "idx": 14, "did": 34, "rate": _random_float(0.0, 5000.0) }
        ]
    }

@app.route("/api/register", methods=["GET"])
def egauge_json():
    payload = generate_egauge_payload()
    return jsonify(payload)


@app.route("/auth/login", methods=["POST"])
def egauge_login():
    return jsonify({
        "rlm": "eGauge Administration",
        "usr": "owner",
        "nnc": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
        "cnnc": "565ce9541eddec103347b5174704e188",
        "hash": "ce5e308c27da651964de14f65bd8b059"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
