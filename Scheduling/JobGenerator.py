import math
import random
import time
from abc import ABC, abstractmethod
from threading import Thread
from .JobFactory import JobFactory

'''
A JobGenerator leverages on the JobFactory class to autonomously (and
asynchronously) generate jobs that are to be scheduled by the scheduler.

JobGenerators will receive:

queue - A Queue.Queue object sent from the scheduler where the jobs generated
        will be queued in a FIFO. This queue can be later popped and sorted in
        an external array before being sent to the simulation server

The JobGenerator object can be started using the `.start()` method, and will
continue running until `.stop()` is called.
'''


# Simple base class that all other generators should inherit from.
# The `add_to_queue` function should be overriden in concrete classes, and
# should implement their own checks against the self.running attribute to start
# and stop the thread
class JobGenerator(ABC):
    def __init__(self, args, queue):
        self.args = args
        self.factory = JobFactory(args)
        self.running = False
        self.queue = queue

    def start(self):
        if not self.running:
            self.running = True
            self.t = Thread(target=self.generator_thread)
            self.t.start()

    def stop(self):
        self.running = False

    @abstractmethod
    def generator_thread():
        pass


# A JobGenerator that models as a Poisson process. The generator needs to be
# given a parameter `n` that corresponds to the lambda parameter in a Poisson
# distribution.
# This should be 1/N where N is the average number of occurances per second
class PoissonGenerator(JobGenerator):
    def __init__(self, args, queue):
        super().__init__(args, queue)

    def generator_thread(self):
        while self.running:
            job = self.factory.generateJob()
            self.queue.put(job)
            sleep_time = - math.log(random.uniform(0, 1)) / \
                self.args.generator_params
            time.sleep(sleep_time)
