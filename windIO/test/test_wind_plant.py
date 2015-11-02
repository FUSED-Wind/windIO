import os
from windIO.Plant import WTLayout
import numpy as np

# The test directory
current_dir = os.path.dirname(__file__)

class TestWindTurbineLayout:
    def test_read_yml(self):
        filename = current_dir + '/tplant1.yml'
        wt_layout = WTLayout(filename)

        # wt_name is there and correct
        assert hasattr(wt_layout, 'wt_names')
        assert wt_layout.wt_names == ['t1', 't2', 't3', 't4']

        # Get item works
        assert wt_layout['turbines']['t1']['name'] == 'T1'

        # Set item works
        wt_layout['turbines']['t1']['name'] = 'T0'
        assert wt_layout['turbines']['t1']['name'] == 'T0'

        # Get item is the same as data
        assert wt_layout['turbines']['t1']['name'] == wt_layout.data['turbines']['t1']['name']

        np.testing.assert_array_almost_equal(
            wt_layout.positions,
            np.array([[0.0, 0.0],
                      [1000.0, 0.0],
                      [1000.0, 1000.0],
                      [0.0, 1000.0],
                      ]))
