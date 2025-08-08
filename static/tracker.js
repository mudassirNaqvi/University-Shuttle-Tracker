let map;
let marker;

async function fetchLocation() {
  const res = await fetch('/location');
  const data = await res.json();
  return data;
}

function initMap(lat, lon) {
  map = L.map('map').setView([lat, lon], 16);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  marker = L.marker([lat, lon]).addTo(map)
           .bindPopup('Current Location')
           .openPopup();
}

async function updateMap() {
  const loc = await fetchLocation();
  const newLatLng = new L.LatLng(loc.lat, loc.lon);
  marker.setLatLng(newLatLng);
  map.panTo(newLatLng);
}

fetchLocation().then(loc => {
  initMap(loc.lat, loc.lon);
  setInterval(updateMap, 3000); 
});

