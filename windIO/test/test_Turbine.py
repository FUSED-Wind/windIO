import os
from windIO.Plant import WTLayout
import numpy as np
import pytest
import yaml
from jsonschema import validate, ValidationError
from windIO.Turbine import WindTurbine

# The test directory
current_dir = os.path.dirname(__file__)

class TestWindTurbine:
    def setup_method(self, method):
        schema_file = current_dir + '/../variables.yml'
        self.wt = WindTurbine()
        self.wt.load_schema(schema_file)

    def validate(self):
        self.wt.validate()

    def validatation_error(self, yml, message):
        with pytest.raises(ValidationError) as valerror:
            self.validate()
        assert message in str(valerror.value)

    def validation_error_min(self, yml):
        self.validatation_error(yml, "is less than the minimum of")

    def validation_error_max(self, yml):
        self.validatation_error(yml, "is greater than the maximum of")

    def validation_error_type(self, yml, type_var=None):
        if type_var:
            str_type_var = "'%s'"%(type_var)
        else:
            str_type_var = ''
        self.validatation_error(yml, "is not of type %s"%(str_type_var))

    def validation_number_bracket(self, base, valid, lt_min=None, gt_max=None):
        self.validate("{}: {}".format(base, valid))
        if lt_min:
            self.validation_error_min("%s: %f"%(base, lt_min))
        if gt_max:
            self.validation_error_max("%s: %f"%(base, gt_max))

    def test_simple_wind_turbine(self):
        self.wt.load_data({
            'hub': {
                'height': 70.0},
            'rotor': {
                'diameter': 80.0
            }
        })

    def test_negative_height(self):
        # test is a simple error is caught
        with pytest.raises(ValidationError) as valerror:
            self.wt.load_data({
                'hub': {
                    'height': -10.0
                }
            })
        assert 'is less than the minimum' in str(valerror.value)
