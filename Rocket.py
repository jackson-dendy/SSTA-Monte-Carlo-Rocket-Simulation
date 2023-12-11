import rocketpy
from rocketpy import Rocket, NoseCone
from Hybrid_Motor import P6127

# Big Liquid instance methods
Big_Liquid = Rocket(
    radius=0.0785,
    mass=25.85,
    inertia=(151.7, 151.7, 0.186),
    power_off_drag="RASPoweroff.csv",
    power_on_drag="RASPoweron.csv",
    center_of_mass_without_motor=2.26,
    coordinate_system_orientation="nose_to_tail",
)

# Parachute Parameters
Big_Liquid.add_parachute("drogue", 3.456, "apogee")
Big_Liquid.add_parachute("main", 28.348, 5000)

# Imports Hybrid Motor
Big_Liquid.add_motor(P6127, 2.148)

# Nose Cone Parameters
nose = NoseCone(
    length=0.914,
    kind='conical',
    base_radius=0.0785,
    rocket_radius=0.0785,
)
Big_Liquid.add_surfaces(nose, 0)

# Fin Parameters
Big_Liquid.add_trapezoidal_fins(4, 0.559, 0.178, 0.127, 5.109, 0, 0.469)

# Body Tube Buildout Parameters
Big_Liquid.add_tail(0.0785, 0.076, 0.051, 2.286)
Big_Liquid.add_tail(0.076, 0.0785, 0.051, 4.856)
Big_Liquid.add_tail(0.0785, 0.057, 0.076, 5.668)

cp = rocketpy.Function(
    source="CP.csv",
    inputs="Mach",
    outputs="CP (m)",
    interpolation="linear",
    extrapolation="constant",
    title='Center of Pressure (m)',
)

cg = rocketpy.Function(
    source="CG(OR).csv",
    inputs="Time (sec)",
    outputs="CG (m)",
    interpolation="spline",
    extrapolation="constant",
    title="CG of the Rocket (m)",
)

Big_Liquid.cp_position = cp
Big_Liquid.center_of_mass = cg

Big_Liquid.cp_position()





