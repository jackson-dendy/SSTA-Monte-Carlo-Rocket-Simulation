import rocketpy
from Environment import env
from Rocket import Big_Liquid
from Tools import cf

test_flight = rocketpy.Flight(
    rocket=Big_Liquid,
    environment=env,
    rail_length=6.096,
    inclination=88,
    heading=0,
    max_time_step=0.01,
    terminate_on_apogee=True
)

apogee = test_flight.apogee

apogee_m = apogee

apogee = apogee * cf("m", "ft")


print("The apogee is {:.2f} ft and {:.2f} m".format(apogee, apogee_m))


