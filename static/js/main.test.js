const { calculateDistance, getNearestSea, getDistanceToSun } = require('./main');

// calculateDistance tests
test('distance between the same point should be zero', () => {
    let point = { lat: 1, lon: 2 };
    expect(calculateDistance(point, point)).toBe(0);
});

// findNearestSea tests
test('(43,34) should return BlackSea', () => {
    let point = { lat: 43, lon: 34 };
    expect(findNearestSea(point).sea).toBe('BlackSea');
});

test("distance to sun calculation validity check", () => {
    for (let i = 0; i < 5; i++) {
        let point = { lat: (Math.random() * 180) - 90, lon: (Math.random() * 360) - 180 };
        let distance = getDistanceToSun(point);
        distance = distance.distance;
        expect(distance).toBeGreaterThan(146000000); // 146 million km
        expect(distance).toBeLessThan(153000000); // 153 million km
    }
})