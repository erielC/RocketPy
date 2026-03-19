from rocketpy import Environment, SolidMotor, Rocket, Flight
from rocketpy.sensors.accelerometer import Accelerometer
from rocketpy.sensors.barometer import Barometer
from rocketpy.sensors.gyroscope import Gyroscope

# environment
env = Environment(latitude=32.99, longitude=106.97, elevation=1400)

# motor
motor = SolidMotor(
    thrust_source="data/motors/cesaroni/Cesaroni_M1670.eng",
    burn_time=3.9,
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    center_of_dry_mass_position=0.317,
    grains_center_of_mass_position=0.397,
    grain_number=5,
    grain_separation=0.005,
    grain_density=1750,
    grain_outer_radius=0.033,
    grain_initial_inner_radius=0.015,
    grain_initial_height=0.12,
    nozzle_radius=0.033,
    throat_radius=0.011,
    interpolation_method="linear",
    nozzle_position=0.0,
    coordinate_system_orientation="combustion_chamber_to_nozzle",
)

# rocket
rocket = Rocket(
    radius=0.0635,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag=0.43,
    power_on_drag=0.43,
    center_of_mass_without_motor=0.0,
    coordinate_system_orientation="nose_to_tail",
)
rocket.set_rail_buttons(0.2, -0.5)
rocket.add_motor(motor, position=-1.373)
rocket.add_nose(length=0.55829, kind="vonKarman", position=1.278)
rocket.add_trapezoidal_fins(
    n=4,
    span=0.120,
    root_chord=0.180,
    tip_chord=0.080,
    position=-1.04956,
)

# sensors
accelerometer = Accelerometer(
    sampling_rate=10,
    orientation=(0, 0, 0),  # aligned with rocket axes
    noise_density=0.005,  # type: ignore
    name="Accelerometer",
)

barometer = Barometer(
    sampling_rate=10,
    noise_density=1.0,  # type: ignore
    name="Barometer",
)

gyroscope = Gyroscope(
    sampling_rate=10,
    orientation=(0, 0, 0),
    noise_density=0.1,  # type: ignore
    name="Gyroscope",
)

rocket.add_sensor(accelerometer, position=0.5)
rocket.add_sensor(barometer, position=0.5)
rocket.add_sensor(gyroscope, position=0.5)

# controller
# 8-param to access sensors and env


def observer_controller(
    time,
    sampling_rate,
    state,
    state_history,
    observed_variables,
    interactive_objects,
    sensors,  # accel, baro, gyro (in order)
    environment,
):
    # state vector [x, y, z, vx, vy, vz, e0, e1, e2, e3, wx, wy, wz]
    z = state[2]
    vz = state[5]

    # sensor measurement updated with each sim step
    accel = sensors[0].measurement
    baro = sensors[1].measurement
    gyro = sensors[2].measurement

    # environment
    atm_pressure = environment.pressure(z)

    return (time, z, vz, baro, atm_pressure)


# use _Controller via air brakes (only entry point)
drag_curve = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [1.0, 1.0, 0.0],
]

rocket.add_air_brakes(
    drag_coefficient_curve=drag_curve,
    controller_function=observer_controller,
    sampling_rate=10,
    initial_observed_variables=[(0.0, 0.0, 0.0, 0.0, 0.0)],
    name="NullBrakes",
    controller_name="SensorObserver",
)


flight = Flight(
    rocket=rocket,
    environment=env,
    rail_length=5.2,
    inclination=85,
    heading=0,
    time_overshoot=False,
    terminate_on_apogee=True,
    verbose=True,
)

# results
flight.prints.apogee_conditions()
flight.prints.burn_out_conditions()

# pull what the controller recorded
obs = flight.get_controller_observed_variables()
print(f"\nController called {len(obs)} times")
print(f"First reading : {obs[0]}")
print(f"Last reading  : {obs[-1]}")

# raw sensor data is also available post-flight
print(f"\nBarometer readings: {len(barometer.measured_data)} samples")
print(f"Accel readings   : {len(accelerometer.measured_data)} samples")
print(f"Gyro readings    : {len(gyroscope.measured_data)} samples")
