# 🚐 University Shuttle Tracker (Live GPS Tracking with PWA)

A real-time GPS tracker web app for tracking a university shuttle/van using **Flask**, **Socket.IO**, **Leaflet.js**, **Firebase Cloud Messaging (FCM)**, and **Progressive Web App (PWA)** technology.

> 🛰️ Students can view the live shuttle location, and the driver can send updates via OwnTracks or a mobile interface.
> 🔔 Firebase is now used for push notifications so students get instant shuttle alerts.

---

## 🌐 Live Features

* 📍 **Live Location Tracking** using WebSockets
* 🧭 **Van Rotation** in direction of movement
* 🗺️ **Interactive Map** with Leaflet.js
* 📲 **Installable PWA** (Add to Home Screen)
* 🔔 **Push Notifications with Firebase Cloud Messaging (FCM)** for shuttle arrivals
* 👨‍✈️ **Separate Driver Interface** (for location updates)

---

## 📁 Folder Structure

```
University-Shuttle-Tracker/
│
├── app.py               # Main Flask backend
├── templates/
│   └── index.html        # Frontend interface (student view)
├── static/
│   ├── van.png           # Van icon for the map
│   └── icons/            # PWA icons
├── location.json         # Stores current van coordinates
├── manifest.json         # PWA settings
├── service-worker.js     # Service worker for offline use & FCM
├── firebase-messaging-sw.js  # Firebase service worker for push
├── requirements.txt      # Python dependencies
├── render.yaml           # Deployment config for Render.com
└── README.md             # Project documentation
```

---

## 🚀 How It Works

### Students (View Only):

* Open the app
* See live shuttle location
* Receive **Firebase push notifications** when the shuttle reaches a department

### Driver (Update Location):

* Sends GPS location via **OwnTracks** or a simple form
* The app broadcasts it using **Socket.IO** to all students in real time
* Can trigger **Firebase push notifications** for important alerts

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔧 Run Locally

```bash
python app.py
```

Visit in browser:
[http://localhost:5000](http://localhost:5000)

---

## ☁️ Deploy on Render.com

This project is Render-ready!

1. Push to GitHub
2. Connect GitHub repo on Render.com
3. Auto-detects:

   * `render.yaml`
   * `requirements.txt`
   * `app.py`
4. Choose Free Plan to deploy

---

## 📱 PWA + Firebase Features

✅ Works like a native app
✅ Installable (via Add to Home Screen)
✅ Offline support via `service-worker.js`
✅ **Firebase Cloud Messaging (FCM)** push notifications for shuttle arrivals
✅ Custom icons and splash screen via `manifest.json`

---

## 🔔 Notifications (with Firebase)

* Uses **Firebase Cloud Messaging (FCM)** for cross-platform push alerts
* Works in browsers and on mobile (via PWA)
* Supports both manual triggers (driver alert) and automated triggers (geo-based events)

---

## 💡 Future Features (Ideas)

* Department stop alerts
* Estimated Time of Arrival (ETA)
* Admin dashboard
* Authentication for driver
* Route heatmaps or analytics
* Firebase topic-based messaging for different routes

---

## 📜 License

MIT License — use freely for academic/non-commercial purposes.

---

## 👨‍💻 Author

Made with ❤️ for university commuters. Contributions welcome!
