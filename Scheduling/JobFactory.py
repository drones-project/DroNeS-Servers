import math
import random
import time
from .CostFunction import NaiveCostFunction

'''
Helper functions to generate random (lat, lon)s within a radius of another
(lat, lon)
'''
EARTH_RADIUS = 6371  # km
# 1 degree latitute in meters
ONE_DEG = EARTH_RADIUS * 2 * math.pi / 360 * 1000


def randomPointOnDisk(radius):
    r = radius * random.uniform(0, 1)
    theta = random.uniform(0, 1) * 2 * math.pi
    return [r * math.cos(theta), r * math.sin(theta)]


def randomCoords(coords, radius):
    dx, dy = randomPointOnDisk(radius)
    random_lat = coords[0] + (dy / ONE_DEG)
    random_lon = coords[1] + \
        (dx / (ONE_DEG * math.cos(coords[0] * math.pi / 180)))
    return { "x" : random_lat, "y" : random_lon }


'''
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
'''


class Job:
    def __init__(self):
        self.uid = None
        self.creation_time = None
        self.content = None
        self.cost_function = None
        self.pick_up = None
        self.destination = None


'''
The JobFactory class is a convenient interface that can be used to generate a
series of Jobs.

A JobFactory should be initialised with:

origin - A (lat, lon) coordinate that corresponds to a drone dispatch depot
range - An area described by a radius of <range> meters where
        the jobs (both pick-up and destination) will be limited to.

The potential contents, rewards and penalty of each job can be configured in a
`config.ini` file within the same directory as this file.

The only function that will need to be called by anyone using this class is
`generateJob()`. This function returns a Job object, whose instantaneous reward
can be determined by `Job['cost_function'].getReward(0)`.

The creation_time of the job is set to the UNIX timestamp (time.time()) at the
time when `generateJob()` was called.
'''


class JobFactory:
    def __init__(self, args):
        self.args = args
        self.counter = 0

    def generateJob(self):
        # Job creation
        job = Job()
        job.uid = self.__generateUID()
        job.creation_time = int(time.time())
        # Assigning item to job
        item = self.__getRandomItem()
        job.content = item['item']
        # Assigning cost function
        reward = random.randint(item['reward'][0], item['reward'][1])
        penalty = random.randint(item['penalty'][0], item['penalty'][1])
        valid_for = random.randint(item['valid_for'][0], item['valid_for'][1])
        job.cost_function = NaiveCostFunction(reward, penalty, valid_for)
        # Assigning pick_up and destination
        job.pick_up = randomCoords(self.args.origin, self.args.radius)
        job.destination = randomCoords(self.args.origin, self.args.radius)
        return job.__dict__

    # Ignores the given probability of the job, and picks one at random
    def __getRandomItem(self):
        return random.choice(self.args.job_items)

    def __generateUID(self):
        self.counter += 1
        return self.counter
