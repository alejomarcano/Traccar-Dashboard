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
from datos import create_df
from datetime import datetime
import re

import flask

import requests
import io

#import locale
#locale.setlocale(locale.LC_ALL, 'esp_esp')

USERNAME_PASSWORD_PAIRS = [
    ['vikua', 'kunigo'],
    ['Juan Andres', '12356']
]

ready = [{'type': 'Polygon',
  'coordinates': (((-78.47814652712178, -0.17952581098751352),
    (-78.47797293860246, -0.17951192392115445),
    (-78.47797293860246, -0.1799077038513417),
    (-78.47657728701314, -0.18035208810573522),
    (-78.47669532699439, -0.181206139581505),
    (-78.4769175200872, -0.1811575349861272),
    (-78.47688974634791, -0.1809700607981597),
    (-78.47829234137205, -0.18079647314390002),
    (-78.47814652712178, -0.17952581098751352)),)},
 {'type': 'Polygon',
  'coordinates': (((-66.85435711164946, 10.485466106518729),
    (-66.85453150643635, 10.483137544749098),
    (-66.85228273155288, 10.483038264594498),
    (-66.85146582965643, 10.48513216656545),
    (-66.85435711164946, 10.485466106518729)),)},
 {'type': 'Polygon',
  'coordinates': (((-78.49208480885643, -0.18486465450376954),
    (-78.49236546381688, -0.1858371515104409),
    (-78.49134727364681, -0.18614391264600272),
    (-78.49097524228796, -0.1847406446958786),
    (-78.4919607984035, -0.1845056790300248),
    (-78.49208480885643, -0.18486465450376954)),)},
 {'type': 'Polygon',
  'coordinates': (((-66.79965329548395, 10.487324156298932),
    (-66.79977233781416, 10.48840060603183),
    (-66.80012393549933, 10.489426725657143),
    (-66.80069165017017, 10.490354534234218),
    (-66.80144893726603, 10.491140647402812),
    (-66.80236038701703, 10.491748306183974),
    (-66.8033833801408, 10.49214909601106),
    (-66.8044700808399, 10.49232427556995),
    (-66.80556967387912, 10.492265653275052),
    (-66.80663074107785, 10.491975970369783),
    (-66.80760366601703, 10.491468772725037),
    (-66.80844295443528, 10.49076777733458),
    (-66.80910936174371, 10.489905763150677),
    (-66.80957172813235, 10.488923038157226),
    (-66.80980843544681, 10.487865554399018),
    (-66.8098084177363, 10.486782759145825),
    (-66.80957167827458, 10.485725282699843),
    (-66.80910928895487, 10.484742570979186),
    (-66.8084428721703, 10.483880573575181),
    (-66.80760358948254, 10.483179595369974),
    (-66.80663068442118, 10.482672412139149),
    (-66.80556964757321, 10.482382738212076),
    (-66.80447008974738, 10.482324117800033),
    (-66.80338342261511, 10.482499291798396),
    (-66.80236045520685, 10.482900069649432),
    (-66.80144901856652, 10.483507712252777),
    (-66.800691729553, 10.484293808032252),
    (-66.80012399829066, 10.485221601223262),
    (-66.79977237240706, 10.486247710309675),
    (-66.79965329548395, 10.487324156298932)),)}]


vector_poligonos = []           
for i in range(0, len(ready)):
    vector_poligonos.append(dict(source = dict(type = 'FeatureCollection',features = [dict(geometry = ready[i])],),type = 'fill',bellow = 'traces',color = 'orange', opacity = 0.5))

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
                                    min_date_allowed=datetime(2020, 5, 1),
                                    max_date_allowed=datetime(2020, 5, 30),
                                    initial_visible_month=datetime(2020, 5, 5),
                                    date=str(datetime(2020, 5, 25).date()),
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
                        html.P(
                            """Selecciona la distancia de km recorrido en el día """
                        ), 


                        html.Div([
                            dcc.Slider(
                                id='elslider',
                                min=0,
                                max= map_data['acum_distance'].max(),
                                step=0.1,
                                value=map_data['acum_distance'].max(),
                            ),
                            html.Div(id='slider-output-container')
                        ]),

                        
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
                     dcc.Tab(label='Eventos', value='tab-5', children=[
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
                     dcc.Tab(label='Viajes', value='tab-6', children=[
                                        dt.DataTable(
                                        rows=df_trips.to_dict('records'),
                                        columns=df_trips.columns,
                                        row_selectable=True,
                                        #filterable=True,
                                        sortable=True,
                                        min_height=250,
                                        selected_row_indices=[],
                                        id='datatable_trips'),
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
     Input('elslider', 'value') 
    ])
def update_selected_row_indices(date, dropdown, borough, elslider):
    map_aux = map_data.copy()
        #map_aux = map_aux[map_aux['datestr'] == date]
    if not map_aux[map_aux['datestr'] == date].empty:
        map_aux = map_aux[map_aux['datestr'] == date]
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
    print('Este es slider', elslider)
    map_aux = map_aux[map_aux["acum_distance"] <= elslider]
    #if selected_row_indices:
    #    map_aux = map_aux.iloc[selected_row_indices]
    
    rows = map_aux.to_dict('records')
    return rows



@app.callback(
    Output('datatable_trips', 'rows'),
    [Input('dropdown', 'value'),
    Input('mydate', 'date'),
    ])
def update_selected_row_indices(dropdown, date):
    trips_aux = df_trips.copy()
    trips_aux = trips_aux[trips_aux['deviceId'] == dropdown]
    trips_aux = trips_aux[trips_aux['strdate'] == date]
    rows = trips_aux.to_dict('records')
    return rows

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
    
        go.Scatter(x=dff['deviceTime'], y=dff['acum_distance'],
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
                        line = dict(color='blue', width=2))
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
                        mode='lines+markers',
                        name='lines+markers',
                        line = dict(color='red', width=2))
        ])

    return go.Figure(data=data, layout=layout)


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('elslider', 'value')])
def update_output(value):
    return 'Has seleccionado {:.2f} Km acumulados en el día'.format(value)



@app.callback(
    Output('output-container-date-picker-single', 'children'),
    [Input('mydate', 'date')])
def update_output(date):
    if date is not None:
        date = datetime.strptime(re.split('T| ', date)[0], '%Y-%m-%d')
        date_string = date.strftime('%B %d, %Y')
        texto = "Usuario: urbo@vikua.com \n Día: " + date_string
        return texto


if __name__ == "__main__":
    app.run_server()
