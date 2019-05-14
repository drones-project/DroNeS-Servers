import numpy as np
import math
from .DataStructures import StaticObstacle
from .Utils import MinHeap, normalize, sqrMagnitude, distance, magnitude, dot

_Buildings = []
_NoFlys = None
_maxAlt = 250.0
_minAlt = 150.0
_altDiv = 10
_buildingDiv = 30
_R_a = 200
_R_d = 3
_epsilon = 0.001
_hubAlt = [500, 510]
_droneCount = None
_altitudes = None
_assigned = None
_origin = None
_destination = None


def altitudes():
    global _altitudes
    global _assigned
    if _altitudes is None:
        _altitudes = [None] * int((_maxAlt - _minAlt) / _altDiv + 1)
        _assigned = [0] * int((_maxAlt - _minAlt) / _altDiv + 1)
        for i in range(len(_altitudes)):
            _altitudes[i] = _minAlt + i * _altDiv
    return _altitudes


def HashVector(v: np.ndarray):
    return hash('%.3f%.3f' % (v[0], v[2]))


def GetBuildings(o: list):
    added = 0
    i = 0
    altitudes()
    while (added < len(o)):
        _Buildings.append([])
        # Split _Buildingsinto buckets of 30m interval in height, e.g. 0-30m,
        # 30-60m, 60-90m, etc.
        for j in range(len(o)):
            lower = i * _buildingDiv
            upper = (i + 1) * _buildingDiv
            if (o[j].size[1] < upper and o[j].size[1] >= lower):
                _Buildings[i].append(o[j])
                added += 1
        i += 1
    return  # Initialised presimulation


def CountAt(i: int, dronePositions: list):
    count = 0
    for j in range(len(dronePositions)):
        if _altitudes[i] - _altDiv / 2 < dronePositions[j]["y"] < \
           _altitudes[i] + _altDiv / 2:
            count += 1
    return count


def UpdateGameState(dronePositions: list, noflys: list):
    global _droneCount, _NoFlys
    _droneCount = len(dronePositions)  # total number of drones in service
    _NoFlys = noflys

    for i in range(len(_assigned)):
        _assigned[i] = CountAt(i, dronePositions)  # Number of jobs completed
        # at the current altitude. Alternatively set a timer have it reduce
        # periodically


def RotationY(theta: float):
    theta *= math.pi / 180
    return np.array(
        [
            [math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)]
        ]
    )


def ChooseAltitude(origin: np.ndarray, dest: np.ndarray):
    max = 0
    start = 0 if (dest - origin)[2] > 0 else 1  # Northbound => even, else odd
    maxIndex = len(_assigned) - 1
    for i in range(start, len(_assigned), 2):
        # maximise altitude, minimize traffic, + 1 to prevent singularity
        tmp = altitudes()[i] / _maxAlt / (_assigned[i] / _droneCount + 1)
        if tmp > max:
            max = tmp
            maxIndex = i
    _assigned[maxIndex] += 1
    return maxIndex


def _getPerp(dir: np.ndarray):
    return np.dot(RotationY(90), dir)


def Route(origin: np.ndarray, dest: np.ndarray, returnToHub: bool):
    global _origin, _destination
    _origin = origin
    _destination = dest  # Cached in global/static var for later use
    _origin[1] = 0
    _destination[1] = 0
    if returnToHub:
        alt = _hubAlt[0 if (dest - origin)[2] > 0 else 1]
    else:
        alt = altitudes()[ChooseAltitude(origin, dest)]

    try:
        waypoints = _navigate(_origin, _destination, alt)
        for i in range(len(waypoints)):
            waypoints[i][1] = alt
        return waypoints
    except Exception as e:
        print(e)
        return


def _blockingBuildings(start: np.ndarray, end: np.ndarray, alt: float):
    direction = end - start
    # sorted by normlized projected distance
    obstacles = MinHeap(key=lambda obs: obs.mu)
    # _R_a is the corridor half-width
    perp = normalize(_getPerp(direction)) * _R_a
    # the building list index where we should start
    startIndex = int(alt / _buildingDiv)
    for i in range(startIndex, len(_Buildings), 1):
        for j in range(len(_Buildings[i])):
            obs = _Buildings[i][j]
            if obs.size[1] > alt - _altDiv / 2:
                # normalized projected distance
                mu = dot(obs.position - start, direction) / \
                    sqrMagnitude(direction)
                # normalized perpendicular distance
                nu = dot(start - obs.position, perp) / sqrMagnitude(perp)
                if (-1 <= nu <= 1) and \
                   (0 <= mu <= 1 + _R_a / magnitude(direction)):
                    obs.mu = mu
                    obstacles.push(obs)
    return obstacles


def _findIntersect(obs: StaticObstacle, start: np.ndarray, end: np.ndarray):
    dir = end - start
    _dir = normalize(dir)
    def path(m): return start + m * dir  # 0 < mu < 1
    numberOfIntersects = 0
    mu = [None] * 4
    indices = [-1, -1]
    for j in range(len(obs.normals)):
        # if heading not parallel to surface
        if abs(dot(_dir, obs.normals[j])) > _epsilon:
            # solve ray-plane intersection: f(mu).n = P0.n
            # where . is dot product, n is plane normal, P0 is a point on the
            # plane, and f(mu) is the ray equation
            mu[j] = dot(obs.verts[j] - start, obs.normals[j]) / \
                dot(dir, obs.normals[j])
            if (distance(path(mu[j]), obs.position) < obs.diag / 2) and \
               (0 < mu[j] <= 1):
                indices[numberOfIntersects] = j
                numberOfIntersects += 1

    if numberOfIntersects > 1 and mu[indices[1]] < mu[indices[0]]:
        indices[0], indices[1] = indices[1], indices[0]
    return numberOfIntersects, indices


def _findOtherWaypoint(obs: StaticObstacle, start: np.ndarray,
                       exclude: np.ndarray):
    for vert in obs.verts:
        point = vert + _R_d * normalize(vert - obs.position)
        x = magnitude(point - exclude)
        if magnitude(point - start) > _epsilon and x > _epsilon and \
           x < obs.diag:
            return point
    return start


def _isContained(obs: StaticObstacle, p: np.ndarray):
    for i in range(len(obs.verts)):
        if (dot(p - obs.verts[i], obs.normals[i]) > 0):
            return False
    return True


def _findWaypoint(obs: StaticObstacle, start: np.ndarray, end: np.ndarray,
                  indices: list):
    global _NoFlys
    _dir = normalize(end - start)
    waypoint = None
    if indices[1] == -1:
        # If only one intersetion detected sets the way point near the vertex
        # clockwise from the intersection point
        newend = end + obs.diag * _dir
        num, indi = _findIntersect(obs, start, newend)
        if num > 0:
            return _findWaypoint(obs, start, newend, indi)

    if abs(indices[1] - indices[0]) in [1, 3]:
        # Indices previously swapped to ensure 1 is bigger than 0
        # Adjacent faces intersection
        if (abs(indices[1] - indices[0]) == 1):
            j = indices[1] if (indices[1] < indices[0]) else indices[0]
        else:
            j = 3

        a = obs.verts[j] + _R_d * normalize(obs.verts[j] - obs.position)
        b = obs.verts[(j + 1) % 4] + _R_d * \
            normalize(obs.verts[(j + 1) % 4] - obs.position)
        waypoint = a if magnitude(a - start) > _epsilon else b
    else:
        # opposite faces intersection
        a = obs.verts[indices[0]] + _R_d * \
            normalize(obs.verts[indices[0]] - obs.position)

        b = obs.verts[(indices[1] + 1) % 4] + _R_d * \
            normalize(obs.verts[(indices[1] + 1) % 4] - obs.position)

        if magnitude(a - start) > _epsilon and magnitude(b - start) > _epsilon:
            # Gets the waypoint with the smallest deviation angle from the path
            if abs(dot(normalize(a - start), _dir)) > \
               abs(dot(normalize(b - start), _dir)):
                waypoint = a
            else:
                waypoint = b
        else:
            # I think its possible for opposite face intersection to obtain the
            # same point again but I might be wrong, this is to prevent it
            waypoint = (b, a)[magnitude(a - start) > _epsilon]
    for nfz in _NoFlys:
        if (_isContained(nfz, waypoint)):
            waypoint = _findOtherWaypoint(obs, start, waypoint)

    return waypoint


def _navigate(start: np.ndarray, end: np.ndarray, alt: float):
    waypoints = [start]
    dir = end - start
    if magnitude(dir) < _epsilon:  # if start = end, then return start
        return waypoints

    # Find all the buildings sorted by distance from the startpoint in a
    # 200m-wide corridor
    buildings = _blockingBuildings(start, end, alt)
    possibilities = MinHeap(
        key=lambda a: dot(a - start, dir) / sqrMagnitude(dir))

    # To store and flag any deadend waypoints to be redirected, I believe
    # Python has a set() which is equivalent waypoints are hashed
    errorPoints = set()

    intersected = False

    for obs in _NoFlys:
        intersects, indices = _findIntersect(obs, start, end)
        # For each NFZ find the number intersects and index of vertices/normals
        if (intersects > 0):
            intersected = True
            v = _findWaypoint(obs, start, end, indices)
            possibilities.push(v)
            if indices[1] == -1:
                errorPoints.add(HashVector(v))

    # 5 is arbitrary but loop through a few in case some buildings overlap
    k = 0
    while (buildings.size() > 0 and k < 5):
        obs = buildings.pop()
        intersects, indices = _findIntersect(obs, start, end)
        if intersects > 0:
            k += 1
            intersected = True
            v = _findWaypoint(obs, start, end, indices)
            possibilities.push(v)
            if indices[1] == -1:
                errorPoints.add(v)

    if intersected:
        nxt = possibilities.pop()
        possibilities.clear()
        buildings.clear()
        li = _navigate(start[:], nxt[:], alt)  # pass args by value!
        for item in li[1:]:
            waypoints.append(item)
        if len(errorPoints) > 0 and HashVector(nxt) in errorPoints:
            end = _destination
        li = _navigate(li[len(li) - 1][:], end[:], alt)  # pass args by value!
        for item in li[1:]:
            waypoints.append(item)
    else:
        waypoints.append(end)
    return waypoints
