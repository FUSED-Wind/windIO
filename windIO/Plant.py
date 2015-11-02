# License: Apache 2.0
# Author: Pierre-Elouan Rethore
# Email: pire@dtu.dk
#

import yaml

class WTLayout(object):
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'r') as f:
            data = yaml.load(f)
        self.wt_names = list(data['turbines'].keys())
        self.wt_names.sort()
        self.data = data

    def __getitem__(self, a):
        return self.data[a]

    def __setitem__(self, a, b):
        self.data[a] = b
