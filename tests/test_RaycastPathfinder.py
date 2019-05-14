import json
import os
import unittest
from Routing.Pathfinder import SmartPathfinder
from jsonschema import validate

data = {
    "noFlyZones": [
        {
            "position": {"x": -191.05543518066, "y": 0.0, "z": 216.4875030518},
            "size": {"x": 708.145141601563, "y": 340.0, "z": 945.245910644531},
            "orientation": {"x": 0.0, "y": 0.0, "z": 0.0},
            "diag": 1181.083984375,
            "dz": {"x": 0.0, "y": 0.0, "z": 472.6229553222656},
            "dx": {"x": 354.07257080078127, "y": 0.0, "z": 0.0},
            "mu": 0.0,
            "normals": [
                {"x": 0.0, "y": 0.0, "z": 1.0},
                {"x": 1.0, "y": 0.0, "z": 0.0},
                {"x": 0.0, "y": 0.0, "z": -1.0},
                {"x": -1.0, "y": 0.0, "z": 0.0},
            ],
            "verts": [
                {"x": 163.0171356201172, "y": 0.0, "z": 689.1104736328125},
                {"x": 163.0171356201172, "y": 0.0, "z": -256.13543701171877},
                {"x": -545.1279907226563, "y": 0.0, "z": -256.13543701171877},
                {"x": -545.1279907226563, "y": 0.0, "z": 689.1104736328125},
            ],
        }
    ],
    "dronePositions": [
        {"x": -317.0, "y": 240.0, "z": -292.0}
    ],
    "drone": 0,
    "origin": {"x": -317.0, "y": 240.0, "z": -292.0},
    "destination": {"x": 478.0, "y": 240.0, "z": 560.0},
    "onJob": True
}

# these values have been calculated ahead of time and proven to be analytically
# accurate
correct_waypoints = {
    "waypoints": [
        {"x": -317.0, "y": 250.0, "z": -292.0},
        {"x": -79.73920849557521, "y": 250.0, "z": -373.7264107651813},
        {"x": 164.81585230803734, "y": 250.0, "z": -258.53639895989653},
        {"x": 329.4790446087086, "y": 250.0, "z": -12.514732474939773},
        {"x": 399.5147056812126, "y": 250.0, "z": 152.47904483356106},
        {"x": 480.1757134342077, "y": 250.0, "z": 342.3121682484161},
        {"x": 478.0, "y": 250.0, "z": 560.0},
    ]
}

pathfinder = SmartPathfinder('../tests/extras/stubBuildings.json')


class RaycastPathfinderTest(unittest.TestCase):
    def setUp(self):
        pass

    def load_schema(self, filename):
        file = os.path.join(os.path.dirname(__file__), "schemas/" + filename)
        with open(file) as f:
            return json.loads(f.read())

    def testGettingRouteFromPathfinder(self):
        routes = eval(pathfinder.getRoute(data))
        self.assertDictEqual(routes, correct_waypoints)
        return

    def testRouterResponseMatchesSchema(self):
        routes = eval(pathfinder.getRoute(data))
        validate(routes, self.load_schema('route.json'))
        return


if __name__ == '__main__':
    unittest.main()
