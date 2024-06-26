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

async function coordinatesCallbackSun(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    let distance = await getDistanceToSun(longitude, latitude);
    const distanceText = document.querySelector("#distanceToSun");
    distanceText.textContent = distance.distance;
};

// Coastline Points (CONSTANTS)
// A coordinate point [latitude, longitude] along the coastline is recorded approximately at every 200 kilometers
const MEDITERRANEAN_COAST = [[36.546061023012676, 27.992580643267388], [36.760197104206895, 28.474359777602103], [36.11533561538254, 29.70445245304643], [36.23056582484409, 30.48424334551555], [36.839329007785025, 30.67095384089555], [35.999936071227076, 32.81263305260654], [36.75139962447892, 34.71268691735531], [36.5399576643336, 35.50346078014093], [36.85690277004255, 36.06359226628069], [36.3367816873356, 35.83294988963485], [35.937727793484854, 35.92081365216666]];
const BLACKSEA_COAST = [[41.982821192008274, 28.029633854862027], [41.870594331067316, 27.98268057268274], [41.65515335101047, 28.08856419724509], [41.583942104114335, 28.14743326126836], [41.494645472233806, 28.278964213721338], [41.35695269014999, 28.6195763492276], [41.24584942915115, 29.013210011340448], [41.235448833358426, 29.256630562486066], [41.17069037637874, 29.59186180900656], [41.13947804403843, 30.149579313205777], [41.20962114056582, 30.271279671104253], [41.07399442203567, 30.967644721515512], [41.116157994139115, 31.291749900655873], [41.193967526410695, 31.38891265343625], [41.31757771107527, 31.404703611348623], [41.72130064879382, 32.300775461217654], [42.030029527543384, 33.34265297600757], [41.95182302083751, 34.227473795040964], [42.03355040880394, 35.060736390023976], [41.685389525689395, 35.41553085891405], [41.732840846288056, 35.960693814031856], [41.28738640192598, 36.35082430686373], [41.38117207964824, 36.6597203470144], [41.14838329203088, 37.16340881163762], [41.115103968595015, 37.78705250206235], [40.95552440280881, 38.11383364432322], [41.07981248538896, 39.1821684303618], [41.00113151639205, 39.745380600481894], [40.996987923759555, 40.327478027254756], [41.325717851911605, 41.2394792528753], [41.52126549686032, 41.5387651939991]];
const MARMARA_COAST = [[40.99991411320964, 28.976373273516856], [40.9548377253707, 28.823984560375834], [40.96916822947897, 28.73746386858295], [40.96294972972019, 28.60704109607491], [41.04995539368643, 28.353059907506577], [41.06651487519351, 28.21165416468216], [41.03753304678294, 28.031808025750024], [40.96425194829529, 27.944466376107925], [41.01027957253547, 27.754694950210023], [40.96469205407907, 27.524052573564177], [40.84020230912064, 27.452663266507216], [40.6155305638738, 27.17259752343739], [40.44444012265776, 26.697584057250197], [40.38800989831614, 26.73053296819944], [40.391238029089955, 27.025771202822625], [40.47387651700755, 27.280741239666668], [40.375528115759046, 27.323509273224204], [40.30229384130656, 27.534931451816192], [40.37134544166552, 27.86991204646847], [40.365070943742204, 29.058818583225957], [40.365070943742204, 29.058818583225957], [40.50088758547553, 28.765024127260403], [40.64476189807711, 28.99566650390625], [40.73218606084142, 29.937456208543267], [40.7613019581973, 29.35535878177052], [40.81457044493717, 29.323832689512642], [40.866489722917116, 29.24832476858694], [40.99781855269656, 29.011519581276502]];
const AEGEAN_COAST = [[40.709867482932594, 26.04817433173389], [40.60157487609736, 26.119563638790964], [40.60991131673373, 26.816982253886636], [40.325889291416146, 26.234884827113888], [40.04066711200239, 26.168987005215058], [39.453914061523804, 26.075631757525116], [39.553078081328685, 26.94077571654418], [39.277377099893776, 26.616778092208392], [38.89233880791285, 27.047443308871607], [38.71263778713752, 26.7454116251688], [38.37059699379965, 26.793904878629178], [38.64555457290465, 26.420483887869295], [38.077305555046415, 26.61817735356567], [37.90422932394058, 27.2222407209714], [36.956263585098654, 27.43186741679915], [37.026426716358166, 28.315996527274706], [36.666157252933694, 27.360478109742076], [36.546061023012676, 27.992580643267388]];


/** A function that takes in a coordinate and outputs the nearest sea to that coordinate. 
    The seas considered are the Mediterranean Sea, the Black Sea, the Sea of Marmara and the Aegean Sea 

 * lat (float) - The latitude of the coordinate
 * long (float) - The longitude of the coordinate
 * returns distanceToNearestSea (Object) - An object in the following format: 
                                            {
                                                sea (string): The name of nearest sea to the given coordinate, 
                                                distance (float): The distance, in kilometers, to the nearest sea from the given coordinates 
                                            }
*/
function getDistanceToNearestSea(lat, long) {
    let distanceToNearestSea = { distance: Infinity };

    function updateDistanceToNearestSea(coastline, name) {
        let line;
        let closestCoord;
        let distanceInKm;

        for (let idx = 1; idx < coastline.length; idx++) {
            // A line can be drawn using two coordinate points
            line = [coastline[idx - 1], coastline[idx]];

            // Finding the point on the line that is closest to the client's location 
            closestCoord = findClosestPointOnLine(line[0][0], line[0][1], line[1][0], line[1][1], lat, long);

            // Calculating the distance in kilometers between the closes point on the line and the client's location
            distanceInKm = calculateDistanceInKm(lat, long, closestCoord.lat, closestCoord.long);

            // Updating the distanceToNearestSea variable
            if (distanceInKm < distanceToNearestSea.distance) {
                distanceToNearestSea.distance = distanceInKm;
                distanceToNearestSea.sea = name;
                distanceToNearestSea.nearestPoint = closestCoord;
            }
        }
    }

    // Calculations for all coastlines
    updateDistanceToNearestSea(MEDITERRANEAN_COAST, "Mediterranean Sea");
    updateDistanceToNearestSea(BLACKSEA_COAST, "Black Sea");
    updateDistanceToNearestSea(MARMARA_COAST, "Sea of Marmara");
    updateDistanceToNearestSea(AEGEAN_COAST, "Aegean Sea");

    return distanceToNearestSea;
}

/** A function that returns the point on the line formed by the points (lat1, long1) and (lat2, long2) that is closest to the point (lat0, long0)  
    The curvature of the Earth's surface can be ignored since the distance between two coastline points is neglectable compared to the Earth's size 
    All inputs are of type float
 * returns closestPoint (Object) - An object in the following format: 
                                    {
                                        lat (float): The latitude of the closest point, 
                                        long (float): The longitude fo the closest point
                                    }
*/
function findClosestPointOnLine(lat1, long1, lat2, long2, lat0, long0) {
    const calculateLineEquation = (x1, y1, x2, y2) => {
        // Calculate the slope (m) and y-intercept (c) of the line passing through points A and B
        const m = (y2 - y1) / (x2 - x1);
        const c = y1 - m * x1;
        return { m, c };
    }
    const degToRad = (deg) => deg * (Math.PI / 180);
    const radToDeg = (rad) => rad * (180 / Math.PI);

    const lat1Rad = degToRad(lat1);
    const long1Rad = degToRad(long1)
    const lat2Rad = degToRad(lat2);
    const long2Rad = degToRad(long2)
    const lat0Rad = degToRad(lat0);
    const long0Rad = degToRad(long0)

    // Calculate the equation of the line passing through points A and B
    const { m, c } = calculateLineEquation(long1Rad, lat1Rad, long2Rad, lat2Rad);

    // Calculate the perpendicular distance from point C to the line
    const distanceToLine = (m * long0Rad - lat0Rad + c) / Math.sqrt(m ** 2 + 1);

    // Calculate the coordinates of the intersection point
    const xIntersect = (m * (lat0Rad - c) + long0Rad) / (m ** 2 + 1);
    const yIntersect = m * xIntersect + c;

    // Check if the intersection point lies between points A and B
    if ((xIntersect >= Math.min(long1Rad, long2Rad) && xIntersect <= Math.max(long1Rad, long2Rad)) &&
        (yIntersect >= Math.min(lat1Rad, lat2Rad) && yIntersect <= Math.max(lat1Rad, lat2Rad))) {
        return { lat: radToDeg(yIntersect), long: radToDeg(xIntersect) };
    } else {
        // If the intersection point is outside the line segment, return the closest endpoint
        const distToA = Math.sqrt((long1Rad - long0Rad) ** 2 + (lat1Rad - lat0Rad) ** 2);
        const distToB = Math.sqrt((long2Rad - long0Rad) ** 2 + (lat2Rad - lat0Rad) ** 2);
        return distToA < distToB ? { long: radToDeg(long1Rad), lat: radToDeg(lat1Rad) } : { long: radToDeg(long2Rad), lat: radToDeg(lat2Rad) };
    }
}

/** A function that calculates the distance (in kilometers) between two coordinate points 
    All inputs are of type float
 * returns distance (float) - the distance (in kilometers) between the coordinates 
*/
function calculateDistanceInKm(lat1, lon1, lat2, lon2) {
    const earthRadiusKm = 6371; // Radius of the Earth in kilometers

    // Convert latitude and longitude from degrees to radians
    const degToRad = (deg) => deg * (Math.PI / 180);
    const lat1Rad = degToRad(lat1);
    const lon1Rad = degToRad(lon1);
    const lat2Rad = degToRad(lat2);
    const lon2Rad = degToRad(lon2);

    // Calculate differences
    const latDiff = lat2Rad - lat1Rad;
    const lonDiff = lon2Rad - lon1Rad;

    // Calculate Haversine distance
    const a = Math.sin(latDiff / 2) * Math.sin(latDiff / 2) +
        Math.cos(lat1Rad) * Math.cos(lat2Rad) *
        Math.sin(lonDiff / 2) * Math.sin(lonDiff / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = earthRadiusKm * c;

    return distance;
}

module.exports = {
    coordinatesCallbackSun,
    getDistanceToSun,
    getDistanceToNearestSea,
    findClosestPointOnLine,
    calculateDistanceInKm
};