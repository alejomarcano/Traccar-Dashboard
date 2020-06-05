import pandas as pd
from pandas import json_normalize
import requests
import datetime
from datetime import time
import json
import sys
import requests
import numpy as np

def calcular_hoy(hora):
    hoy = datetime.datetime.combine(datetime.datetime.now().date(), datetime.time(hora,0,0))
    hoy = hoy.isoformat()
    hoy = hoy + 'Z'
    return hoy


def calcular_next(hora):
    hoy = datetime.datetime.combine(datetime.datetime.now().date() - datetime.timedelta(days=1), datetime.time(hora,0,0))
    hoy = hoy.isoformat()
    hoy = hoy + 'Z'
    return hoy

def calcular_ayer(hora):
    hoy = datetime.datetime.combine(datetime.datetime.now().date() - datetime.timedelta(days=5), datetime.time(hora,0,0))
    hoy = hoy.isoformat()
    hoy = hoy + 'Z'
    return hoy

def calcular_desde_picker():
    hoy = datetime.datetime.combine(datetime.datetime.now().date() - datetime.timedelta(days=5), datetime.time(0,0,0))
    hoy = hoy.date()
    return hoy
def calcular_ayer_picker():
    ayer = datetime.datetime.combine(datetime.datetime.now().date() - datetime.timedelta(days=1), datetime.time(0,0,0))
    ayer = ayer.date()
    return ayer

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

    url = 'http://traccar.vikua.com'
    user = 'barranquilla@vikua.com'
    password = 'B@rr@nquill@.2020'
    headers = {'Accept': 'application/json'}
    desde = calcular_ayer(0)
    hasta = calcular_hoy(0)
    
    #request to get all devices
    responsedev = requests.get(url + '/api/devices', auth=(user, password), headers=headers)
    devices = json.loads(responsedev.content)
    df_devices = json_normalize(devices)
    id_devices = df_devices['id'].to_list()
    df_devices =df_devices[['id', 'name']]
    dic_devices = df_devices.set_index('id')['name'].to_dict()

    #request to get all points to all devices
    response = requests.get(url + '/api/reports/route?to={1}&from={0}&deviceId={2}&deviceId={3}&deviceId={4}&deviceId={5}&deviceId={6}&deviceId={7}'.format(desde, hasta, id_devices[0], id_devices[1], id_devices[2], id_devices[3], id_devices[4], id_devices[5] ), auth=(user, password), headers=headers, timeout=5.000)
    #response = requests.get(url + '/api/reports/route?to={1}&from={0}&deviceId={2}'.format(desde, hasta, id_devices[0]), auth=(user, password), headers=headers, timeout=5.000)
    data = json.loads(response.content)
    dataframe = json_normalize(data)

    #Select columns Dataframe
    df_distance = dataframe[['attributes.distance', 'deviceId', 'latitude', 'longitude', 'deviceTime', 'attributes.batteryLevel', 'speed', 'serverTime']]
    
    #dates, times covertiones
    df_distance["date"] = df_distance['deviceTime'].apply(lambda row: datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S.%f%z').date())
    df_distance["time"] = df_distance['deviceTime'].apply(lambda row: datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S.%f%z').time())
    df_distance["strdate"] = df_distance['deviceTime'].apply(lambda row: datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S.%f%z').date().strftime('%Y-%m-%d'))
    df_distance["partday"] = df_distance['time'].apply(lambda row: get_part_of_day(row) )
    df_distance["datestr"] = df_distance["strdate"] 
    #distance acum column
    df_distance['acum_distance'] = df_distance['attributes.distance'].cumsum()
    #distance acum in Km
    df_distance['acum_distance'] = df_distance['acum_distance']/1000
    #convert speed to Km/h
    df_distance['speed_Km'] = df_distance['speed']*1.852
    df_distance['horita'] = pd.to_datetime(df_distance['time'], format='%H:%M:%S')
    df_distance['hour'] = df_distance['horita'].dt.hour
    
    #Replace int id with string name deviceId in df_distance dataframe
    df_distance['deviceIdReal'] = df_distance['deviceId']
    df_distance['deviceId'] = df_distance['deviceId'].replace(dic_devices)

    df_distance = df_distance[['time', 'attributes.distance', 'deviceId', 'latitude', 'longitude', 'deviceTime', 'attributes.batteryLevel', 'date', 'strdate', 'speed', 'partday', 'serverTime', 'acum_distance', 'hour', 'datestr', 'speed_Km']]
    df_distance.rename(columns={'time':'hora', 'attributes.distance':'distancia'}, inplace=True)

    #dict: key with date and value is the devices that report this day
    df_to_dic = df_distance[['deviceId', 'datestr']]
    diction = df_to_dic.drop_duplicates(subset=['deviceId', 'datestr']).groupby('datestr')['deviceId'].unique().to_frame('id').reset_index()
    idd = []
    [idd.append(diction['id'][key].tolist()) for key, value in diction['id'].iteritems()]
    diction["id"] = idd
    #diction["id"] = diction['id'].apply(lambda row: row.tolist())

    seriee= diction.set_index('datestr')
    seriee = seriee.squeeze()
    frame = seriee.to_dict()
    
    #request get all events to all devices
    response = requests.get(url + '/api/reports/events?to={1}&from={0}&deviceId={2}&deviceId={3}&deviceId={4}&deviceId={5}&deviceId={6}&deviceId={7}'.format(desde, hasta, id_devices[0], id_devices[1], id_devices[2], id_devices[3], id_devices[4], id_devices[5] ), auth=(user, password), headers=headers, timeout=5.000)
    #response = requests.get(url + '/api/reports/events?to={1}&from={0}&deviceId={2}'.format(desde, hasta, id_devices[0]), auth=(user, password), headers=headers, timeout=5.000)

    datosevents = json.loads(response.content)
    df_events = json_normalize(datosevents)  
    #Replace int id with string name deviceId in df_distance dataframe
    df_events['deviceId'] = df_events['deviceId'].replace(dic_devices)
    df_events["date"] = df_events['serverTime'].apply(lambda row: datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S.%f%z').date())
    df_events["time"] = df_events['serverTime'].apply(lambda row: datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S.%f%z').time())
    df_events["strdate"] = df_events['serverTime'].apply(lambda row: datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S.%f%z').date().strftime('%Y-%m-%d'))
    df_events['type'] = df_events['type'].replace(['deviceOnline','deviceUnknown', 'deviceStopped', 'deviceMoving'  ],['En línea','Sin Conexión', 'Detenido', 'Moviendose'])
    #df_online = df_events[(df_events['type'] == 'En línea') | (df_events['type'] == 'Sin Conexión') ]
    df_online = df_events[['deviceId', 'type', 'strdate', 'time', 'serverTime']]
    df_online.rename(columns={'deviceId':'dispositivo', 'type':'tipo de evento', 'strdate':'dia', 'time':'hora'}, inplace=True)

    #request get all events to all devices
    # response = requests.get(url + '/api/reports/trips?to={1}&from={0}&deviceId={2}'.format(desde, hasta, id_devices[0]), auth=(user, password), headers=headers, timeout=5.000)
    # datostrips = json.loads(response.content)
    # df_trips = json_normalize(datostrips)
    # df_trips['deviceId'] = df_trips['deviceId'].replace(dic_devices)
    # df_trips[['deviceId', 'startTime', 'endTime', 'distance', 'duration']]
    # df_trips["date"] = df_trips['startTime'].apply(lambda row: datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S.%f%z').date())
    # df_trips["time"] = df_trips['startTime'].apply(lambda row: datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S.%f%z').time())
    # df_trips["strdate"] = df_trips['startTime'].apply(lambda row: datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S.%f%z').date().strftime('%Y-%m-%d'))
    # df_trips = df_trips[['deviceId', 'startTime', 'endTime', 'distance', 'strdate']]
    df_trips = df_events
    #the function return 3 dataframes and 1 dict
    hora_mostrar = datetime.datetime.strptime(sorted(frame.keys())[-1], '%Y-%m-%d').date()
    return df_distance, df_online, df_trips, frame, hora_mostrar