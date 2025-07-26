from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

LOCATION_FILE = "location.json"

def load_location():
    try:
        with open(LOCATION_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"lat": 24.9456, "lon": 67.0897}  # default location

def save_location(lat, lon):
    with open(LOCATION_FILE, "w") as f:
        json.dump({"lat": lat, "lon": lon}, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/location", methods=["GET"])
def get_location():
    return jsonify(load_location())

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
            socketio.emit("location_update", {"lat": lat, "lon": lon})
            return jsonify({"status": "ok"})
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid float values"}), 400

    return jsonify({"status": "error", "message": "Missing lat/lon"}), 400

# ✅ Serve service-worker.js from static folder
@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")

# ✅ Serve manifest.json from static folder
@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

# ✅ Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT automatically
    socketio.run(app, host="0.0.0.0", port=port)
