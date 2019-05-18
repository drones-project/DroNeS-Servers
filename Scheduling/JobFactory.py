import json
import math
import os
import random
import time
from .CostFunction import NaiveCostFunction


"""
Helper functions to generate random cartesian coordinates within a bounded
square
"""


def randomCartesian(coords, bounds):
    x = random.uniform(-bounds, bounds)
    z = random.uniform(-bounds, bounds)
    return {"x": coords[0] + x, "y": 0, "z": coords[1] + z}


def distance(point1, point2):
    return math.sqrt(
        (point1["x"] - point2["x"]) ** 2 + (point1["y"] - point2["y"]) ** 2
    )


def generateCoordsPair(coords, bounds, min_dist=None):
    first = randomCartesian(coords, bounds)
    second = randomCartesian(coords, bounds)
    if min_dist is not None:
        while distance(first, second) < min_dist:
            first = randomCartesian(coords, bounds)
            second = randomCartesian(coords, bounds)
    return first, second


"""
Helper functions to ensure that generated jobs do not end up on building tops
"""


class Scene:
    boundary = None


def __isClockwise(a, b, c):
    val = (b["z"] - a["z"]) * (c["x"] - b["x"]) - \
          (b["x"] - a["x"]) * (c["z"] - b["z"])
    return (val > 0)


def __willIntersect(a1, a2, b1, b2):
    o1 = __isClockwise(a1, a2, b1)
    o2 = __isClockwise(a1, a2, b2)
    o3 = __isClockwise(b1, b2, a1)
    o4 = __isClockwise(b1, b2, a2)
    return (o1 != o2 and o3 != o4)


def isContained(point):
    x, z = point["x"], point["z"]
    if (Scene.boundary is None):
        print("here")
        file = os.path.join(os.path.dirname(__file__), "boundary.json")
        with open(file) as f:
            Scene.boundary = json.load(f)
    p1 = {"x": x, "y": 0, "z": z}
    p2 = {"x": x + 10000000, "y": 0, "z": z}

    k = 0
    for i in range(len(Scene.boundary)):
        nxt = (i + 1) % len(Scene.boundary)
        if __willIntersect(Scene.boundary[i], Scene.boundary[nxt], p1, p2):
            k += 1
    return (k % 2) == 1


def generateContainedCoords(coords, bounds, min_dist=None):
    first, second = generateCoordsPair(coords, bounds, min_dist)
    while not isContained(first) or not isContained(second):
        first, second = generateCoordsPair(coords, bounds, min_dist)
    return first, second


"""
The Job class resembles the data structure of a job that is to be sent to the
simulation server. More attributes can be added in the future if it describes
a more realistic model for the simulation.

uid: Should be a unique ID that will be used to identify and display each job
     on a dashboard. Could be incrementing integers or Hash IDs.

creation_time: The time at which the job was created; this allows job
               generators to easily determine a sense of "real-time" if needed

content: The contents of the job, i.e. the item(s) that it is carrying.

cost_function: An instance of CostFunction that allows the job holder to
               determine immediate and projected reward values

pick_up: The coordinates where the item is to be picked up from (lat, lon)

destination: The coordinates where the item is to be delivered to (lat, lon)
"""


class Job:
    def __init__(self):
        self.uid = None
        self.creationTime = None
        self.content = None
        self.packageWeight = None
        self.packageXarea = None
        self.costFunction = None
        self.pickup = None
        self.destination = None
        self.droneUID = None


"""
The JobFactory class is a convenient interface that can be used to generate a
series of Jobs.

A JobFactory should be initialised with:

origin - A (lat, lon) coordinate that corresponds to a drone dispatch depot
range - An area described by a bounds of  meters where
        the jobs (both pick-up and destination) will be limited to.

The potential contents, rewards and penalty of each job can be configured in a
`config.ini` file within the same directory as this file.

The only function that will need to be called by anyone using this class is
`generateJob()`. This function returns a Job object, whose instantaneous reward
can be determined by `Job['cost_function'].getReward(0)`.

The creation_time of the job is set to the UNIX timestamp (time.time()) at the
time when `generateJob()` was called.
"""


class JobFactory:
    def __init__(self, args):
        self.args = args
        self.counter = 0
        if args.bound_check:
            self.point_generator = generateContainedCoords
        else:
            self.point_generator = generateCoordsPair

    def generateJob(self):
        # Job creation
        job = Job()
        job.uid = self.__generateUID()
        job.creationTime = int(time.time())
        # Assigning item to job
        item = self.__getRandomItem()
        job.content = item["item"]
        job.packageWeight = item["weight"]
        job.packageXarea = item["cross_sectional_area"]
        # Assigning cost function
        job.costFunction = NaiveCostFunction(
            item["reward"], item["penalty"], item["valid_for"]
        )
        # Assigning pick_up and destination
        job.pickup, job.destination = self.point_generator(
            self.args.origin, self.args.bounds, self.args.min_dist
        )
        return job

    # Ignores the given probability of the job, and picks one at random
    def __getRandomItem(self):
        return random.choice(self.args.job_items)

    def __generateUID(self):
        self.counter += 1
        return self.counter
