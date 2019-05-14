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
        self.generator_params = 0.1


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

    args.origin = eval(config['Settings']['dispatch_origin'])
    args.bounds = eval(config['Settings']['dispatch_bounds'])
    args.generator_params = eval(config['Job Generator']['params'])

    return args
