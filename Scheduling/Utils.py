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
        self.bounds = None
        self.generator_params = None


class mockArgs:
    def __init__(self):
        self.job_items = [
            {
                "item": "mock_item",
                "weight": 10,
                "reward": 10,
                "penalty": 10,
                "valid_for": 10,
                "cross_sectional_area": 10
            }
        ]
        self.origin = [0, 0]
        self.bounds = 3000
        self.min_dist = 500
        self.bound_check = True
        self.scheduler = 'FCFS'
        self.generator = 'Poisson'
        self.generator_param = 0.1


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
                 'valid_for': float(config[s]['Valid_Time']),
                 'cross_sectional_area': float(config[s]['Cross_Section_Area'])
                 }
        args.job_items.append(entry)

    settings = config['Settings']
    args.origin = eval(settings.get('dispatch_origin', '[0, 0]'))
    args.bounds = eval(settings.get('dispatch_bounds', '1000'))
    args.min_dist = eval(settings.get('min_distance', 'None'))
    args.bound_check = eval(settings.get('bound_check', 'True'))

    args.scheduler = settings.get('scheduler', 'FCFS')
    args.generator = settings.get('generator', 'Poisson')
    args.generator_param = eval(settings.get('generator_param', '1'))

    return args
