from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import json
import os
import eventlet
eventlet.monkey_patch()  # Required for eventlet to work with Flask-SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

LOCATION_FILE = "location.json"

# Load last known shuttle location
def load_location():
    try:
        with open(LOCATION_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"lat": 24.9456, "lon": 67.0897}  # Default location (e.g., university gate)

# Save current shuttle location
def save_location(lat, lon):
    with open(LOCATION_FILE, "w") as f:
        json.dump({"lat": lat, "lon": lon}, f)

# Main index page (student side map)
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint to get current shuttle location
@app.route("/location", methods=["GET"])
def get_location():
    return jsonify(load_location())

# API to update shuttle location (from driver app)
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

# Serve PWA service worker
@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")

# Serve PWA manifest file
@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

# Run app with eventlet (Render-compatible port binding)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or fallback to 5000
    socketio.run(app, host="0.0.0.0", port=port)
