from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import json
import os
import eventlet
import logging

eventlet.monkey_patch()

# ✅ Initialize app
app = Flask(__name__,
            static_folder="static",
            static_url_path='',  # allow root-level access to static files like /manifest.json
            template_folder="templates")

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

logging.basicConfig(level=logging.INFO)

# ✅ Location file
LOCATION_FILE = "location.json"

# ✅ Load last known shuttle location
def load_location():
    try:
        with open(LOCATION_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"lat": 24.9456, "lon": 67.0897}  # Default fallback location

# ✅ Save new location
def save_location(lat, lon):
    with open(LOCATION_FILE, "w") as f:
        json.dump({"lat": lat, "lon": lon}, f)

# ✅ Home page
@app.route("/")
def index():
    return render_template("index.html")

# ✅ Serve current shuttle location
@app.route("/location", methods=["GET"])
def get_location():
    return jsonify(load_location())

# ✅ Update shuttle location from driver app
@app.route("/update", methods=["POST"])
def update_location():
    data = request.get_json(force=True)
    lat = data.get("lat") or data.get("latitude")
    lon = data.get("lon") or data.get("longitude")

    if lat is not None and lon is not None:
        try:
            lat = float(lat)
            lon = float(lon)
            save_location(lat, lon)
            socketio.emit("location_update", {"lat": lat, "lon": lon})
            app.logger.info(f"Location updated: lat={lat}, lon={lon}")
            return jsonify({"status": "ok"})
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid coordinates"}), 400

    return jsonify({"status": "error", "message": "Missing lat/lon"}), 400

# ✅ Serve PWA files
@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")

@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

# ✅ Optional: robots.txt (to block crawlers)
@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /", 200, {'Content-Type': 'text/plain'}

# ✅ Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT automatically
    socketio.run(app, host="0.0.0.0", port=port)
