import json
import os
import queue
import unittest
from jsonschema import validate
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

    def testStartandStop(self):
        self.assertFalse(self.generator.running)
        self.generator.start()
        self.assertTrue(self.generator.running)
        self.generator.stop()
        self.assertFalse(self.generator.running)

    def testAdd_To_Queue(self):
        schema = load_schema("job.json")
        self.generator.start()
        self.generator.stop()
        job = self.generator.queue.get()
        # we serialise the cost function object before sending it off
        job["cost_function"] = job["cost_function"].__dict__
        validate(job, schema)


if __name__ == "__main__":
    unittest.main()
