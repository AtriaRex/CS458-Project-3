const { calculateDistance } = require('./main');

test('distance between the same point should be zero', () => {
    let point = { x: 1, y: 2 };
    expect(calculateDistance(point, point)).toBe(0);
});