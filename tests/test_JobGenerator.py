import json
import os
import queue
import unittest
from Scheduling.JobGenerator import PoissonGenerator
from Scheduling.Utils import mockArgs


# JSON schema loader
def load_schema(filename):
    file = os.path.join(os.path.dirname(__file__), "schemas/" + filename)
    with open(file) as f:
        return json.loads(f.read())


class JobGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.mockArgs = mockArgs()
        self.running = False
        self.queue = queue.Queue()
        self.generator = PoissonGenerator(self.mockArgs, self.queue)

    def testNull(self):
        return


if __name__ == "__main__":
    unittest.main()
