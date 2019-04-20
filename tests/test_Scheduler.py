import json
import os
import unittest
from Scheduling.Scheduler import FCFSScheduler
from Scheduling.Utils import mockArgs
from MockSimulation.MockSimulation import Simulation


# JSON schema loader
def load_schema(filename):
    file = os.path.join(os.path.dirname(__file__), "schemas/" + filename)
    with open(file) as f:
        return json.loads(f.read())


class SchedulerTest(unittest.TestCase):
    def setUp(self):
        self.mockArgs = mockArgs()
        self.scheduler = FCFSScheduler(self.mockArgs)
        self.mockdata = Simulation().getGeneric()

    def testNull(self):
        return


if __name__ == "__main__":
    unittest.main()
