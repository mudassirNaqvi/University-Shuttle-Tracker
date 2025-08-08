importScripts("https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.7.0/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyD11rsR9f63WVv_BETeK5u0S-s_dpIncJM",
  authDomain: "shuttle-tracker-4f151.firebaseapp.com",
  projectId: "shuttle-tracker-4f151",
  messagingSenderId: "983403439545",
  appId: "1:983403439545:web:f23b51374ddd80db5f8268"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(payload => {
  console.log('[Service Worker] 📦 Background message received:', payload);

  self.registration.showNotification(payload.notification.title, {
    body: payload.notification.body,
    icon: '/static/van.png'  // Customize icon path
  });
});

self.addEventListener('install', event => {
  console.log('🔧 Service Worker installing...');
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  console.log('🚀 Service Worker activating...');
});


self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return new Response('📡 Offline content unavailable.');
    })
  );
});
