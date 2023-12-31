from rocketpy import Rocket, Environment, Function, GenericMotor, Flight, NoseCone
import numpy
from numpy.random import normal, choice
import xlsxwriter
import os
import sys

# This code is a Monte Carlo Simulation for the SSTA Big Liquid program
# To run this code more sure to install the rocketpy, numpy, and xlsxwriter ibraries
# The data for the simulation can be found in your project folder as
# MonteCarlo_sim_inputs.xlsx and MonteCarlo_sim_outputs.xlsx
# Made by Jackson Dendy

# number of simulations ran
num_sim = 2

# The settings for the simulation the first number is the theoretical value
# the second is the standard deviation of that value

analysis_parameters = {
    # Rocket
    "radius_rocket": (0.0785, 0.0003),
    "rocket_mass": (25.85, 0.001),
    "rocket_inertia_11": (151.7, 0.0001517),
    "rocket_inertia_33": (0.186, 0.000186),
    "Center_of_mass_without_motor": (2.26, 0.0000226),
    "drogue_drag": (3.456, 0.005),
    "main_drag": (28.348, 0.005),
    "power_off_drag": (1, 0.05),
    "power_on_drag": (1, 0.05),

    # Motor Position
    "Motor_Position": (2.148, 0.0003),

    # Nose Cone parameters
    "Nose_Cone_Length": (0.914, 0.0002),
    "base_radius": (0.0785, 0.0003),
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
    "Burn_time": (12.066, 0.001),
    "propellant_initial_mass": (33.5, 0.002),
    "Impulse": (73828.591382, 50),

    # Flight Parameters
    "rail_length": (6.096, 0.002),
    "inclination": (88, 0.0005),
    "heading": (0, 0.0002)
}

# creates n list of sim number and loading bar
lst = [int(d) for d in range(num_sim+1)]
len_bar = 50

bar = ["-"]*len_bar
done = []
percent_bar = 1/len_bar

for z in range(len_bar):
    x = percent_bar * (z+1)
    x = round(x, 2)
    done.append(x)

# Initialize Excel Files and detect previous files
if os.path.exists('MonteCarlo_sim_inputs.xlsx') or os.path.exists("MonteCarlo_sim_outputs.xlsx"):
    sys.stdout.write("The file you are creating already exists you may overwrite"
                     "data if you proceed.\nDo you wish to proceed? ")
    ans = input("")
    ans = ans.lower()
    ans = ans.capitalize()
    if ans == "Yes":
        print("\n\nInitializing Monte Carlo Simulation\n")
    else:
        quit()
else:
    print("\n\nInitializing Monte Carlo Simulation\n")
inputs = xlsxwriter.Workbook('MonteCarlo_sim_inputs.xlsx')
outputs = xlsxwriter.Workbook("MonteCarlo_sim_outputs.xlsx")
inp = inputs.add_worksheet()
out = outputs.add_worksheet()

# Writes the simulation number to out and in file and input parameter names to the input files
col = 0
row = 1
for n in lst:
    out.write(0, col, n)
    inp.write(0, col, n)
    col += 1
for p in analysis_parameters.keys():
    inp.write(row, 0, p)
    row += 1

# The simulations that are ran are dependent on what the above parameters, and they change each iteration
for i in range(num_sim):
    # for each iteration this loop defines the parameters of the simulation
    setting = {}
    for parameter_key, parameter_value in analysis_parameters.items():
        if type(parameter_value) is tuple:
            setting[parameter_key] = normal(*parameter_value)
        else:
            setting[parameter_key] = choice(parameter_value)

    # writes the settings for each simulation iteration
    for g in range(len(setting)):
        inp.write(g+1, i+1, list(setting.values())[g])

    # Motor Object
    P6127 = GenericMotor(
        thrust_source="MotorData(thrust).csv",
        dry_mass=setting["dry_mass"],
        dry_inertia=(setting["motor_inertia_11"], setting["motor_inertia_11"], setting["motor_inertia_33"]),
        nozzle_radius=setting["nozzle_radius"],
        center_of_dry_mass_position=setting["Center_of_mass_motor"],
        nozzle_position=setting["nozzle_position"],
        burn_time=12.066,
        reshape_thrust_curve=(setting["Burn_time"], setting["Impulse"]),
        interpolation_method="linear",
        coordinate_system_orientation="combustion_chamber_to_nozzle",
        chamber_radius=0.0785,
        chamber_height=3.52,
        chamber_position=1.196,
        propellant_initial_mass=setting["propellant_initial_mass"],
    )

    P6127.exhaust_velocity.set_discrete_based_on_model(P6127.thrust)

    cg = Function(
        source="CG(OR).csv",
        inputs="time (s)",
        outputs="CG (m)",
        interpolation="spline",
        extrapolation="constant",
        title="CG of the Motor"
    )

    P6127.center_of_mass = cg

    # Big Liquid object
    RASPoweroff = Function(
        source="RASPoweroff.csv",
        inputs="mach",
        outputs="CD",
        interpolation="spline",
        extrapolation="constant",
        title="Power off drag",
    )

    RASPoweron = Function(
        source="RASPoweron.csv",
        inputs="mach",
        outputs="CD",
        interpolation="spline",
        extrapolation="constant",
        title="Power on drag",
    )

    Big_Liquid = Rocket(
        radius=setting["radius_rocket"],
        mass=setting["rocket_mass"],
        inertia=(setting["rocket_inertia_11"], setting["rocket_inertia_11"], setting["rocket_inertia_33"]),
        power_off_drag=numpy.array(RASPoweroff) * setting["power_off_drag"],
        power_on_drag=numpy.array(RASPoweron) * setting["power_on_drag"],
        center_of_mass_without_motor=setting["Center_of_mass_without_motor"],
        coordinate_system_orientation="nose_to_tail",
    )

    # Parachute Parameters
    Big_Liquid.add_parachute("drogue", setting["drogue_drag"], "apogee")
    Big_Liquid.add_parachute("main", setting["main_drag"], 5000)

    # Imports Hybrid Motor
    Big_Liquid.add_motor(P6127, setting["Motor_Position"])

    # Nose Cone Parameters
    nose = NoseCone(
        length=setting["Nose_Cone_Length"],
        kind='conical',
        base_radius=setting["base_radius"],
        rocket_radius=setting["base_radius"],
    )
    Big_Liquid.add_surfaces(nose, setting["Nose_Cone_Position"])

    # Fin Parameters
    Big_Liquid.add_trapezoidal_fins(4, setting["Root_Chord"], setting["tip_chord"], setting["Span"],
                                    setting["Fin_Position"], setting["cant_angle"], setting["sweep_length"])

    # Body Tube Buildout Parameters
    Big_Liquid.add_tail(0.0785, 0.076, 0.051, 2.286)
    Big_Liquid.add_tail(0.076, 0.0785, 0.051, 4.856)
    Big_Liquid.add_tail(0.0785, 0.057, 0.076, 5.668)

    cp = Function(
        source="CP.csv",
        inputs="Mach",
        outputs="CP (m)",
        interpolation="spline",
        extrapolation="constant",
        title='Center of Pressure (m)',
    )

    cg = Function(
        source="CG_Rocket.csv",
        inputs="Time (sec)",
        outputs="CG (m)",
        interpolation="spline",
        extrapolation="constant",
        title="CG of the Rocket (m)",
    )

    Big_Liquid.cp_position = cp
    Big_Liquid.center_of_mass = cg

    # Environment Parameters
    env = Environment(
        date=(2020, 6, 10, 18),
        latitude=35.3467755,
        longitude=-117.80820,
        elevation=630,
        datum="WGS84",
        max_expected_height=26000
    )

    env.set_atmospheric_model(
        type="Windy",
        file="GFS"
    )

    # Flight parameters
    flight_data = Flight(
        rocket=Big_Liquid,
        environment=env,
        rail_length=setting["rail_length"],
        inclination=setting["inclination"],
        heading=setting["heading"],
        max_time_step=0.01,
        max_time=2000
    )

    # Selected Returned Values for the flight (can add more)
    flight_result = {
        "out_of_rail_time": flight_data.out_of_rail_time,
        "out_of_rail_velocity": flight_data.out_of_rail_velocity,
        "max_velocity": flight_data.speed.max,
        "apogee_time": flight_data.apogee_time,
        "apogee_altitude": flight_data.apogee - env.elevation,
        "apogee_x": flight_data.apogee_x,
        "apogee_y": flight_data.apogee_y,
        "impact_time": flight_data.t_final,
        "impact_x": flight_data.x_impact,
        "impact_y": flight_data.y_impact,
        "impact_velocity": flight_data.impact_velocity,
        "initial_static_margin": flight_data.rocket.static_margin(0),
        "out_of_rail_static_margin": flight_data.rocket.static_margin(
            flight_data.out_of_rail_time
        ),
        "final_static_margin": flight_data.rocket.static_margin(
            flight_data.rocket.motor.burn_out_time
        ),
        "number_of_events": len(flight_data.parachute_events)
    }

    # writes flight result titles to the output file for the first iteration
    row = 1
    if i == 0:
        for o in flight_result.keys():
            out.write(row, 0, o)
            row += 1
    else:
        pass

    # Writes flight results to the output file
    for h in range(len(flight_result)):
        out.write(h+1, i+1, list(flight_result.values())[h])

    # Writes the updated prompts per simulation to command window
    message = "Simulation " + str(i+1) + " success! - "
    percent_done = (i+1) / num_sim
    for z in range(len(done)):
        if done[z] <= percent_done:
            bar[z] = "*"

    # writes to terminal
    sys.stdout.write('\r' + message + "".join(bar))
    # feed, so it erases the previous line.
    sys.stdout.flush()


inputs.close()
outputs.close()
print('\n\nYou will find the results in your project folder')
print("You ran {} simulations".format(num_sim))
