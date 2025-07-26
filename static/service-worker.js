self.addEventListener('install', event => {
  console.log('Service Worker installing...');
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  console.log('Service Worker activating...');
});

self.addEventListener('fetch', event => {
  // Basic fetch handler for offline
  event.respondWith(
    fetch(event.request).catch(() => {
      return new Response('Offline');
    })
  );
});
