# License: Apache 2.0
# Author: Pierre-Elouan Rethore
# Email: pire@dtu.dk
#

import yaml
import numpy as np

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

    @property
    def wt_list(self):
        return [self.data['turbines'][wtn] for wtn in self.wt_names]

    @property
    def positions(self):
        return np.array([wt['position'] for wt in self.wt_list])
