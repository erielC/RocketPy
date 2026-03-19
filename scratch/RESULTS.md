## Test Results

```bash
(rocketpy) user@emac RocketPy % python scratch/test_controller.py
/Users/user/projects/RocketPy/rocketpy/sensors/sensor.py:120: UserWarning: The Sensor class (and all its subclasses) is still under experimental development. Some features may be changed in future versions, although we will try to keep the changes to a minimum.
  warnings.warn(
Current Simulation Time: 3.1323 s
>>> Simulation Completed at Time: 3.1247 s
```

```bash
Apogee State

Apogee Time: 3.125 s
Apogee Altitude: 1639.143 m (ASL) | 239.143 m (AGL)
Apogee Freestream Speed: 0.128 m/s
Apogee X position: 0.188 m
Apogee Y position: -5.721 m
Apogee latitude: 32.9899486°
Apogee longitude: 106.9700020°
```

```bash
Burn out State

Burn out time: 3.900 s
Altitude at burn out: 1639.143 m (ASL) | 239.143 m (AGL)
Rocket speed at burn out: 0.000 m/s
Freestream velocity at burn out: 0.128 m/s
Mach Number at burn out: 0.000
Kinetic energy at burn out: 0.000e+00 J
```

```bash
Controller called 65 times
First reading : [(0.0, 0.0, 0.0, 0.0, 0.0)]
Last reading  : (3.1, np.float64(1639.1176907353256), np.float64(2.054534319404984), np.float64(83133.36969303068), np.float64(83127.17040096948))

Barometer readings: 32 samples
Accel readings   : 32 samples
Gyro readings    : 32 samples
```

### success

- Controller was called 65 times
- Sensors fired and collected data
- observed_variables accumulated correctly
- 8-param controller function signature worked
- environment.pressure(z) inside the controller worked
- Baro/accel/gyro all got 32 samples each
