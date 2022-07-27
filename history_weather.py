from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily
from statistics import mean
from geopy.geocoders import Nominatim
import PySimpleGUI as sg


def Average(l):     # Calculate average
    avg = mean(l) 
    return avg


##################################################################################
sg.theme('SandyBeach')           #    create theme for the simple GUI   

while True: 

                                                                                                  
    layout = [                                       #    create simple GUI   
        [sg.Text('Enter your location:')],
        [sg.Text('Location:', size=(15, 1)), sg.InputText()],
        [sg.Text('Enter your start date:', size=(15, 1 )), sg.InputText()],
        [sg.Text('Enter your end date:', size=(15, 1 )), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Climate History', layout)
    event, values = window.read()
    window.close()
###################################################################################


    if event == 'Cancel' or event == None:          ######### if user clicks cancel or closes window stop program
        break

#    print(values[0])                               ######### if you want to see the values of the inputs



    geolocater = Nominatim(user_agent="history_weather")
    location = geolocater.geocode(values[0])
#    print((location.latitude, location.longitude)) ######### if you want to see the coordinates of the location 



    location = Point(location.latitude, location.longitude)
    average_lst = []
    average_lst2 = []
    average_lst3 = []

# Set time period
    first_year = int(values[1])
    last_year = int(values[2])


    year_lst = []
    for i in range(first_year, last_year):
        start = datetime(i,1,1)
        end = datetime(i,12,31)
        year_lst.append(i)
        data = Daily(location, start, end)
        data = data.fetch()
    
        avg_lst = []
        for v in data['tavg']:
            avg_lst.append(v)
        average = Average(avg_lst)  # Calculate the average of the average temp. over on year
        average_lst.append(average)

        max_lst = []                                                               
        for v2 in data['tmax']:
            max_lst.append(v2)
        max_temp = Average(max_lst)  # Calculate the average max. temp over one year 
        average_lst2.append(max_temp)

        min_lst = []                                                               
        for v3 in data['tmin']:
            min_lst.append(v3)
        min_temp = Average(min_lst)  # Calculate the average min. temp over one year 
        average_lst3.append(min_temp)


    avgpoint1 = [average_lst[0], average_lst[-1]]
    maxpoint = [average_lst2[0], average_lst2[-1]]
    minpoint = [average_lst3[0], average_lst3[-1]]
    yearsafe =[first_year, last_year]



    fig, ax = plt.subplots()                    ####### plot stuff ######
    ax.plot(year_lst, average_lst2)
    ax.plot(yearsafe, maxpoint)
    ax.plot(year_lst, average_lst)
    ax.plot(yearsafe, avgpoint1)
    ax.plot(year_lst, average_lst3)
    ax.plot(yearsafe, minpoint)
    plt.show(block=True)
