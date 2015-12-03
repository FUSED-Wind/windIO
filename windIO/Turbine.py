import yaml
from jsonschema import validate


def loadyml(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

class WindTurbine(object):
    def __init__(self, data=None, filename=None, schema=None):
        """Initialize the wind turbine
        :param data: dict, a dictionary containing the fused wind compatible wind turbine information
        :param filename: string, a filename of where to load the turbine (yml format)
        :param schema: string, a json/yaml schema to validate the data
        """
        self.data = None
        self.schema = None
        self.filename = None
        if schema:
            self.load_schema(schema)
        if filename:
            self.load_file(filename)
        if data:
            self.load_data(data)

    def load_file(self, filename):
        self.filename = filename
        self.data = loadyml(filename)
        self.validate()

    def load_data(self, data):
        """Load a wind turbine data
        :param data: dict
        """
        self.data = data
        self.validate()

    def load_schema(self, filename):
        self.schema = loadyml(filename)
        self.validate()

    def validate(self):
        if (self.schema is not None) and (self.data is not None):
            validate(self.data, self.schema)


