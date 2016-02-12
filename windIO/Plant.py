# License: Apache 2.0
# Author: Pierre-Elouan Rethore
# Email: pire@dtu.dk
#

import yaml
import numpy as np
from .plot import *

class WTLayout(object):
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'r') as f:
            data = yaml.load(f)
        self.data = data
        self.wt_names = list(wt['name'] for wt in data['layout'])
        self._name_map = {n:(k, i)
            for k in data.keys()
                for i,n in enumerate([ob['name'] for ob in data[k]])}
        # Check that the data is correctly organized
        #self.check_structure(data)

    def __getitem__(self, a):
        if a in self.data:
            return self.data[a]
        elif a in self._name_map:
            return self.data[self._name_map[a][0]][self._name_map[a][1]]

    #def __setitem__(self, a, b):
    #    self.data[a] = b

    def __getattr__(self, a):
        """Give access to a list of the properties of the turbine

        Parameters
        ----------
        key: str
            The parameter to return

        Returns
        -------
        parameters: list
            The parameter list of the turbines
        """
        if a in self.data:
            return self.data[a]
        elif a in self._name_map:
            return self.data[self._name_map[a][0]][self._name_map[a][1]]
        else:
            return self.__getattribute__(a)

    @property
    def wt_list(self):
        return self.data['layout']

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

    def plot_layout(self, fig_size=(1000, 500), data={}, layout={}, **kwargs):
        """Plot the wind turbine layout of a wind farm

        Parameters
        ----------
        fig_size: tuple, optional
            The figure size in pixels
        data: dict, optional
            Additional data inputs
        layout: dict, optional
            Additional layout inputs

        Returns
        -------
        h: Plotly instance
            The instance of the Plot.ly plot
        """
        return plot_layout(self, fig_size, data, layout, **kwargs)

    def plot_location(self, UTM, buffers=(16,8), fig_size=(1000, 500), data={}, layout={}, **kwargs):
        """Plot the wind farm location on a map

        Parameters
        ----------
        UTM: tuple
            The UTM region number and letter e.g.: UTM=(32, 'U')
        buffers: tuple, optional
            The longitude and latitude buffer region to plot around the wind farm location
        fig_size: tuple, optional
            The figure size in pixels
        data: dict, optional
            Additional data inputs
        layout: dict, optional
            Additional layout inputs

        Returns
        -------
        h: Plotly instance
            The instance of the Plot.ly plot

        """
        return plot_location(self.positions, UTM, buffers, fig_size, data, layout, **kwargs)
