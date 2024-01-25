from rocketpy import Environment
import pandas as pd
import json
import os
import shutil
import time

def wind_data(year, month, day, soundingstation):
        os.makedirs("WindData")
        Wind_X = dict.fromkeys(range(len(year)))
        Wind_Y = dict.fromkeys(range(len(year)))
        print("Gathering Wind Data")
        if type(year) == tuple:
            for i in range(len(year)):    
               while(True):
                    try:
                        env = Environment(date = (year[i], month, day, 12))
                        url ="http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR={0}&MONTH={1}&FROM={3}12&TO={3}12&STNM={2}".format(year[i], month, soundingstation, day)
                        env.set_atmospheric_model(
                        type="wyoming_sounding",
                        file=url
                        )
                    except ImportError:
                         continue
                    else:
                        env.export_environment(filename="Winddata{:}".format(i+1))
                        shutil.move("Winddata{:}.json".format(i+1), "WindData")
                        break

            for i in range(len(os.listdir("WindData"))):
                 file = open("WindData\Winddata{:}.json".format(i+1))
                 data = json.load(file)
                 windy_x = data["atmospheric_model_wind_velocity_x_profile"]
                 windy_y = data["atmospheric_model_wind_velocity_y_profile"]
                 Wind_X[year[i]] = Wind_X.pop(i)
                 Wind_X[year[i]] = windy_x
                 Wind_Y[year[i]] = Wind_Y.pop(i)
                 Wind_Y[year[i]] = windy_y

        else:
            raise TypeError
        
       
    
wind_data((2021, 2022), 10, 10, 72388)























