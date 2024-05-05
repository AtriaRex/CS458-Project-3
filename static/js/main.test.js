const { calculateDistance, findNearestSea } = require('./main');

// calculateDistance tests
test('distance between the same point should be zero', () => {
    let point = { x: 1, y: 2 };
    expect(calculateDistance(point, point)).toBe(0);
});

test('distance between the (0, 0) and (4, 3) should be 5', () => {
    let point0 = { x: 0, y: 0 };
    let point1 = { x: 4, y: 3 };

    expect(calculateDistance(point0, point1)).toBe(5);
});

// findNearestSea tests
test('(43,34) should return BlackSea', () => {
    let point = { x: 43, y: 34 };
    expect(findNearestSea(point).sea).toBe('BlackSea');
});