function calculateDistance(point1, point2) {
    var x = point2.x - point1.x;
    var y = point2.y - point1.y;
    return Math.sqrt(x * x + y * y);
}

const SEA_COORDS = {
    "BlackSea": { x: 43.4130, y: 34.2993 },
    "MarmaraSea": { x: 40.6681, y: 28.1123 },
    "AegeanSea": { x: 39.0192, y: 25.2686 },
    "MediterraneanSea": { x: 34.5531, y: 18.0480 },
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
    console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
};

module.exports = {
    calculateDistance,
    coordinatesCallback,
    findNearestSea,
};