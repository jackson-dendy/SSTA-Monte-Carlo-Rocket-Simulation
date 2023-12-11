
from rocketpy import GenericMotor
from Unit_Converter import cf
from rocketpy.mathutils import Function

P6127 = GenericMotor(
    thrust_source="MotorData(thrust).csv",
    dry_mass=28.35,
    dry_inertia=(29.2998, 29.2998, 0.08184),
    nozzle_radius=cf("in", "m")*1.79,
    center_of_dry_mass_position=1.706762,
    nozzle_position=3.596,
    burn_time=(0.04, 12.106),
    reshape_thrust_curve=False,
    interpolation_method="linear",
    coordinate_system_orientation="combustion_chamber_to_nozzle",
    chamber_radius=0.0785,
    chamber_height=3.52,
    chamber_position=1.196,
    propellant_initial_mass=33.5,
)

P6127.exhaust_velocity.set_discrete_based_on_model(P6127.thrust)

cg = Function(
    source="Motor_Data(cginmm).csv",
    inputs="time (s)",
    outputs="CG (m)",
    interpolation="spline",
    extrapolation="constant",
    title="CG of the Motor"
)

P6127.center_of_mass = cg



