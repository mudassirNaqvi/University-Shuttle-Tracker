# University-Shuttle-Tracker

```markdown
# 🚐 University Shuttle Tracker (Live GPS Tracking with PWA)

A real-time GPS tracker web app for tracking a university shuttle/van using **Flask**, **Socket.IO**, **Leaflet.js**, and **Progressive Web App (PWA)** technology.

> 🛰️ Students can view the live shuttle location, and the driver can send updates via OwnTracks or a mobile interface.

---

## 🌐 Live Features

- 📍 **Live Location Tracking** using WebSockets  
- 🧭 **Van Rotation** in direction of movement  
- 🗺️ **Interactive Map** with Leaflet.js  
- 📲 **Installable PWA** (Add to Home Screen)  
- 🔔 **Push Notifications** (e.g. shuttle arrival alerts)  
- 👨‍✈️ **Separate Driver Interface** (for location updates)

---

## 📁 Folder Structure

```

University-Shuttle-Tracker/
│
├── app.py                   # Main Flask backend
├── templates/
│   └── index.html           # Frontend interface (student view)
├── static/
│   ├── van.png              # Van icon for the map
│   └── icons/               # PWA icons
├── location.json            # Stores current van coordinates
├── manifest.json            # PWA settings
├── service-worker.js        # Service worker for offline use
├── requirements.txt         # Python dependencies
├── render.yaml              # Deployment config for Render.com
└── README.md                # Project documentation (this file)

````

---

## 🚀 How It Works

### Students (View Only):
- Open the app
- See live shuttle location
- Receive notification when shuttle reaches a department

### Driver (Update Location):
- Sends GPS location via **OwnTracks** or a simple form
- The app broadcasts it using **Socket.IO** to all students in real time

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
````

---

## 🔧 Run Locally

```bash
python app.py
```

Visit in browser:
`http://localhost:5000`

---

## ☁️ Deploy on Render.com

This project is **Render-ready**!

1. Push to GitHub
2. Connect GitHub repo on [Render.com](https://render.com/)
3. Auto-detects:

   * `render.yaml`
   * `requirements.txt`
   * `app.py`
4. Choose **Free Plan** to deploy

---

## 📱 PWA Features

* ✅ Works like a native app
* ✅ Installable (via Add to Home Screen)
* ✅ Offline support via `service-worker.js`
* ✅ Custom icons and splash screen via `manifest.json`

---

## 🔔 Notifications (Optional Enhancement)

* Push notifications for shuttle arrivals using `Notification API`
* Future support for Firebase or VAPID for advanced messaging

---

## 💡 Future Features (Ideas)

* Department stop alerts
* Estimated Time of Arrival (ETA)
* Admin dashboard
* Authentication for driver
* Route heatmaps or analytics

---

## 📜 License

MIT License — use freely for academic/non-commercial purposes.

---

## 👨‍💻 Author

Made with ❤️ for university commuters.
Contributions welcome!
