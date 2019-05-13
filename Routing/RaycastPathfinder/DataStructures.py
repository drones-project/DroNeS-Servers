import numpy as np


def getter_setter_gen(name, type_):
    def getter(self):
        return getattr(self, "__" + name)

    def setter(self, value):
        if not isinstance(value, type_):
            raise TypeError("%s attribute must be set to an instance of %s"
                            % (name, type_))
        setattr(self, "__" + name, value)
    return property(getter, setter)


def auto_attr_check(cls):
    new_dct = {}
    for key, value in cls.__dict__.items():
        if isinstance(value, type):
            value = getter_setter_gen(key, value)
        new_dct[key] = value
    # Creates a new class, using the modified dictionary as the class dict:
    return type(cls)(cls.__name__, cls.__bases__, new_dct)


def vectorize(v: dict):
    return np.array([[v['x']], [v['y']], [v['z']]])


@auto_attr_check
class StaticObstacle(object):
    def __init__(self, obj: dict):
        self.position = vectorize(obj['position'])
        self.size = vectorize(obj['size'])
        self.orientation = vectorize(obj['orientation'])
        self.diag = obj['diag']
        self.dz = vectorize(obj['dz'])
        self.dx = vectorize(obj['dx'])
        self.mu = obj['mu']
        self.normals = []
        self.verts = []
        for i in range(len(obj['normals'])):
            self.normals.append(vectorize(obj['normals'][i]))
            self.verts.append(vectorize(obj['verts'][i]))
