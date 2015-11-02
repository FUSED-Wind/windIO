# windIO
A python library to write inputs / output files

# Classes
## WTLayout
Defines a wind turbine layout.

```yaml
turbines:
  t1:
    name: T1
    position: [0.0, 0.0]
    type: Type1
  t2:
    name: T2
    position: [1000.0, 0.0]
    type: Type1
  t3:
    name: T3
    position: [1000.0, 1000.0]
    type: Type1
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
