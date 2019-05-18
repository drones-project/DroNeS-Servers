import json
import queue
import time
from abc import ABC, abstractmethod
from .JobGenerator import PoissonGenerator
from .Utils import Encoder, getArgs

"""
A JobScheduler is the final component of scheduling and that serves as the
interface between the simulation server and the web server.

It creates an instance of a JobGenerator class, and priotises the incoming
jobs as defined by the Scheduler implementation whenever a request for a job
is made.

* Attention has to be made to ensure that the jobs are scheduled in a timely
and sensical manner such that it is able to process the jobs quicker than they
are generated.

Methods:
  .start() - Starts the JobGenerator component
  .stop()  - Stops the JobGenerator component
  .getJob(data) - Fetches the next scheduled job. `data` will contain the
                  simulation data, including number of idle drones (so a buffer
                  of emergency drones can be reserved. A schema of can be found
                  in the schema folder.
"""


# Simple base class that all other schedulers should inherit from.
# The `getJob(data)` function should be overriden in concrete classes, and
# the order of when the jobs are processed, scheduled and returned should be
# considered.
class JobScheduler(ABC):
    def __init__(self, args):
        self.args = args
        self.sortedQueue = []
        self.backlog = queue.Queue()
        if args.generator == "Poisson":
            self.generator = PoissonGenerator(args, self.backlog)
        # default to poisson generator
        else:
            self.generator = PoissonGenerator(args, self.backlog)

    def start(self):
        self.generator.start()

    def stop(self):
        self.generator.stop()

    @abstractmethod
    def updateTimescale(self, timescale):
        pass

    @abstractmethod
    def getJob(self, data):
        pass


# A basic first-come-first-serve scheduler.
class FCFSScheduler(JobScheduler):
    def __init__(self, args=None):
        if args is None:
            args = getArgs()
        super().__init__(args)

    def getJob(self, data):
        self.__processQueue()
        if len(self.sortedQueue) > 0:
            job = self.sortedQueue.pop(0)
            job = self.__ageJob(job)
            job.droneUID = data["requester"]
        else:
            job = {}
        return json.dumps(job, cls=Encoder)

    def updateTimescale(self, timescale):
        self.__processQueue()
        for job in self.sortedQueue:
            self.__ageJob(job)
        self.generator.updateTimescale(timescale)

    def __processQueue(self):
        # empty the backlog queue into the 'sorted' queue
        for i in range(self.backlog.qsize()):
            job = self.backlog.get()
            self.sortedQueue.append(job)

    def __ageJob(self, job):
        # 'ages' a job
        job.costFunction.valid_time -= (
            int(time.time()) - job.creationTime
        ) * self.generator.timescale
        job.creationTime = int(time.time())
        return job
