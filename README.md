# windIO
A multi-language library to write inputs / output files

# Motivation
Wind Energy software ecosystem is a mess. There are many different softwares and
research models that are in competition with their own defined input and output
files. The compatibility between one tool or another is completely left for at the
discretion of the developers and the users. As the ecosystem is mostly closed source
those file convertors are sitting on the companies or individual hard disc rotting
sometime unused, until they become irrelevant. This condition makes it very difficult
for users to get second opinion on their analysis by using another tool, or to
create system engineering workflows by combining different design and analysis
tools together.
This library is an attempt to offer a standard type of I/O fully documented and
flexible enough to cover most use cases. It is the idea that each model and  code
developers can create a file translator to offer a compatibility to this file format.
This library is also a core element of the FUSED-Wind framework, which offers a
code-agnostic and model-agnostic ontology to formulate analysis and design workflows, connect models of different level of fidelities.

# Concept
The library is using json-schema to enforce a taxonomy of how the files should be
organized. That means that the files used in the library will be automatically
checked to see if they fulfill the requirements of the schema. Both JSON and
YAML file format will be supported.
The library will contain an implementation of the file reader/writer in different
languages (e.g. Python, Matlab, Javascript).
Additionally some standard visualization functions will be available for some of
the scripting languages implementations.

## Plugins
Additional file format plugins will be also
supported as pull-request contribution to the library (e.g. WAsP power curve .wtf
file, WRF NETCDF file, ).
The library will also offer the possibility to upload plugin visualization functions
in different languages.

## Documentation
The library will eventually also build a documentation of the file schema.
Additional explanations tutorials and examples will be presented in the library documentation and source code to help developers to design their tools around this library.

# Running the tests
You can use [py.test](http://pytest.org/latest/):

```bash
  $ py.test
```

Or even better [tox](https://testrun.org/tox/latest/):
```bash
  $ tox
```

# Classes
## WTLayout
Defines a wind turbine layout.

```yaml
turbines:
  t1:
    name: T1
    position: [0.0, 0.0]
    type: Type1
  ...
  t4:
    name: T4
    position: [0.0, 1000.0]
    type: Type1
turbine_types:
  Type1:
     hub_height: 65.0
     rotor_diameter: 92.6
     rated_power: 2300.0
     cut_in_wind_speed: 4.0
     cut_out_wind_speed: 25.0
     rated_wind_speed: 14.0
     air_density: 1.225
     power_curve:
        - [3.0,     0.0]
          ...
        - [25.0, 2300.0]
     c_t_curve:
        - [3.0,  0.00]
          ...
        - [25.0, 0.05]

```
