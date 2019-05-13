import heapq
import numpy as np


VEC_RIGHT = np.array((1, 0, 0))
VEC_FWD = np.array((0, 0, 1))


class MinHeap(object):

    def __init__(self, initial=None, key=lambda x: x):
        self.key = key
        self._size = 0
        if initial:
            self._data = [(key(item), item) for item in initial]
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), item))
        self._size += 1

    def pop(self):
        self._size -= 1
        return heapq.heappop(self._data)[1]

    def clear(self):
        self._size = 0
        self._data = []

    def size(self):
        return self._size


def dot(a: np.ndarray, b: np.ndarray):
    return np.dot(np.transpose(a), b)[0][0]


def normalize(v: np.ndarray):
    return v / np.linalg.norm(v)


def magnitude(v: np.ndarray):
    return np.linalg.norm(v)


def sqrMagnitude(v: np.ndarray):
    return np.linalg.norm(v)**2


def distance(a: np.ndarray, b: np.ndarray):
    return np.linalg.norm(a - b)
