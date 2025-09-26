from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import json
import os
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Firebase Admin
cred = credentials.Certificate("D:/Gps/service-account.json")  # 🔑 Your Firebase Admin SDK key file
firebase_admin.initialize_app(cred)

# File paths
LOCATION_FILE = "location.json"
DEVICE_TOKENS_FILE = "tokens.json"

# Geofence data
DEPARTMENTS = {
    "Computer Science": (24.944694, 67.114917),
    "Electrical": (24.9460, 67.0899),
    "Mechanical": (24.9465, 67.0888)
}
GEOFENCE_RADIUS = 0.0005  # ~50 meters

# ------------------ Utility Functions ------------------

def load_location():
    try:
        with open(LOCATION_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"lat": 24.9456, "lon": 67.0897}

def save_location(lat, lon):
    with open(LOCATION_FILE, "w") as f:
        json.dump({"lat": lat, "lon": lon}, f)

def load_tokens():
    try:
        with open(DEVICE_TOKENS_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_token(token):
    tokens = load_tokens()
    if token not in tokens:
        tokens.append(token)
        with open(DEVICE_TOKENS_FILE, "w") as f:
            json.dump(tokens, f)
    else:
        print("ℹ️ Token already exists.")

def send_fcm_notification(title, body):
    tokens = load_tokens()
    if not tokens:
        print("⚠️ No tokens to send.")
        return

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        tokens=tokens
    )

    response = messaging.send_each_for_multicast(message)
    print("📬 FCM Response:", response.success_count, "success,", response.failure_count, "failed")

def check_geofence(lat, lon):
    for dept, (dlat, dlon) in DEPARTMENTS.items():
        if abs(lat - dlat) < GEOFENCE_RADIUS and abs(lon - dlon) < GEOFENCE_RADIUS:
            return dept
    return None


from math import radians, cos, sin, asin, sqrt
def estimate_eta_minutes(lat, lon):
    cs_lat, cs_lon = DEPARTMENTS["Computer Science"]
    R = 6371  # km
    dlat = radians(cs_lat - lat)
    dlon = radians(cs_lon - lon)
    a = sin(dlat/2)**2 + cos(radians(lat)) * cos(radians(cs_lat)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    dist_km = R * c
    speed_kmh = 20.0  # assume 20 km/h
    return int((dist_km / speed_kmh) * 60)

# ------------------ Routes ------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/location")
def get_location():
    loc = load_location()
    
    loc["eta_min"] = estimate_eta_minutes(loc["lat"], loc["lon"])
    return jsonify(loc)

@app.route("/update", methods=["POST"])
def update_location():
    data = request.get_json(force=True)
    lat = data.get("lat") or data.get("latitude")
    lon = data.get("lon") or data.get("longitude")

    if lat and lon:
        try:
            lat = float(lat)
            lon = float(lon)
            save_location(lat, lon)

            
            socketio.emit("location_update", {
                "lat": lat,
                "lon": lon,
                "eta_min": estimate_eta_minutes(lat, lon)
            })

            dept = check_geofence(lat, lon)
            if dept:
                send_fcm_notification("Shuttle Arrival", f"Shuttle has reached {dept} Department")

            return jsonify({"status": "ok"})
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid lat/lon"}), 400

    return jsonify({"status": "error", "message": "Missing coordinates"}), 400

@app.route("/register-token", methods=["POST"])
def register_token():
    data = request.get_json()
    token = data.get("token")
    if token:
        save_token(token)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Missing token"}), 400

@app.route("/service-worker.js")
def sw():
    return send_from_directory("static", "service-worker.js")

@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

# ------------------ Main ------------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
