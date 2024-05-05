function calculateDistance(point1, point2) {
    const R = 6371e3; // radius of earth in metres
    const phi1 = point1.lat * Math.PI / 180;
    const phi2 = point2.lat * Math.PI / 180;
    const delta_phi = (point2.lat - point1.lat) * Math.PI / 180;
    const delta_lambda = (point2.lon - point1.lon) * Math.PI / 180;

    // Haversine formula
    const a = Math.sin(delta_phi / 2) * Math.sin(delta_phi / 2) +
        Math.cos(phi1) * Math.cos(phi2) *
        Math.sin(delta_lambda / 2) * Math.sin(delta_lambda / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const d = R * c; // in metres

    return d;
}

const SEA_COORDS = {
    "BlackSea": { lat: 43.4130, lon: 34.2993 },
    "MarmaraSea": { lat: 40.6681, lon: 28.1123 },
    "AegeanSea": { lat: 39.0192, lon: 25.2686 },
    "MediterraneanSea": { lat: 34.5531, lon: 18.0480 },
};

function findNearestSea(position) {
    let nearestSea = null;
    for (const [sea, coords] of Object.entries(SEA_COORDS)) {
        let distance = calculateDistance(position, coords);
        if (!nearestSea || distance < nearestSea.distance) {
            nearestSea = { sea, distance };
        }
    }

    return nearestSea;
}

function coordinatesCallback(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    const nearestSea = findNearestSea({ lat: latitude, lon: longitude });
    const nearestSeaText = document.querySelector("#nearestSea");
    nearestSeaText.textContent = nearestSea.sea;

    const nearestSeaDistance = document.querySelector("#nearestSeaDistance");
    nearestSeaDistance.textContent = nearestSea.distance;

    console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
};

module.exports = {
    calculateDistance,
    coordinatesCallback,
    findNearestSea,
};