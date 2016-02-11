import os
from windIO.Plant import WTLayout
import numpy as np
import pytest

# The test directory
current_dir = os.path.dirname(__file__)

class TestWindTurbineLayout:
    def setup_method(self, method):
        self.filename = current_dir + '/tplant1.yml'
        self.wt_layout = WTLayout(self.filename)

    def test_read_yml(self):
        # wt_name is there and correct
        assert hasattr(self.wt_layout, 'wt_names')
        assert self.wt_layout.wt_names == ['T1', 'T2', 'T3', 'T4']

        # Get item works
        assert self.wt_layout['layout'][0]['name'] == 'T1'

        # Set item works
        self.wt_layout['layout'][0]['name'] = 'T0'
        assert self.wt_layout['layout'][0]['name'] == 'T0'

        # Get item is the same as data
        assert self.wt_layout['layout'][0]['name'] == self.wt_layout.data['layout'][0]['name']

        # Test the positions property
        np.testing.assert_array_almost_equal(
            self.wt_layout.positions,
            np.array([[0.0, 0.0],
                      [1000.0, 0.0],
                      [1000.0, 1000.0],
                      [0.0, 1000.0],
                      ]))


    def test_tree_structure(self):
        assert self.wt_layout.T1.name == 'T1'
        assert self.wt_layout[0].name == 'T1'
        assert self.wt_layout.T1.rotor_diameter == self.wt_layout['turbine_types'][self.wt_layout.T1.turbine_type]['rotor_diameter']


    # def test_check_base_structure(self):
    #     data = self.wt_layout.data
    #     data['wrong_key'] = ''
    #     with pytest.raises(KeyError) as keyinfo:
    #         self.wt_layout.check_structure(data)
    #     assert 'not recognized' in str(keyinfo.value)

    # def test_check_turbine_type_definition(self):
    #     data = self.wt_layout.data
    #     data['turbines']['t1']['type'] = 'Type2'
    #     with pytest.raises(Exception) as keyinfo:
    #         self.wt_layout.check_structure(data)
    #     assert 'turbine: t1 type: Type2 is not defined in `turbine_types`' in str(keyinfo.value)
    #
    # def test_check_turbine_position_definition(self):
    #     data = self.wt_layout.data
    #     data['turbines']['t1'].pop('position', None)
    #     with pytest.raises(Exception) as keyinfo:
    #         self.wt_layout.check_structure(data)
    #     assert "turbine: t1 doesn't have a defined position" in str(keyinfo.value)
    #
    # def test_check_turbine_type_structure(self):
    #     data = self.wt_layout.data
    #     data['turbine_types']['Type1']['rotor_diamter'] =  90.0
    #     with pytest.raises(KeyError) as keyinfo:
    #         self.wt_layout.check_structure(data)
    #     assert 'not recognized' in str(keyinfo.value)
