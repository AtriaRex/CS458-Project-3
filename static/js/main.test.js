const { calculateDistance, findNearestSea } = require('./main');

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