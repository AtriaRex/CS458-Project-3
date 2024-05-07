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

// gets the distance to the center of the sun from a given coordinates on earth
async function getDistanceToSun(longitude, latitude) {
    const result = await fetch("calculate-distance-to-sun", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body:
            JSON.stringify({
                longitude: longitude,
                latitude: latitude
            })
    });
    const distance = await result.json();
    console.log(distance);

    return distance;
}

async function getNearestSea(position) {
    const result = await fetch("get-closest-sea", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body:
            JSON.stringify({
                longitude: position.lon,
                latitude: position.lat,
            })
    });
    const sea = await result.json();
    console.log(sea);

    return sea;
}

function coordinatesCallbackSea(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    const nearestSea = getNearestSea({ lat: latitude, lon: longitude });
    const nearestSeaText = document.querySelector("#nearestSea");
    nearestSeaText.textContent = nearestSea.sea;

    const nearestSeaDistance = document.querySelector("#nearestSeaDistance");
    nearestSeaDistance.textContent = nearestSea.distance;

    console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
};

async function coordinatesCallbackSun(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    let distance = await getDistanceToSun(longitude, latitude);
    const distanceText = document.querySelector("#distanceToSun");
    distanceText.textContent = distance.distance;
};

module.exports = {
    calculateDistance,
    coordinatesCallbackSea,
    getNearestSea,
    coordinatesCallbackSun,
    getDistanceToSun
};