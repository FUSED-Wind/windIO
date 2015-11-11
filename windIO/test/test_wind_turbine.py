import os
from windIO.Plant import WTLayout
import numpy as np
import pytest
import yaml
from jsonschema import validate, ValidationError

# The test directory
current_dir = os.path.dirname(__file__)

class TestWindTurbine:
    def setup_method(self, method):
        schema_file = current_dir + '/../variables.yml'
        with open(schema_file, 'r') as f:
            self.schema = yaml.load(f.read())

    def validate(self, yml):
        validate(yaml.load(yml), self.schema)

    def validatation_error(self, yml, message):
        with pytest.raises(ValidationError) as valerror:
            self.validate(yml)
        assert message in str(valerror.value)

    def test_name(self):
        # Test with a correct name
        self.validate("""
            turbine:
                name: V80 """)

        # pass a number instead of a string
        self.validatation_error("""
            turbine:
                name: 80 """,
            "is not of type 'string'")

    def test_position(self):
        self.validate("""
            turbine:
                position: [123, 456] """)

        # pass a wrong list item
        self.validatation_error("""
            turbine:
                position: [123, a456] """,
            "is not of type 'number'")

        # pass a wrong number of items
        self.validatation_error("""
            turbine:
                position: [123, 45, 6] """,
            "Additional items are not allowed")
