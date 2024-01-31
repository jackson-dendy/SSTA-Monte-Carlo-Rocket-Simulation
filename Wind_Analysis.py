import json
import matplotlib.pyplot as plt
import numpy as np
from rocketpy import Function


################################################################
# Unfinished prediction model using previosly aquired wind data
################################################################


# Takes collected data and creates a normally distributed plot 
def wind_data(year):
    print("Gathering Wind Data")
    print("**************************\n\n")
    
    wind_x = []
    wind_y = []
    
    for i in year:
        file = open("Outputs\\WindData\\Winddata{:}.json".format(i))
        data = json.load(file)

        windyx = data["atmospheric_model_wind_velocity_x_profile"]
        windyy = data["atmospheric_model_wind_velocity_y_profile"]

        speedx = equal_matrix(windyx)
        speedy = equal_matrix(windyy)

        wind_x.append(speedx)
        wind_y.append(speedy)
    
    wind_x = np.concatenate(wind_x, axis=1)
    wind_y = np.concatenate(wind_y, axis=1)
    
    
    

# Generates the new function (unfinished)        
def equal_matrix(windy):
       
    func = Function(
        source =windy,
        interpolation="spline",
        extrapolation="constant"
        )
    
    
    altitude = np.linspace(0,32000, 120)

    speed = func.get_value(altitude)
    speed = np.array(speed, ndmin= 2).T    

    return speed

wind_data((2021, 2022, 2019))

