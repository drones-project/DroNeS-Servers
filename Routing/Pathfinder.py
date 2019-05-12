import json
import os


class Pathfinder:
    def __init__(self):
        # load the buildings
        file = os.path.join(os.path.dirname(__file__), 'buildings.json')
        self.buildings = json.load(open(file))

    def getRoute(self, data):
        waypoints = {"waypoints": [{"x": data['destination']['x'],
                                    "y": 250,
                                    "z": data['destination']['y']}]}
        return json.dumps(waypoints)
