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

        speedx, altitude = equal_matrix(windyx)
        speedy = equal_matrix(windyy)

        wind_x.append(speedx)
        wind_y.append(speedy)
    
    wind_x = np.concatenate(wind_x, axis=1)
    wind_y = np.concatenate(wind_y, axis=1)

    wind_x = function_gen(wind_x)
    wind_y = function_gen(wind_y)

    plt.figure()
    plt.scatter(wind_x, altitude)
def function_gen(matrix):
    mean = mean(matrix)
    cov = cov(matrix)

    function = np.random.multivariate_normal(mean, cov)

    return function
    
    
    

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

    return speed, altitude

wind_data((2021, 2022, 2019))

