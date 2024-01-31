import json
import matplotlib.pyplot as plt
import numpy as np


################################################################
# Unfinished prediction model using previosly aquired wind data
################################################################


# Takes collected data and creates a normally distributed plot 
def wind_data(year):
    print("Gathering Wind Data")
    print("**************************\n\n")
    

    # Opens files and stacks all data points into a single array
    windy_x = np.array([[0, 0]])
    windy_y = np.array([[0, 0]])
    for i in year:
        file = open("Outputs\\WindData\\Winddata{:}.json".format(i))
        data = json.load(file)

        windyx = data["atmospheric_model_wind_velocity_x_profile"]
        windyy = data["atmospheric_model_wind_velocity_y_profile"]

        data_frame_windyx = np.array(windyx)
        data_frame_windyy = np.array(windyy)

        windy_x = np.vstack((windy_x, data_frame_windyx))
        windy_y = np.vstack((windy_y, data_frame_windyy))
    
       
    # Generates the new function (unfinished)        
    def function_generator(windy):
       mean_input = np.mean(windy.T, axis=1)
       cov_input = np.cov(windy.T)

       function = np.random.multivariate_normal(
           mean = mean_input,
           cov = cov_input,
           size=(2,667)
       ) 

       return function


    #func = function_generator(windy_x)
    
    #plt.figure()
    #plt.scatter(func[0,:],func[1,:])
   # plt.show()
    

      
  

wind_data((2021, 2022, 2019, 2018, 2017, 2016))

    
    











    #lr_modelx = np.poly1d(np.polyfit(windy_x[:,0], windy_x[:,1], 4))
    #lr_modely = np.poly1d(np.polyfit(windy_y[:,0], windy_y[:,1], 4))

    #lr_altitude_samples = np.linspace(0, 32000, 1000)

    #windx_samples = lr_modelx(lr_altitude_samples)
    #windy_samples = lr_modely(lr_altitude_samples)


 

   


    #plt.figure()
    #print(len(windy_y[:,0]))
    

    

    
    
    

