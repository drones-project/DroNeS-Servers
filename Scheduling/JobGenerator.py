import math
import random
from abc import ABC, abstractmethod
from threading import Timer
from .JobFactory import JobFactory


'''
A JobGenerator leverages on the JobFactory class to autonomously (and
asynchronously) generate jobs that are to be scheduled by the scheduler.

JobGenerators will receive:

queue - A Queue.Queue object sent from the scheduler where the jobs generated
        will be queued in a FIFO. This queue can be later popped and sorted in
        an external array before being sent to the simulation server

The JobGenerator object can be started using the `.start()` method, and stopped
with the `.stop()` method
'''


# Simple base class that all other generators should inherit from.
# The `_sleep` function should be overriden in concrete classes to generate
# sleep times representative of whatever model is being implemented
class JobGenerator(ABC):
    def __init__(self, args, queue):
        self.args = args
        self.factory = JobFactory(args)
        self.queue = queue
        # threading variables
        self._should_continue = False
        self.is_running = False
        self.timescale = 0
        self.thread = None

    def _fetch_job(self):
        self.is_running = True
        job = self.factory.generateJob()
        self.queue.put(job)
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        # Code could have been running when cancel was called.
        if self._should_continue and self.timescale > 0:
            sleep_time = self._sleep() / self.timescale
            self.thread = Timer(sleep_time, self._fetch_job)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()

    def stop(self):
        if self.thread is not None:
            # Just in case thread is running and cancel fails.
            self.thread.cancel()
        self._should_continue = False

    def updateTimescale(self, timescale):
        if self.thread is not None:
            self.thread.cancel()
        self.timescale = timescale
        if self._should_continue:
            self._start_timer()

    @abstractmethod
    def _sleep(self):
        pass


# A JobGenerator that models as a Poisson process. The generator needs to be
# given a parameter that corresponds to the lambda parameter in a Poisson
# distribution.
# This should be 1/N where N is the average number of occurances per second
class PoissonGenerator(JobGenerator):
    def __init__(self, args, queue):
        super().__init__(args, queue)

    def _sleep(self):
        return - math.log(random.uniform(0, 1)) / self.args.generator_param
