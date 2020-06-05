# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import dash_auth
import pandas as pd
import datetime
from datetime import time
from dash.dependencies import Input, Output, State, Event
from plotly import graph_objs as go
from plotly.graph_objs import *
from pandas.io.json import json_normalize
from datos import create_df, calcular_ayer_picker, calcular_desde_picker
from datetime import datetime
import re

import flask

import requests
import io

#import locale
#locale.setlocale(locale.LC_ALL, 'esp_esp')

USERNAME_PASSWORD_PAIRS = [
    ['vikua', 'kunigo'],
    ['Juan Andres', '12356'],
    ['barranquila', 'barranquilla.2020']
]

ready = []

# ready = [{'type': 'Polygon',
#   'coordinates': (((-74.78515943350743, 10.957642599149807),
#     (-74.77453580192436, 10.949660396095908),
#     (-74.77941399858116, 10.938378513120412),
#     (-74.78147368326816, 10.934440400352557),
#     (-74.78483421708874, 10.947212478190906),
#     (-74.78624347720896, 10.954343316273722),
#     (-74.79892678520844, 10.958387594597298),
#     (-74.80066125347673, 10.960728994909601),
#     (-74.79556625138785, 10.962538246280204),
#     (-74.78515943350743, 10.957642599149807)),)},
#  {'type': 'Polygon',
#   'coordinates': (((-74.80896298725673, 10.986620313619142),
#     (-74.7981563042545, 10.981057205891176),
#     (-74.80514110812751, 10.971353858493714),
#     (-74.81291665324116, 10.971483236580994),
#     (-74.81726568984591, 10.975882126941713),
#     (-74.81423454190262, 10.980539700102767),
#     (-74.80606362616868, 10.976399635955616),
#     (-74.80369142255614, 10.979763444654978),
#     (-74.81067623648384, 10.98351533366153),
#     (-74.80896298725673, 10.986620313619142)),)},
#  {'type': 'Polygon',
#   'coordinates': (((-74.77950564484186, 10.973733361659946),
#     (-74.77967889360004, 10.975297579095963),
#     (-74.78019062088649, 10.976788663173153),
#     (-74.78101690321765, 10.978136890848484),
#     (-74.78211910709062, 10.979279218144471),
#     (-74.78344569497267, 10.980162228449881),
#     (-74.78493463508391, 10.98074463071232),
#     (-74.78651630230489, 10.980999190619164),
#     (-74.78811673449727, 10.9809140043823),
#     (-74.78966109184147, 10.980493055503239),
#     (-74.79107715726003, 10.97975602845578),
#     (-74.79229871406692, 10.978737388008058),
#     (-74.79326864274826, 10.977484767280885),
#     (-74.79394159196893, 10.97605673999037),
#     (-74.79428609888154, 10.974520081132168),
#     (-74.79428605964475, 10.97294664428234),
#     (-74.79394148151147, 10.971410001597981),
#     (-74.79326848148808, 10.969982003665432),
#     (-74.7922985318128, 10.968729420053554),
#     (-74.79107698770154, 10.967710817617725),
#     (-74.78966096632135, 10.966973822452285),
#     (-74.7881166762178, 10.966552893432013),
#     (-74.78651632203895, 10.966467711359819),
#     (-74.78493472918373, 10.966722258967383),
#     (-74.78344584604395, 10.967304634740104),
#     (-74.78211928720795, 10.968187609261957),
#     (-74.78101707908651, 10.969329898095113),
#     (-74.78019075999767, 10.970678091738156),
#     (-74.77967897023895, 10.972169152504444),
#     (-74.77950564484186, 10.973733361659946)),)},
#  {'type': 'Polygon',
#   'coordinates': (((-74.77950564484186, 10.973733361659946),
#     (-74.77967889360004, 10.975297579095963),
#     (-74.78019062088649, 10.976788663173153),
#     (-74.78101690321765, 10.978136890848484),
#     (-74.78211910709062, 10.979279218144471),
#     (-74.78344569497267, 10.980162228449881),
#     (-74.78493463508391, 10.98074463071232),
#     (-74.78651630230489, 10.980999190619164),
#     (-74.78811673449727, 10.9809140043823),
#     (-74.78966109184147, 10.980493055503239),
#     (-74.79107715726003, 10.97975602845578),
#     (-74.79229871406692, 10.978737388008058),
#     (-74.79326864274826, 10.977484767280885),
#     (-74.79394159196893, 10.97605673999037),
#     (-74.79428609888154, 10.974520081132168),
#     (-74.79428605964475, 10.97294664428234),
#     (-74.79394148151147, 10.971410001597981),
#     (-74.79326848148808, 10.969982003665432),
#     (-74.7922985318128, 10.968729420053554),
#     (-74.79107698770154, 10.967710817617725),
#     (-74.78966096632135, 10.966973822452285),
#     (-74.7881166762178, 10.966552893432013),
#     (-74.78651632203895, 10.966467711359819),
#     (-74.78493472918373, 10.966722258967383),
#     (-74.78344584604395, 10.967304634740104),
#     (-74.78211928720795, 10.968187609261957),
#     (-74.78101707908651, 10.969329898095113),
#     (-74.78019075999767, 10.970678091738156),
#     (-74.77967897023895, 10.972169152504444),
#     (-74.77950564484186, 10.973733361659946)),)},
#  {'type': 'Polygon',
#   'coordinates': (((-74.79364984292619, 10.99813418814024),
#     (-74.79385682448891, 11.000002898264741),
#     (-74.79446820815923, 11.001784240609934),
#     (-74.79545541249064, 11.003394919286437),
#     (-74.79677228054103, 11.004759617388105),
#     (-74.79835723744705, 11.005814519348217),
#     (-74.80013616951727, 11.00651029558724),
#     (-74.80202589023598, 11.006814409763296),
#     (-74.80393803101319, 11.006712640619742),
#     (-74.80578317456111, 11.006209747180302),
#     (-74.8074750373734, 11.005329246146223),
#     (-74.80893450547494, 11.004112311918258),
#     (-74.81009333450768, 11.002615850744535),
#     (-74.81089734099187, 11.000909839152888),
#     (-74.81130893550029, 10.999074051248266),
#     (-74.81130887936872, 10.997194328028492),
#     (-74.81089718297304, 10.99535856326002),
#     (-74.81009310381123, 10.993652593663976),
#     (-74.8089342447449, 10.992156185582457),
#     (-74.80747479480553, 10.99093930572925),
#     (-74.80578299499386, 10.990058850301349),
#     (-74.80393794763943, 10.98955598526925),
#     (-74.80202591846725, 10.989454222083122),
#     (-74.80013630413507, 10.98975831866546),
#     (-74.79835745356739, 10.990454057011815),
#     (-74.79677253821423, 10.991508907784732),
#     (-74.79545566408603, 10.992873550866587),
#     (-74.79446840716962, 10.994484180861027),
#     (-74.7938569341274, 10.996265489860743),
#     (-74.79364984292619, 10.99813418814024)),)}]


vector_poligonos = []           
for i in range(0, len(ready)):
    vector_poligonos.append(dict(source = dict(type = 'FeatureCollection',features = [dict(geometry = ready[i])],),type = 'fill',bellow = 'traces',color = 'blue', opacity = 0.5))

#print(vector_poligonos)
# Plotly mapbox public token

mapbox_access_token = 'pk.eyJ1IjoiYWxlam9tdmciLCJhIjoiY2thZnh6ZDFjMDFoYTJ6cW4wY2djZDVvcSJ9.HuWjTGhIzUBCEf0yx25iEw'
server = flask.Flask(__name__)

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], server=server
)


auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server
# app.config.suppress_callback_exceptions = True
# app.server.config.suppress_callback_exceptions = True
# app.config['suppress_callback_exceptions'] = True




map_data, df_events, df_trips, frame = create_df()
#map_data = df_distance

print('Este es el frame', frame)

#  Layouts
layout_table = dict(
    autosize=False,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    # margin=dict(
    #     l=35,
    #     r=35,
    #     b=35,
    #     t=45
    # ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=8), orientation='h'),
)
layout_table['font-size'] = '8'
layout_table['margin-top'] = '8'



def gen_map(map_data):
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(map_data['latitude']),
                "lon": list(map_data['longitude']),
                "text": "1",
                "hoverinfo": "text",
                "hovertext": [["Hora (hr): {} <br>Velocidad (Km/h): {} <br>Distancia (m): {}".format(i,j,k)]
                                for i,j,k in zip(map_data['hora'], map_data['speed_Km'],map_data['distancia'])],
                "mode": "lines+markers",
                "line_color": "#ffe476", 
                #"name": list(map_data['partday']),
                "marker": go.scattermapbox.Marker(
                    size=17,
                    color=map_data['hour'],
                    colorscale= 'YlOrRd',
                    #colorscale= 'Inferno',
                    #reversescale=True,
                    showscale=True,
                    #cmax=23,
                    #cmin=0,
                    opacity=0.7,
                    ),
                "line": go.scattermapbox.Line(
                    color="yellowgreen"
                ),  

        }],
        "layout": dict(
            autosize=True,
            height=400,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            bearing=0,
            font=dict(color="#191A1A"),
            titlefont=dict(color="#191A1A", size='14'),
            # margin=dict(
            #     l=35,
            #     r=35,
            #     b=35,
            #     t=10
            # ),
            hovermode="closest",
            plot_bgcolor='#fffcfc',
            paper_bgcolor='#fffcfc',
            #legend=dict(font=dict(size=10), orientation='h'),
            #title='Posiciones del dispositivo',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style="streets",
                center=dict(
                    lon=-74.7889,
                    lat=10.9878
                ),
                zoom=10,
                layers =vector_poligonos,),
            updatemenus=[
                dict(
                    type = "buttons",
                    buttons=list([
                        dict(
                            args=[
                            {
                                "mapbox.style": "streets",
                                "mapbox.layers": vector_poligonos,
                            }
                            ],
                            label="Mapa Claro",
                            method="relayout"
                        ),
                        dict(
                            args=[
                            {
                                "mapbox.style": "dark",
                                "colorscale": "Inferno",
                                "mapbox.layers": vector_poligonos,
                            }
                            ],
                            label="Mapa Oscuro",
                            method="relayout"
                        )
                    ]),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=True,
                    #type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    #bgcolor="#323130",
                    borderwidth=1,
                    #bordercolor="#6d6d6d",
                    #font=dict(color="#FFFFFF"),
                ),
            ]
        ),
        "update_layout": dict(
    updatemenus=[
        dict(
            type = "buttons",
            buttons=list([
                dict(
                    args=[
                    {
                        "mapbox.style": "streets",
                    }
                    ],
                    label="Mapa Claro",
                    method="relayout"
                ),
                dict(
                    args=[
                    {
                        "mapbox.style": "dark",
                        "colorscale": "Inferno",
                    }
                    ],
                    label="Mapa Oscuro",
                    method="relayout"
                )
            ]),
            direction="left",
            pad={"r": 0, "t": 0, "b": 0, "l": 0},
            showactive=True,
            #type="buttons",
            #x=0.45,
            #y=0.02,
            #xanchor="left",
            #yanchor="bottom",
            #bgcolor="#323130",
            borderwidth=1,
            #bordercolor="#6d6d6d",
            #font=dict(color="#FFFFFF"),
        ),
    ]


        )

    }








# Layout of Dash App
app.layout = html.Div(
    children=[

        html.Div(
            className="row",
            children=[
                
                # Column for user controls
                html.Div(
                    className="three columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo",  src="https://res.cloudinary.com/vikua/image/upload/v1590017694/samples/URBO/Logo_Vikua_gof6mb.png",
                    style={
                        'height': '45%',
                        'width': '45%',
                        'position': 'relative',
                        'padding-top': 0,
                        'padding-right': 0
                    },
                        ),
                        html.H2(id='output-container-date-picker-single'),

                        html.P(
                            'Selecciona el día:'
                        ),

                            html.Div([
                                dcc.DatePickerSingle(
                                    id='mydate',
                                    min_date_allowed=calcular_desde_picker(),
                                    max_date_allowed=calcular_ayer_picker(),
                                    initial_visible_month=calcular_ayer_picker(),
                                    date=str(calcular_ayer_picker()),
                                ),
                               
                            ]),            
       

                        html.P(
                            'Selecciona el dispositivo:'
                        ),
                        html.Div([
                            dcc.Dropdown(
                                id='dropdown',
                                #options= [{'label': str(item), 'value': item} for item in set(map_data['deviceId'])],
                                #value='URBO-9',
                            ),
                            html.Div(id='dd-output-container')
                        ]),
            
                        html.P(
                            'Selecciona el intervalo de horas:'
                        ),
                        #html.Button('Submit', id='submit-val', n_clicks=0),
                        
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                        dcc.Checklist(
                                id = 'boroughs',
                                options=[
                                    {'label': 'Mañana (de 5 AM a 11 AM)', 'value': 0},
                                    {'label': 'Tarde (de 12 PM a 5 PM)', 'value': 1},
                                    {'label': 'Noche (de 6 PM a 11 PM)', 'value': 2},
                                    {'label': 'Madrugada (de 12 AM a 4 AM)', 'value': 3}
                                ],
                                values=[0, 1, 2,  3],
                                labelStyle={'display': 'inline-block'}
                        ),
                            ],
                        ),
                        # html.P(
                        #     """Selecciona la distancia de km recorrido en el día """
                        # ), 


                        # html.Div([
                        #     dcc.Slider(
                        #         id='elslider',
                        #         min=0,
                        #         max= map_data['acum_distance'].max(),
                        #         step=0.1,
                        #         value=map_data['acum_distance'].max(),
                        #     ),
                        #     html.Div(id='slider-output-container')
                        # ]),

                        
                        #html.H2("Tabla"),
                        # html.P(
                        #     """Selecciona las filas que quieres ver en el mapa """
                        # ),
                        
                        html.Div(
                            className="row",
                            children=[
                                # html.Div(
                                #     #className="div-for-dropdown",
                                #     children=[
                                #         # Dropdown for locations on map
                                #         dt.DataTable(
                                #         rows=map_data.to_dict('records'),
                                #         columns=map_data.columns[0:2],
                                #         row_selectable=True,
                                #         #filterable=True,
                                #         sortable=True,
                                #         min_height=250,
                                #         selected_row_indices=[],
                                #         id='datatable'),
                                #     ],
                                # ),
                                html.Div(
                                    #className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                    html.P(
                                    
                                    ),
                                    ],
                                ),
                            ],
                        ),
                    
                    
                        
                    ],
                ),

                # Column for app graphs and plots
                html.Div(
                    className="nine columns div-for-charts",
                    children=[
                        dcc.Graph(id='map-graph', animate=True),
                        html.Div(
                            className="text-padding",
                            children=[
                                "   "
                            ],
                        ),
                 html.Div(
                    [
                    dcc.Tabs(id='tabs-example', value='tab-1', children=[
                    dcc.Tab(label='Distancia Recorrida', value='tab-1', children=[
                         dcc.Graph(id='graph222'),
                    ]),
                    dcc.Tab(label='Distancia Acumulada', value='tab-2', children=[
                        dcc.Graph(id='grafico_distancia'),

                    ]),
                    dcc.Tab(label='Velocidad Detectada', value='tab-3', children=[
                         dcc.Graph(id='velocidad_detectada'),

                    ]),
                    dcc.Tab(label='Batería del Dispositivo', value='tab-4', children=[
                        
                        dcc.Graph(id='bateria'),


                    ]),
                    dcc.Tab(label='Conexión', value='tab-5', children=[
                        
                        dcc.Graph(id='activo'),


                    ]),
                     dcc.Tab(label='Puntos donde Reporto', value='tab-6', children=[
                                        dt.DataTable(
                                        rows=map_data.to_dict('records'),
                                        columns=map_data.columns[0:2],
                                        row_selectable=True,
                                        #filterable=True,
                                        sortable=True,
                                        min_height=250,
                                        selected_row_indices=[],
                                        id='datatable'),
                    ]),
                     dcc.Tab(label='Eventos', value='tab-7', children=[
                                        dt.DataTable(
                                        rows=df_events.to_dict('records'),
                                        columns=df_events.columns[0:4],
                                        #row_selectable=True,
                                        filterable=True,
                                        sortable=True,
                                        min_height=250,
                                        selected_row_indices=[],
                                        id='datatable_events'),
                    ]),
                
                    ]
                    ),
                    html.Div(id='tabs-example-content')
                    ],
                    #className="twelve columns"
                    ),
                    ],
                ),
           
           
            ],
                
        ),
        #html.Div(children=[dcc.Graph(id='bar-graph')])

    ]
)

@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'rows'), Input('dropdown', 'value'),
     Input('datatable', 'selected_row_indices')])
def map_selection(rows, dropdown, selected_row_indices):
    aux = pd.DataFrame(rows)
    #lat = aux[aux['deviceId'] == dropdown]['latitude'].mean()
    #lon = aux[aux['deviceId'] == dropdown]['longitude'].mean()
    # filtro_zoom = aux[aux['deviceId'] == dropdown]['distancia'].sum() 
    # if filtro_zoom  < 100:
    #     zoom = 18
    # elif filtro_zoom > 100000:
    #     zoom = 10
    # elif  100  <= filtro_zoom < 500:
    #     zoom = 17
    # elif  500  <= filtro_zoom < 1000:
    #     zoom = 16
    # elif  1000  <= filtro_zoom < 2000:
    #     zoom = 15
    # elif  2000  <= filtro_zoom < 5000:
    #     zoom = 14
    # elif  5000  <= filtro_zoom < 10000:
    #     zoom = 13
    # else:
    #     zoom = 15
    temp_df = aux.loc[selected_row_indices, :]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df)

@app.callback(
    Output('datatable', 'rows'),
    [Input('mydate', 'date'),
    Input('dropdown', 'value'),
     Input('boroughs', 'values'),
     #Input('elslider', 'value') 
    ])
def update_selected_row_indices(date, dropdown, borough):
    map_aux = map_data.copy()
    events_aux = df_events.copy()
        #map_aux = map_aux[map_aux['datestr'] == date]
    if (map_aux['strdate'] == date).any():
        print('Fecha fuera de rango')

    print('Esta es date seleccionadado', date)
    if not map_aux[map_aux['strdate'] == date].empty:
        map_aux = map_aux[map_aux['strdate'] == date]
    else:
        print('Fecha no existente', date)
    
    if not map_aux[map_aux['deviceId'] == dropdown].empty:
        map_aux = map_aux[map_aux['deviceId'] == dropdown]
    else:
        print('Ese device ID no existe', dropdown)

 

    #map_aux[(map_aux['deviceId'] == dropdown) | (map_aux["datestr"] == date)]
    #if date is not None:
        #print('Este es date', date)
        #map_aux = map_aux[map_aux['datestr'] == date]
    #print('Este es type date', type(date))
    #map_aux = map_aux[map_aux['strdate'] == fecha]
    # Type filter
    #map_aux = map_aux[map_aux['partday'].isin(type)]
    # Boroughs filter
    #if ((borough == map_aux['partday']).any()):
    if not map_aux[map_aux['partday'].isin(borough)].empty:
        map_aux = map_aux[map_aux["partday"].isin(borough)]
    else:
        print('Rango fuera de hora', borough)
    #else:
    #map_aux = map_aux[map_aux["hour"].isin(myslider)]
    #print('Este es slider', elslider)
    #map_aux = map_aux[map_aux["acum_distance"] <= elslider]



    #if selected_row_indices:
    #    map_aux = map_aux.iloc[selected_row_indices]
    
    rows = map_aux.to_dict('records')
    return rows

@app.callback(
    Output('datatable_events', 'rows'),
    [Input('mydate', 'date'),
    Input('dropdown', 'value'),
     Input('boroughs', 'values'),
     #Input('elslider', 'value') 
    ])
def update_selected_row_indices_events_aux(date, dropdown, borough):
    events_aux = df_events.copy()
    #print('Lalalala', date)
    #Dataframe events
    if (events_aux['dia'] == date).any():
        print('Fecha fuera de rango')

    print('Esta es date seleccionadado', date)
    if not events_aux[events_aux['dia'] == date].empty:
        events_aux = events_aux[events_aux['dia'] == date]
    else:
        print('Fecha no existente', date)
    
    if not events_aux[events_aux['dispositivo'] == dropdown].empty:
        events_aux = events_aux[events_aux['dispositivo'] == dropdown]
    else:
        print('Ese device ID no existe', dropdown)    


    rows = events_aux.to_dict('records')
    return rows

# @app.callback(
#     Output('datatable_trips', 'rows'),
#     [Input('dropdown', 'value'),
#     Input('mydate', 'date'),
#     ])
# def update_selected_row_indices(dropdown, date):
#     trips_aux = df_trips.copy()
#     trips_aux = trips_aux[trips_aux['deviceId'] == dropdown]
#     trips_aux = trips_aux[trips_aux['strdate'] == date]
#     rows = trips_aux.to_dict('records')
#     return rows

@app.callback(
    Output('datatable', 'selected_row_indices'),
    [Input('graph222', 'selectedData'),
    Input('grafico_distancia', 'selectedData')],
    [State('datatable', 'selected_row_indices')])
def update_selected_row_indices(selection1,selection2, selected_row_indices):
    if selection1 and selection1['points']:
        selected_row_indices = []
        for point in selection1['points']:
            selected_row_indices.append(point['pointNumber'])
    if selection2 and selection2['points']:
        selected_row_indices = []
        for point in selection2['points']:
            selected_row_indices.append(point['pointNumber'])

    return selected_row_indices

@app.callback(
    Output('dropdown', 'options'),
    [Input('mydate', 'date')]
)
def update_date_dropdown(date):
    return [{'label': i, 'value': i} for i in frame[date]]

@app.callback(
    Output('dropdown', 'value'),
    [Input('mydate', 'date')]
)
def update_date_value(date):
    return frame[date][0]


@app.callback(
    Output('graph222', 'figure'),
    [Input('datatable', 'rows'), 
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)

    layout = go.Layout(
        title="Distancia Recorrida en el día",
        #bargap=0.05,
        #bargroupgap=0,
        #barmode='group',
        #showlegend=False,
        height=350,
        dragmode="select",
        #paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            #showgrid=False,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #nticks=50,
            #fixedrange=False
            title= 'Tiempo (horas)',        

        ),
        yaxis=dict(
            showticklabels=True,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #showgrid=False,
            #fixedrange=False,
            #rangemode='nonnegative',
            #zeroline=True
            title= 'Distancia (metros)',        

    
        )
    )

    data = Data([
    
        go.Scatter(x=dff['deviceTime'], y=dff['distancia'],
                        mode='lines+markers',
                        name='lines+markers',
                        line = dict(color='red', width=2))
        ])

    return go.Figure(data=data, layout=layout)



#Grafico Distancia Acumulada
@app.callback(
    Output('grafico_distancia', 'figure'),
    [Input('datatable', 'rows'), 
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)

    layout = go.Layout(
        title="Distancia Acumulada en el día",
        #bargap=0.05,
        #bargroupgap=0,
        #barmode='group',
        #showlegend=False,
        height=350,
        dragmode="select",
        #paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            #showgrid=False,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #nticks=50,
            #fixedrange=False
            title= 'Tiempo (horas)',        

        ),
        yaxis=dict(
            showticklabels=True,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #showgrid=False,
            #fixedrange=False,
            #rangemode='nonnegative',
            #zeroline=True
            title= 'Distancia (Km)',        

    
        )
    )

    data = Data([
    
        go.Scatter(x=dff['deviceTime'], y=dff['distancia'].cumsum()/1000,
                        mode='lines+markers',
                        name='lines+markers',
                        line = dict(color='orange', width=2))
        ])

    return go.Figure(data=data, layout=layout)

#Grafico Velocidad
@app.callback(
    Output('velocidad_detectada', 'figure'),
    [Input('datatable', 'rows'), 
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)

    layout = go.Layout(
        title="Velocidad detectada en el día",
        #bargap=0.05,
        #bargroupgap=0,
        #barmode='group',
        #showlegend=False,
        height=350,
        dragmode="select",
        #paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            #showgrid=False,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #nticks=50,
            #fixedrange=False
            title= 'Tiempo (horas)',        

        ),
        yaxis=dict(
            showticklabels=True,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #showgrid=False,
            #fixedrange=False,
            #rangemode='nonnegative',
            #zeroline=True
            title= 'Velocidad (Km/h)',        

    
        )
    )

    data = Data([
    
        go.Scatter(x=dff['deviceTime'], y=dff['speed_Km'],
                        mode='lines+markers',
                        name='lines+markers',
                        line = dict(color='orange', width=2))
        ])

    return go.Figure(data=data, layout=layout)

#Grafico Bateria
@app.callback(
    Output('bateria', 'figure'),
    [Input('datatable', 'rows'), 
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)

    layout = go.Layout(
        title="Batería del dispositivo",
        #bargap=0.05,
        #bargroupgap=0,
        #barmode='group',
        #showlegend=False,
        height=350,
        dragmode="select",
        #paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            #showgrid=False,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #nticks=50,
            #fixedrange=False
            title= 'Tiempo (horas)',        

        ),
        yaxis=dict(
            showticklabels=True,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #showgrid=False,
            #fixedrange=False,
            #rangemode='nonnegative',
            #zeroline=True
            title= 'Porcentaje batería (%)',        

    
        )
    )

    data = Data([
    
        go.Scatter(x=dff['deviceTime'], y=dff['attributes.batteryLevel'],
                        fill='tozeroy',
                        mode='lines+markers',
                        name='lines+markers',
                        line = dict(color='red', width=2))
        ])

    return go.Figure(data=data, layout=layout)




#Grafico Conexion
@app.callback(
    Output('activo', 'figure'),
    [Input('datatable_events', 'rows'), 
     Input('datatable_events', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    dff = dff[(dff['tipo de evento'] == 'En línea') | (dff['tipo de evento'] == 'Sin Conexión') ]
    layout = go.Layout(
        title="Conexión",
        #bargap=0.05,
        #bargroupgap=0,
        #barmode='group',
        #showlegend=False,
        height=350,
        dragmode="select",
        #paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            #showgrid=False,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #nticks=50,
            #fixedrange=False
            title= 'Tiempo (horas)',        

        ),
        yaxis=dict(
            showticklabels=True,
            showspikes= True,
            spikesnap =  'cursor',
            spikedash = 'dot',
            #showgrid=False,
            #fixedrange=False,
            #rangemode='nonnegative',
            #zeroline=True    

    
        )
    )

    data = Data([
        go.Scatter(x=dff['serverTime'], y=dff['tipo de evento'], name="linear", mode='markers+lines', line = {"shape": 'hv', "color": "red"})
        # go.Scatter(x=dff['serverTime'], y=dff['typenumber'],
        #                 mode='lines+markers',
        #                 name='lines+markers',
        #                 line_shape='vh',
        #                 line = dict(color='red', width=2))
         ])
    return go.Figure(data=data, layout=layout)






# @app.callback(
#     dash.dependencies.Output('slider-output-container', 'children'),
#     [dash.dependencies.Input('elslider', 'value')])
# def update_output(value):
#     return 'Has seleccionado {:.2f} Km acumulados en el día'.format(value)



@app.callback(
    Output('output-container-date-picker-single', 'children'),
    [Input('mydate', 'date')])
def update_output(date):
    if date is not None:
        date = datetime.strptime(re.split('T| ', date)[0], '%Y-%m-%d')
        date_string = date.strftime('%B %d, %Y')
        texto = "Usuario: barranquilla@vikua.com \n Día: " + date_string
        return texto


if __name__ == "__main__":
    app.run_server(debug=True)
