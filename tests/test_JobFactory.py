import ast
import json
import os
import unittest
from Scheduling.JobFactory import JobFactory, Job
from Scheduling.Utils import mockArgs, Encoder
from jsonschema import validate


def load_schema(filename):
    file = os.path.join(os.path.dirname(__file__), "schemas/" + filename)
    with open(file) as f:
        return json.loads(f.read())


class JobFactoryTest(unittest.TestCase):
    def setUp(self):
        self.args = mockArgs()
        self.factory = JobFactory(self.args)

    def testGenerateJobCreatesAJob(self):
        job = self.factory.generateJob()
        assert(type(job) == Job)
        return

    def testJobUIDIsSequential(self):
        job = self.factory.generateJob()
        assert(job.uid == 1)
        job = self.factory.generateJob()
        assert(job.uid == 2)
        job = self.factory.generateJob()
        assert(job.uid == 3)
        return

    def testJobObjectIsConsistentWithSchema(self):
        job = self.factory.generateJob()
        # convert to json string then back to dict
        job = eval(json.dumps(job, cls=Encoder))
        validate(job, load_schema('job.json'))



if __name__ == "__main__":
    unittest.main()
