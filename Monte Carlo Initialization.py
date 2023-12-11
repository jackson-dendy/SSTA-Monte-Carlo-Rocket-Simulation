from rocketpy import Rocket, Environment, Function, GenericMotor, Flight, NoseCone
from numpy.random import normal, choice


analysis_parameters = {
    # Largest Radius of Rocket
    "radius_rocket": (0.0785, 0.003),

    # Rocket dry mass without motor (kg)
    "rocket_mass": (25.85, 0.01),

    # Rocket Inertia moment
    "rocket_inertia_11": (151.7, 0.001517),
    "rocket_inertia_33": (0.186, 0.000186),

    # Center of Mass without motor
    "Center_of_mass_without_motor": (2.26, 0.000226),

    # Parachute reference drags
    "drogue_drag": (3.456, 0.005),
    "main_drag": (28.348, 0.005),

    # Motor Position
    "Motor_Position": (2.148, 0.003),

    # Nose Cone parameters
    "Nose_Cone_Length": (0.914, 0.002),
    "base_radius": (0.0785, 0.003),
    "Nose_Cone_Position": [0],

    # Fins Parameters
    "Num_Fins": [4],
    "Root_Chord": (0.559, 0.002),
    "tip_chord": (0.178, 0.002),
    "Span": (0.127, 0.002),
    "Fin_Position": (5.109, 0.002),
    "cant_angle": (0, 0.001),
    "sweep_length": (0.469, 0.002),

    # Motor Parameters
    "dry_mass": (28.35, 0.002),
    "motor_inertia_11": (29.2998, 0.0002),
    "motor_inertia_33": (0.08184, 0.0002),
    "nozzle_radius": (0.45466, 0.0002),
    "Center_of_mass_motor": (1.7067, 0.001),
    "nozzle_position": (3.596, 0.002),
    "Burn_time_start": (0.04, 0.001),
    "Burn_time_end": (12.106, 0.002),
    "propellant_initial_mass": (33.5, 0.002),

    # Flight Parameters
    "rail_length": (6.096, 0.002),
    "inclination": (88, 0.005),
    "heading": (0, 0.002)
}


flight_setting = {}
for parameter_key, parameter_value in analysis_parameters.items():
    if type(parameter_value) is tuple:
        flight_setting[parameter_key] = normal(*parameter_value)
    else:
        flight_setting[parameter_key] = choice(parameter_value)

