// Array of places with their coordinates
var places = document.currentScript.getAttribute('data-marketplaces-map');
places = JSON.parse(places);

// Initialize the map to Costa Rica
var map = L.map('map').setView([9.7489, -83.7534], 7);

// Add the tile layer (e.g., OpenStreetMap)
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: 'Datos: TC-691 Tropicalización. Mapa: &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
    maxZoom: 18,
}).addTo(map);

// Add markers for each place
places.forEach(function (place) {
    L.marker([place.latitude, place.longitude]).addTo(map).bindPopup("Feria de " + place.name);
});