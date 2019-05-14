import json
import numpy as np
import os
from abc import ABC, abstractmethod
from Routing.RaycastPathfinder.Router import (UpdateGameState, GetBuildings,
                                              Route)
from Routing.RaycastPathfinder.DataStructures import StaticObstacle


class Pathfinder(ABC):
    def __init__(self):
        self.buildings = []

    def loadBuildings(self, filename):
        file = os.path.join(os.path.dirname(__file__), filename)
        with open(file) as f:
            Buildings = json.load(f)['buildings']
        for building in Buildings:
            self.buildings.append(StaticObstacle(building))

    @abstractmethod
    def getRoute(self, data):
        pass


class DumbPathfinder(Pathfinder):
    def getRoute(self, data):
        waypoints = {"waypoints": [{"x": data['destination']['x'],
                                    "y": 400,
                                    "z": data['destination']['z']}]}
        return json.dumps(waypoints)


class SmartPathfinder(Pathfinder):
    def __init__(self, filename='buildings.json'):
        super().__init__()
        self.loadBuildings(filename)
        GetBuildings(self.buildings)

    def getRoute(self, data):
        if len(data) == 0:
            return json.dumps({'waypoints': []})
        self.nfzs = [StaticObstacle(nfz) for nfz in data['noFlyZones']]
        UpdateGameState(data['dronePositions'], self.nfzs)

        origin = np.array([[data['origin']['x']],
                           [data['origin']['y']],
                           [data['origin']['z']]])
        destination = np.array([[data['destination']['x']],
                                [data['destination']['y']],
                                [data['destination']['z']]])

        tmp = Route(origin, destination, not data['onJob'])
        res = {'waypoints': []}
        for i in tmp:
            waypoint = {'x': float(i[0][0]),
                        'y': float(i[1][0]),
                        'z': float(i[2][0])}
            res['waypoints'].append(waypoint)
        return json.dumps(res)
