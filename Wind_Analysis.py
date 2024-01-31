import json
import matplotlib.pyplot as plt
import numpy as np
from rocketpy import Function


################################################################
# Unfinished prediction model using previosly aquired wind data
################################################################


# Takes collected data and creates a normally distributed plot 
def wind_data(year,date):
    print("Gathering Wind Data")
    print("**************************\n\n")
    
    wind_x = []
    wind_y = []
    
    for i in year:
        file = open("Outputs\\WindData\\Winddata{:}.json".format(i))
        data = json.load(file)

        windyx = data["atmospheric_model_wind_velocity_x_profile"]
        windyy = data["atmospheric_model_wind_velocity_y_profile"]

        altitude = np.linspace(0,32000, 110)

        speedx = equal_matrix(windyx,altitude)
        speedy = equal_matrix(windyy,altitude)

        wind_x.append(speedx)
        wind_y.append(speedy)
    
    wind_x = np.concatenate(wind_x, axis=1)
    wind_y = np.concatenate(wind_y, axis=1)
    
    wind_x = function_gen(wind_x)
    wind_y = function_gen(wind_y)

    wind_x = np.vstack((altitude, wind_x))
    wind_y = np.vstack((altitude, wind_y)) 

    
    export(wind_x.T, wind_y.T, date)

def equal_matrix(windy,altitude):
       
    func = Function(
        source =windy,
        interpolation="spline",
        extrapolation="constant"
        )
    speed = func.get_value(altitude)
    speed = np.array(speed, ndmin= 2).T    

    return speed

def function_gen(matrix):
    
    mean = np.mean(matrix, axis = 1)
    cov = np.cov(matrix)

    function = np.random.multivariate_normal(mean, cov)
    return function
    

def export(export1, export2, date):
    def list_maker(matrix):
        matrix = matrix.tolist()
        return matrix
    
    wind_x = list_maker(export1)
    wind_y = list_maker(export2)

    
    with open("Outputs\\WindData\\Final_Wind.json", "r") as r:
        final = json.load(r)
        final["date"]= date
        final["atmospheric_model_wind_velocity_x_profile"] = wind_x
        final["atmospheric_model_wind_velocity_y_profile"] = wind_y
        r.close()
    with open("Outputs\\WindData\\Final_Wind.json", "w") as w:
        w.truncate()
        json.dump(final, w)
        
    
wind_data((2021, 2022, 2019,2017, 2016, 2018), [2024, 6, 6,12])

