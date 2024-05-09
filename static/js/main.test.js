const { getDistanceToNearestSea, findClosestPointOnLine, calculateDistanceInKm } = require('./main');

test("should not return lakes", () => {
    expect(getDistanceToNearestSea(39.4, 38.48).sea).not.toBe('Hazar Lake');

    expect(getDistanceToNearestSea(42.91, 38.61).sea).not.toBe('Van Lake');
})

test("maximum distance of nearest sea", () => {
    for (let i = 0; i < 100; i++) {
        let longitude = Math.random() * 9 + 26;
        let latitude = Math.random() * 6 + 36;
        let distance = getDistanceToNearestSea(latitude, longitude);
        expect(distance.distance).toBeLessThan(500); // 500 km
    }
})


test("correct sea returned", () => {
    let point = { lat: 39.71, lon: 41 };
    expect(getDistanceToNearestSea(point.lat, point.lon).sea).toBe('Black Sea');

    point = { lat: 30.70, lon: 36.39 };
    expect(getDistanceToNearestSea(point.lat, point.lon).sea).toBe('Mediterranean Sea');

    point = { lat: 38.30, lon: 26.51 };
    expect(getDistanceToNearestSea(point.lat, point.lon).sea).toBe('Aegean Sea');

    point = { lat: 40.18, lon: 29.06 };
    expect(getDistanceToNearestSea(point.lat, point.lon).sea).toBe('Sea of Marmara');
})