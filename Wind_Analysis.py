import json
import numpy as np
from rocketpy import Function


################################################################
# Unfinished prediction model using previosly aquired wind data
################################################################


# Takes collected data and creates a normally distributed plot 


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

    return cov, mean

def wind_data(year, max_height, sample = 120):
    wind_x = []
    wind_y = []
    
    for i in year:
        file = open("Outputs\\WindData\\Winddata{:}.json".format(i))
        data = json.load(file)

        windyx = data["atmospheric_model_wind_velocity_x_profile"]
        windyy = data["atmospheric_model_wind_velocity_y_profile"]

        altitude = np.linspace(0,max_height, sample)

        speedx = equal_matrix(windyx,altitude)
        speedy = equal_matrix(windyy,altitude)

        wind_x.append(speedx)
        wind_y.append(speedy)
    
    wind_x = np.concatenate(wind_x, axis=1)
    wind_y = np.concatenate(wind_y, axis=1)
    
    cov_x, mean_x = function_gen(wind_x)
    cov_y, mean_y = function_gen(wind_y)

    return cov_x, cov_y, mean_x, mean_y, altitude


def iterator(cov_x, cov_y, mean_x, mean_y, altitude, date):
    functionx = np.random.multivariate_normal(mean_x, cov_x)
    functionx = np.vstack((altitude, functionx)) 
    functiony = np.random.multivariate_normal(mean_y, cov_y)
    functiony = np.vstack((altitude, functiony)) 

    export(functionx, functiony, date)
    

def export(exportx, exporty, date):
    def list_maker(matrix):
        matrix = matrix.tolist()
        return matrix
    
    wind_x = list_maker(exportx)
    wind_y = list_maker(exporty)

    
    with open("Outputs\\WindData\\Final_Wind.json", "r") as r:
        final = json.load(r)
        final["date"]= date
        final["atmospheric_model_wind_velocity_x_profile"] = wind_x
        final["atmospheric_model_wind_velocity_y_profile"] = wind_y
        r.close()
    with open("Outputs\\WindData\\Final_Wind.json", "w") as w:
        w.truncate()
        json.dump(final, w)
        
    

cov_x, cov_y, mean_x, mean_y, altitude = wind_data((2021, 2022, 2017, 2016), 35000)


iterator(cov_x, cov_y, mean_x, mean_y, altitude, [2024, 6, 6, 12])
    