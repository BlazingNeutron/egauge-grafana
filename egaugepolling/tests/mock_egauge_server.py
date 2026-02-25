import random, math, time
import json
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

START_TIME = time.perf_counter()
_last_offset: dict(str, float) = {
    "egauge000001.local:5000": 0.0,
    "egauge000002.local:5000": 0.0,
    "egauge000003.local:5000": 0.0,
    "egauge000004.local:5000": 0.0,
    "egauge000005.local:5000": 0.0,
    "egauge000006.local:5000": 0.0,
    "egauge000007.local:5000": 0.0,
}

_last_temp_trend: dict(str, float) = {
    "egauge000001.local:5000": 0.0,
    "egauge000002.local:5000": 0.0,
    "egauge000003.local:5000": 0.0,
    "egauge000004.local:5000": 0.0,
    "egauge000005.local:5000": 0.0,
    "egauge000006.local:5000": 0.0,
    "egauge000007.local:5000": 0.0,
}


def _random_float(min_val: float, max_val: float) -> float:
    return round(random.uniform(min_val, max_val), 2)


def generate_egauge_payload(device_name) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "ts": now,
        "registers": [
            {
                "name": "V1",
                "type": "V",
                "idx": 3,
                "did": 31,
                "rate": get_voltage(device_name),
            },
            {
                "name": "grid",
                "type": "P",
                "idx": 7,
                "did": 6,
                "rate": _random_float(0.0, 30.0),
            },
            {
                "name": "temp",
                "type": "T",
                "idx": 8,
                "did": 7,
                "rate": get_temperature(device_name),
            },
            {
                "name": "mask",
                "type": "#",
                "idx": 14,
                "did": 34,
                "rate": _random_float(0.0, 5000.0),
            },
        ],
    }


def get_temperature(device_name) -> float:
    global _last_temp_trend
    base = 45.0

    _last_temp_trend[device_name] += random.uniform(-0.1, 0.1)
    return base + _last_temp_trend[device_name]


def get_voltage(device_name) -> float:
    global _last_offset

    base = 230.0
    amplitude = 3.0
    frequency = 350.0

    t = time.perf_counter() - START_TIME

    wave = amplitude * math.sin(2 * math.pi * frequency * t)

    _last_offset[device_name] += random.uniform(-0.05, 0.05)
    _last_offset[device_name] = max(-2.0, min(2.0, _last_offset[device_name]))

    noise = random.uniform(-0.3, 0.3)

    return base + wave + _last_offset[device_name] + noise


@app.route("/api/register", methods=["GET"])
def egauge_json():
    payload = generate_egauge_payload(request.host)
    return jsonify(payload)


@app.route("/auth/login", methods=["POST"])
def egauge_login():
    return jsonify(
        {
            "rlm": "eGauge Administration",
            "usr": "owner",
            "nnc": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
            "cnnc": "565ce9541eddec103347b5174704e188",
            "hash": "ce5e308c27da651964de14f65bd8b059",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
