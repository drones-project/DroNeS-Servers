import json
import os
import unittest
from Scheduling.JobFactory import JobFactory
from Scheduling.Utils import mockArgs


def load_schema(filename):
    file = os.path.join(os.path.dirname(__file__), "schemas/" + filename)
    with open(file) as f:
        return json.loads(f.read())


class JobFactoryTest(unittest.TestCase):
    def setUp(self):
        self.args = mockArgs()
        self.factory = JobFactory(self.args)

    def testNull(self):
        return


if __name__ == "__main__":
    unittest.main()
