function calculateDistance(point1, point2) {
    var x = point2.x - point1.x;
    var y = point2.y - point1.y;
    return Math.sqrt(x * x + y * y);
}

function coordinatesCallback(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
};

module.exports = {
    calculateDistance,
    coordinatesCallback
};