import json
import random


class Pathfinder:
    @staticmethod
    def getRoute(data):
        waypoints = {"waypoints": [{"x": random.randint(-1000, 1000),
                                    "y": random.randint(-1000, 1000),
                                    "z": random.randint(-1000, 1000)},
                                   {"x": random.randint(-1000, 1000),
                                    "y": random.randint(-1000, 1000),
                                    "z": random.randint(-1000, 1000)}]}
        return json.dumps(waypoints)
