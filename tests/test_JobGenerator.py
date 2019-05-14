import queue
import time
import unittest
from Scheduling.JobGenerator import PoissonGenerator
from Scheduling.Utils import mockArgs


class JobGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.mockArgs = mockArgs()
        self.queue = queue.Queue()
        self.generator = PoissonGenerator(self.mockArgs, self.queue)

    def testTimescaleInitiallyZero(self):
        assert(self.generator.timescale == 0)
        return

    def testStartingWithZeroTimescaleDoesNothing(self):
        self.generator.start()
        assert(self.generator.thread is None)
        return

    def testCanChangeTimescale(self):
        self.generator.start()
        self.generator.updateTimescale(1)
        assert(self.generator.timescale == 1)
        self.generator.updateTimescale(2)
        assert(self.generator.timescale == 2)
        self.generator.stop()
        return

    def testUpdatingTimescaleStartsTheGenerator(self):
        self.generator.start()
        self.generator.updateTimescale(1)
        assert(self.generator.thread is not None)
        self.generator.stop()
        return

    def testStopCancelsTheGeneratorThread(self):
        self.generator.updateTimescale(1)
        self.generator.start()
        assert(self.generator.thread is not None)
        self.generator.stop()
        assert(self.generator.thread.finished._flag is True)
        return

    def testGeneratorCreatesAJobEventually(self):
        self.generator.start()
        self.generator.updateTimescale(100)
        timeout = 0
        while self.queue.empty() and timeout < 20:
            time.sleep(0.5)
            timeout += 1
        assert(self.queue.qsize() > 0)
        self.generator.stop()
        return


if __name__ == "__main__":
    unittest.main()
