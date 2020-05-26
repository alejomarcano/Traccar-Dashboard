import pandas as pd
from pandas.io.json import json_normalize
import requests
import datetime
from datetime import time

def calcular_fecha(hora):
    hoy = datetime.datetime.combine(datetime.datetime.now().date(), datetime.time(hora,0,0))
    hoy = hoy.isoformat()
    hoy = hoy + 'Z'
    return hoy

def calcular_exacto():
    exacto = datetime.datetime.now()
    exacto = exacto.isoformat()
    exacto = exacto + 'Z'
    return exacto

def calcular_next(hora):
    hoy = datetime.datetime.combine(datetime.datetime.now().date() + datetime.timedelta(days=1), datetime.time(hora,0,0))
    hoy = hoy.isoformat()
    hoy = hoy + 'Z'
    return hoy

def get_part_of_day(hour):
    return (
        0 if  datetime.time(5, 0) <= hour <= datetime.time(11, 0)
        else
        1 if datetime.time(12, 0) <= hour <= datetime.time(17, 0) 
        else
        2 if datetime.time(18, 0)  <= hour <= datetime.time(23, 0) 
        else
        3
    )

def create_df():
    import json
    import sys
    import requests
    uid = 1
    url = 'http://traccar.vikua.com'
    user = 'urbo@vikua.com'
    password = '$W&qeDuuJ5z^Z2wqV^0!T3nB!'
    headers = {'Accept': 'application/json'}

    # intialise data of lists.
    datenow = datetime.datetime.now().date()
    now = datenow.isoformat()
    hoy_inicio = '2020-05-25T00:00:00Z' #calcular_fecha(0)
    exacto = '2020-05-26T00:00:00Z' #calcular_exacto()
    parameters = {'deviceId' : 36,
    'from' :  hoy_inicio,
    'to' : exacto }
    response = requests.get(url + '/api/reports/route', auth=(user, password), headers=headers, params=parameters)
    data = json.loads(response.content)
    #if data:
    dataframe = json_normalize(data)
    df_distance = dataframe[['latitude', 'longitude', 'altitude', 'deviceTime', 'fixTime', 'attributes.distance', 'attributes.totalDistance', 'attributes.batteryLevel', 'speed']]
    df_distance['acum_distance'] = df_distance['attributes.distance'].cumsum()/1000 
    #dataframe['acum_distance'] = dataframe['attributes.distance'].cumsum()
    date = []
    time = []
    date_time = []
    for key, value in df_distance['deviceTime'].iteritems(): 
        #print(key, value) 
        date_time_str = value
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        #date_time_obj.date()
        #print(key, date_time_obj.date())
        date.append(date_time_obj.date()) 
        time.append(date_time_obj.time())
        date_time.append(date_time_obj)
    df_distance["date"] = date
    df_distance["time"] = time
    df_distance["datetime"] = date_time
    partday = []
    [partday.append(get_part_of_day(df_distance['time'][key])) for key, value in df_distance['time'].iteritems()]
    df_distance["partday"] = partday
    df_distance['acum_distance'] = df_distance['attributes.distance'].cumsum()
    df_distance['acum_distance'] = df_distance['acum_distance']/1000
    df_distance = df_distance[['time', 'attributes.distance', 'latitude', 'longitude', 'altitude', 'deviceTime', 'fixTime', 'attributes.totalDistance', 'attributes.batteryLevel', 'speed', 'partday', 'acum_distance']]
    df_distance.rename(columns={'time':'hora', 'attributes.distance':'distancia'}, inplace=True)
    df_distance['speed_Km'] = df_distance['speed']*1.852
    df_distance['horita'] = pd.to_datetime(df_distance['hora'], format='%H:%M:%S')
    df_distance['hour'] = df_distance['horita'].dt.hour
    # else:
    #     df_distance = pd.read_csv("distances_dash.csv")
    #     df_distance = df_distance[['time', 'attributes.distance', 'latitude', 'longitude', 'altitude', 'deviceTime', 'fixTime', 'attributes.totalDistance', 'attributes.batteryLevel', 'speed', 'partday']]
    #     df_distance['acum_distance'] = df_distance['attributes.distance'].cumsum()
    #     df_distance['acum_distance'] = df_distance['acum_distance']/1000
    #     df_distance['speed_Km'] = df_distance['speed']*1.852
    #     df_distance.rename(columns={'time':'hora', 'attributes.distance':'distancia'}, inplace=True)
    #     df_distance['horita'] = pd.to_datetime(df_distance['hora'], format='%H:%M:%S')
    #     df_distance['hour'] = df_distance['horita'].dt.hour
    return df_distance