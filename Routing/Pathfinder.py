import json
import numpy as np
import os
from abc import ABC, abstractmethod
from Routing.RaycastPathfinder.Router import (UpdateGameState, GetBuildings,
                                              Route)
from Routing.RaycastPathfinder.DataStructures import StaticObstacle


class Pathfinder(ABC):
    def __init__(self):
        # load the buildings
        file = os.path.join(os.path.dirname(__file__), 'buildings.json')
        self.buildings = []
        Buildings = json.load(open(file))['buildings']
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
    def __init__(self):
        super()
        GetBuildings(self.buildings)

    def getRoute(self, data):
        nfzs = []
        for nfz in data['noFlyZones']:
            nfzs.append(StaticObstacle(nfz))
        zeroes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        numDrones = len(data['dronePositions'])
        UpdateGameState(numDrones, zeroes, nfzs)

        origin = np.array([[data['origin']['x']],
                           [data['origin']['y']],
                           [data['origin']['z']]])
        destination = np.array([[data['destination']['x']],
                                [data['destination']['y']],
                                [data['destination']['z']]])

        tmp = Route(origin, destination, not data['onJob'])
        res = {'waypoints': []}
        for i in tmp:
            waypoint = {'x': i[0][0], 'y': i[1][0], 'z': i[2][0]}
            res['waypoints'].append(waypoint)
        return json.dumps(res)
