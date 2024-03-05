import json
import numpy as np
from rocketpy import Function




################################################################
# Prediction model using previosly aquired environment data
################################################################

# The Below Function generate a covariance and mean matrix in order to use in the iterator function

# Greates equal sized matrix with equivelant y values for every wind data collection

def equal_matrix(windy,altitude):
       
    func = Function(
        source =windy,
        interpolation="spline",
        extrapolation="constant"
        )
    speed = func.get_value(altitude)
    speed = np.array(speed, ndmin= 2).T    

    return speed

# Creates a covariance and mean matrix
def function_gen(matrix):
    
    mean = np.mean(matrix, axis = 1)
    cov = np.cov(matrix)

    return cov, mean

# Exports the covariance and mean matrixes 
def data_collection(year, max_height, sample = 120):
    print("Generating Matrixes \n########################\n")
    wind_x = []
    wind_y = []
    final_temp_data = []
    final_pressure_data = []
    
    for i in year:
        file = open("Outputs\\WindData\\Winddata{:}.json".format(i))
        data = json.load(file)

        windyx = data["atmospheric_model_wind_velocity_x_profile"]
        windyy = data["atmospheric_model_wind_velocity_y_profile"]
        temperature = data["atmospheric_model_temperature_profile"]
        pressure = data["atmospheric_model_temperature_profile"]

        altitude = np.linspace(0,max_height, sample)

        speedx = equal_matrix(windyx,altitude)
        speedy = equal_matrix(windyy,altitude)
        temp = equal_matrix(temperature,altitude)
        pres = equal_matrix(pressure,altitude)

        wind_x.append(speedx)
        wind_y.append(speedy)
        final_pressure_data.append(pres)
        final_temp_data.append(temp)
    
    wind_x = np.concatenate(wind_x, axis=1)
    wind_y = np.concatenate(wind_y, axis=1)
    final_pressure_data = np.concatenate(final_pressure_data, axis=1)
    final_temp_data = np.concatenate(final_temp_data, axis=1)
    
    cov_x, mean_x = function_gen(wind_x)
    cov_y, mean_y = function_gen(wind_y)
    cov_temp, mean_temp = function_gen(final_temp_data)
    cov_pressure, mean_pressure = function_gen(final_pressure_data)
    return cov_x, cov_y, cov_temp, cov_pressure, mean_x, mean_y, mean_temp, mean_pressure, altitude

# a function designed to be iterated in a monte carlo simulation and exports the environment parameters
def iterator(cov, mean, altitude):
    list = []
    function = np.random.multivariate_normal(mean, cov)
    for f in range(np.size(function)):
        item =[]
        item.append(altitude[f])
        item.append(function[f])
        list.append(item)
    function = list
    return function



