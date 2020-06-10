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
    print()
    #request to get all points to all devices
    response = requests.get(url + '/api/reports/route?to={1}&from={0}&deviceId={2}&deviceId={3}&deviceId={4}&deviceId={5}'.format(desde, hasta, id_devices[0], id_devices[1], id_devices[2], id_devices[3] ), auth=(user, password), headers=headers, timeout=5.000)
    #response = requests.get(url + '/api/reports/route?to={1}&from={0}&deviceId={2}'.format(desde, hasta, id_devices[0]), auth=(user, password), headers=headers, timeout=5.000)
    data = json.loads(response.content)
    dataframe = json_normalize(data)
    return dataframe
dataframe = create_df()
print(dataframe)
