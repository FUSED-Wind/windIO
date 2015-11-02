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
        # Check that the data is correctly organized
        self.check_structure(data)

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

    def check_structure(self, data):
        """Check that the data is conform to the standard
        Parameters
        ----------
        data:   dictionary
                The data to check
        """

        # Check that all the keys are defined in the base
        base = ['turbines', 'transformers', 'metmasts', 'turbine_types']
        for k, v in data.items():
            if not k in base:
                raise KeyError('key: {0} not recognized. It should be one of those keys {1}'.format(k, base))

        # Check for all turbines to have a defined type
        for k, v in data['turbines'].items():
            if 'type' in v:
                if not v['type'] in data['turbine_types']:
                    raise Exception("turbine: {0} type: {1} is not defined in `turbine_types`".format(k, v['type']))
            else:
                raise KeyError("turbine: {0} doesn't have a defined type".format(k))

        # Check that the turbines have a position
        for k, v in data['turbines'].items():
            if 'position' not in v:
                raise Exception("turbine: {0} doesn't have a defined position".format(k))

        # Check the turbine type definition structure
        type_base = ['hub_height',
                     'rotor_diameter',
                     'rated_power',
                     'cut_in_wind_speed',
                     'cut_out_wind_speed',
                     'rated_wind_speed',
                     'air_density',
                     'power_curve',
                     'c_t_curve']
        for k, v in data['turbine_types'].items():
            for k2 in v.keys():
                if k2 not in type_base:
                    raise KeyError('key: {0} not recognized. It should be one of those keys {1}'.format(k2, type_base))
