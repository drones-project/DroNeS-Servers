import configparser
import os
from json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Args:
    def __init__(self):
        self.job_items = []
        self.origin = None
        self.radius = None
        self.generator_params = None


def getArgs():
    args = Args()
    config = configparser.ConfigParser()
    file = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(file)

    for s in config.sections():
        if not s.startswith('Job:'):
            continue
        entry = {'item': s[len('Job:'):],
                 'weight': float(config[s]['Weight']),
                 'reward': float(config[s]['Reward']),
                 'penalty': float(config[s]['Penalty']),
                 'valid_for': float(config[s]['Valid_Time'])}
        args.job_items.append(entry)

    args.origin = eval(config['Settings']['dispatch_origin'])
    args.radius = eval(config['Settings']['dispatch_radius'])
    args.generator_params = eval(config['Job Generator']['params'])

    return args
