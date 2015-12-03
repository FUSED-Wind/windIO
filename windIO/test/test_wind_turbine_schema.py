import os
from windIO.Plant import WTLayout
import numpy as np
import pytest
import yaml
from jsonschema import validate, ValidationError

# The test directory
current_dir = os.path.dirname(__file__)

class TestWindTurbineSchema:
    base = ""

    def setup_method(self, method):
        schema_file = current_dir + '/../variables.yml'
        with open(schema_file, 'r') as f:
            self.schema = yaml.load(f.read())

    def validate(self, yml):
        validate(yaml.load(self.base + yml), self.schema)

    def validatation_error(self, yml, message):
        with pytest.raises(ValidationError) as valerror:
            self.validate(yml)
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
        self.validate("%s: %f"%(base, valid))
        if lt_min:
            self.validation_error_min("%s: %f"%(base, lt_min))
        if gt_max:
            self.validation_error_max("%s: %f"%(base, gt_max))

    def test_name(self):
        # Test with a correct name
        self.validate("name: V80")

        # pass a number instead of a string
        self.validation_error_type('name: 80','string')

    def test_position(self):
        self.validate("position: [123, 456]")

        # pass a wrong list item
        self.validatation_error("position: [123, a456]",
            "is not of type 'number'")

        # pass a wrong number of items
        self.validatation_error("position: [123, 45, 6]",
            "Additional items are not allowed")

    def test_rated_power(self):
        self.validation_number_bracket('rated_power', 2000.0, -4.)

    def test_cut_in_wind_speed(self):
        self.validation_number_bracket('cut_in_wind_speed', 4.0, -4., 1000.)

    def test_cut_out_wind_speed(self):
        self.validation_number_bracket('cut_out_wind_speed', 4.0, -4., 1000.)

    def test_rated_wind_speed(self):
        self.validation_number_bracket('rated_wind_speed', 4.0, -4., 1000.)

    def test_air_density(self):
        self.validation_number_bracket('air_density', 1.224, 0.1, 3.0)

    def test_power_curve(self):
        self.validate("""
            power_curve:
                - [4.0, 25.0]
                - [10.0, 1000.0]
                - [15.0, 2000.0]
            """)
        # Test that the items min/max works
        self.validation_error_min("""
            power_curve:
                - [-4.0, 25.0]
                - [10.0, 1000.0]
                - [15.0, 2000.0]
            """)

        self.validation_error_min("""
            power_curve:
                - [4.0, -25.0]
                - [10.0, 1000.0]
                - [15.0, 2000.0]
            """)

        # Type error
        self.validation_error_type("""
            power_curve:
                - [4.0, a25.0]
                - [10.0, 1000.0]
                - [15.0, 2000.0] """,
            'number')

        # Wrong number of columns
        self.validatation_error("""
            power_curve:
                - [4.0, 25.0, 0.8]
                - [10.0, 1000.0, 0.2]
                - [15.0, 2000.0, 0.1]
            """, 'Additional items are not allowed')

    def test_c_t_curve(self):
        self.validate("""
            c_t_curve:
                - [4.0, 0.8]
                - [10.0, 0.4]
                - [15.0, 0.1]
            """)
        # Test that the items min/max works
        self.validation_error_min("""
            c_t_curve:
                - [-4.0, 0.8]
                - [10.0, 0.1]
                - [15.0, 0.05]
            """)

        self.validation_error_min("""
            c_t_curve:
                - [4.0, -0.8]
                - [10.0, 0.1]
                - [15.0, 0.05]
            """)

        self.validation_error_max("""
            c_t_curve:
                - [4.0, 1.8]
                - [10.0, 0.1]
                - [15.0, 0.05]
            """)

        # Type error
        self.validation_error_type("""
            c_t_curve:
                - [4.0, a0.8]
                - [10.0, 0.1]
                - [15.0, 0.05] """,
            'number')

        # Wrong number of columns
        self.validatation_error("""
            c_t_curve:
                - [4.0, 0.8, 25.0]
                - [10.0, 0.2, 100.0]
                - [15.0, 0.1, 2000.0]
            """, 'Additional items are not allowed')

    def test_c_t(self):
        self.validation_number_bracket('c_t', 0.89, -0.1, 1.3)

    def test_c_t_idle(self):
        self.validation_number_bracket('c_t_idle', 0.1, -0.1, 1.3)

    def test_c_p(self):
        self.validation_number_bracket('c_p', 0.49, -0.1, 0.7)

    def test_thrust(self):
        self.validation_number_bracket('thrust', 49.0, -0.1)

    def test_power(self):
        self.validation_number_bracket('power', 49, -0.1, 1.0E6)

    def test_hub(self):
        self.validate("""
            hub:
                height: 80.0
                wind_speed: 13.0
            """)
            
        # Test an error in type
        self.validation_error_type("""
            hub:
                height: 80.0
                wind_speed: a13.0
            """, 'number')

        # Test minimum error
        self.validation_error_min("""
            hub:
                height: 80.0
                wind_speed: -13.0
            """)
