import json
import os
import unittest
from jsonschema import validate
from Scheduling.Scheduler import FCFSScheduler
from MockSimulation.MockSimulation import Simulation


class mockArgs:
    def __init__(self):
        self.job_items = [
            {
                "item": "mock_item",
                "reward": [0, 0],
                "penalty": [0, 0],
                "valid_for": [0, 0],
            }
        ]
        self.origin = [0, 0]
        self.radius = 3000
        self.generator_params = 0.1


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

    def testStartandStop(self):
        self.assertFalse(self.scheduler.generator.running)
        self.scheduler.start()
        self.assertTrue(self.scheduler.generator.running)
        self.scheduler.stop()
        self.assertFalse(self.scheduler.generator.running)

    def testGetJob(self):
        schema = load_schema("job.json")
        job = self.scheduler.getJob(self.mockdata)
        self.assertEqual(job, "{}")
        self.scheduler.start()
        self.scheduler.stop()
        job = self.scheduler.getJob(self.mockdata)

        # job is returned as a string and therefore converted to JSON format.
        validate(json.loads(job), schema)


if __name__ == "__main__":
    unittest.main()
