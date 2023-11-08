from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily
from statistics import mean
from geopy.geocoders import Nominatim
import PySimpleGUI as sg


def Average(l):     # Calculate average
    avg = mean(l) 
    return avg

def geolocate(location_str):
    geolocator = Nominatim(user_agent="history_weather")
    location = geolocator.geocode(location_str)
    return Point(location.latitude, location.longitude)

    

##################################################################################
sg.theme('LightBlue3')           #    create theme for the simple GUI   

while True: 

                                                                                                  
    layout = [
    [sg.Text('Climate History', font=('Helvetica', 20), justification='center', size=(30, 1))],
    [sg.Text('Enter your location:', font=('Helvetica', 14))],
    [sg.InputText(size=(30, 1))],
    [sg.Text('Enter your start date:', font=('Helvetica', 14))],
    [sg.InputText(size=(30, 1))],
    [sg.Text('Enter your end date:', font=('Helvetica', 14))],
    [sg.InputText(size=(30, 1))],
    [sg.Submit(button_color=('white', 'green')), sg.Cancel(button_color=('white', 'red'))]
    ]

    window = sg.Window('Climate History', layout)
    event, values = window.read()
    window.close()
    if event == 'Cancel' or event == None:          ######### if user clicks cancel or closes window stop program
        break
###################################################################################


#    print(values)                               ######### if you want to see the values of the inputs

    location = geolocate(values[0])
  
    # Set time period
    first_year = int(values[1])
    last_year = int(values[2])


    average_lst = []
    average_lst2 = []
    average_lst3 = []

    year_lst = []
    for i in range(first_year, last_year):
        start = datetime(i,1,1)
        end = datetime(i,12,31)
        year_lst.append(i)
        data = Daily(location, start, end)
        data = data.fetch()
    
        average_lst.append(Average(data['tavg']))
        average_lst2.append(Average(data['tmax']))
        average_lst3.append(Average(data['tmin']))


    avgpoint1 = [average_lst[0], average_lst[-1]]
    maxpoint = [average_lst2[0], average_lst2[-1]]
    minpoint = [average_lst3[0], average_lst3[-1]]
    yearsafe =[first_year, last_year]



    fig, ax = plt.subplots()                    ####### plot stuff ######
    ax.plot(year_lst, average_lst, label='Average Temp')
    ax.plot(yearsafe, avgpoint1)
    ax.plot(year_lst, average_lst2,  label='Max Temp')
    ax.plot(yearsafe, maxpoint)
    ax.plot(year_lst, average_lst3, label='Min Temp')
    ax.plot(yearsafe, minpoint)
    ax.legend()
    plt.show(block=True)
