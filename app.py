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
#from datetime import datetime as dt
from pandas.io.json import json_normalize
from datos import create_df
from datetime import datetime
import re

import flask

import requests
import io
help_info = """
     # [GOI official Information Portal](https://www.mygov.in/covid-19)
    # [World Health Organization](https://www.who.int/emergencies/diseases/novel-coronavirus-2019)
    # [Ministry of Health and Family Welfare | GOI](https://www.mohfw.gov.in/)
    # [Government Laboratories Approved by ICMR](https://icmr.nic.in/sites/default/files/upload_documents/Final_Government_Laboratories_Testing_2303.pdf)
    """
#html.Div([dcc.Graph(id='bar-graph')],className= 'twelve columns'),
#info = 
import locale
locale.setlocale(locale.LC_ALL, 'esp_esp')

USERNAME_PASSWORD_PAIRS = [
    ['vikua', 'kunigo'],
    ['Juan Andres', '12356']
]
#print(USERNAME_PASSWORD_PAIRS)



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




map_data, frame = create_df()
# df_distance = pd.read_csv("distances_dash.csv")
# df_distance = df_distance[['time', 'attributes.distance', 'latitude', 'longitude', 'altitude', 'deviceTime', 'fixTime', 'attributes.totalDistance', 'attributes.batteryLevel', 'speed', 'partday']]
# df_distance['acum_distance'] = df_distance['attributes.distance'].cumsum() 
# df_distance['speed_Km'] = df_distance['speed']*1.852
# df_distance.rename(columns={'time':'hora', 'attributes.distance':'distancia'}, inplace=True)
# df_distance['horita'] = pd.to_datetime(df_distance['hora'], format='%H:%M:%S')
# df_distance['hour'] = df_distance['horita'].dt.hour

#map_data = df_distance

print('Este es el frame', frame)

#  Layouts
layout_table = dict(
    autosize=False,
    height=600,
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
            ),
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
                        # html.P(
                        #     """Selecciona el dispositivo a consultar"""
                        # ),                        
                        # html.Div(
                        #     className="div-for-dropdown",
                        #             children=[
                        #                 # Dropdown for locations on map
                        # dcc.Dropdown(
                        #     id='type',
                        #     options= [{'label': str(item), 'value': str(item)} for item in set(map_data['partday'])],
                        #     multi=True,
                        #     value=list(set(map_data['partday']))
                        # )
                        # ],
                        # ),

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

                        # html.Div(
                        #     className="div-for-dropdown",
                        #     children=[
                        # dcc.RangeSlider(
                        #         id='myslider',
                        #         min=0,
                        #         max=23,
                        #         #marks={i : {'label' : "{}".format(i+1), 'style':{ 'font-size':'8px'}} for i in range(0, 23) if i %5 ==0},
                        #         marks={
                        #         0: {'label': '12 AM', 'style': { 'font-size':'10px'}},
                        #         3: {'label': '3 AM', 'style': { 'font-size':'10px'}},
                        #         6: {'label': '6 AM',  'style': { 'font-size':'10px'}},
                        #         9: {'label': '9 PM',  'style': { 'font-size':'10px'}},
                        #         12: {'label': '12 PM', 'style': { 'font-size':'10px'}},
                        #         15: {'label': '3 PM',  'style': { 'font-size':'10px'}},
                        #         18: {'label': '6 PM', 'style': { 'font-size':'10px'}},
                        #         21: {'label': '9 PM',  'style': { 'font-size':'10px'}},
                        #         },
                        #         value=[0, 23],
                        #         allowCross=False,
                        #     ),
                        #         #html.Div(id='sliderhoras'), 
                        #     ],
                        # ),

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
                        html.P(
                            """Selecciona las filas que quieres ver en el mapa """
                        ),
                        
                        
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    #className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dt.DataTable(
                                        rows=map_data.to_dict('records'),
                                        columns=map_data.columns[0:2],
                                        row_selectable=True,
                                        #filterable=True,
                                        sortable=True,
                                        min_height=250,
                                        selected_row_indices=[],
                                        id='datatable'),
                                    ],
                                ),
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
    try:
        if len(selected_row_indices) == 0:
            return gen_map(aux)
        return gen_map(temp_df)
    except KeyError:
        print("El dispositivo no se encuentra en esa fecha")
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
    map_aux = map_aux[map_aux['datestr'] == date]
    
    if ((dropdown == map_aux['deviceId']).any()):
        map_aux = map_aux[map_aux['deviceId'] == dropdown]
    else:
        column_names = ['hora', 'distancia', 'deviceId', 'latitude', 'longitude', 'altitude', 'deviceTime', 'fixTime', 'attributes.totalDistance', 'attributes.batteryLevel', 'date', 'datestr', 'speed', 'partday', 'acum_distance', 'speed_Km', 'hour']
        map_aux = pd.DataFrame(columns = column_names)
        print("El dispositivo no reporto en esa fecha")
    #map_aux[(map_aux['deviceId'] == dropdown) | (map_aux["datestr"] == date)]
    #if date is not None:
        #print('Este es date', date)
        #map_aux = map_aux[map_aux['datestr'] == date]
    #print('Este es type date', type(date))
    #map_aux = map_aux[map_aux['strdate'] == fecha]
    # Type filter
    #map_aux = map_aux[map_aux['partday'].isin(type)]
    # Boroughs filter
    map_aux = map_aux[map_aux["partday"].isin(borough)]
    #map_aux = map_aux[map_aux["hour"].isin(myslider)]
    print('Este es slider', elslider)
    map_aux = map_aux[map_aux["acum_distance"] <= elslider]
    #print('Estos son los indices', selected_row_indices)
    #if selected_row_indices:
    #    map_aux = map_aux.iloc[selected_row_indices]
    
    rows = map_aux.to_dict('records')
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
    app.run_server(debug=True)
