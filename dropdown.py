import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

#fnameDict = {'chriddy': ['opt1_c', 'opt2_c', 'opt3_c'], 'jackp': ['opt1_j', 'opt2_j']}
fnameDict ={'2020-05-05': ['URBO-5'],
 '2020-05-08': ['URBO-5'],
 '2020-05-09': ['URBO-5'],
 '2020-05-11': ['URBO-9', 'URBO-5'],
 '2020-05-12': ['URBO-9', 'URBO-5'],
 '2020-05-15': ['URBO-5'],
 '2020-05-16': ['URBO-6'],
 '2020-05-18': ['URBO-7', 'URBO-9'],
 '2020-05-19': ['URBO-7', 'URBO-9'],
 '2020-05-20': ['URBO-7', 'URBO-9'],
 '2020-05-21': ['URBO-7', 'URBO-9'],
 '2020-05-22': ['URBO-7', 'URBO-9'],
 '2020-05-23': ['URBO-7', 'URBO-9'],
 '2020-05-24': ['URBO-9'],
 '2020-05-25': ['URBO-9', 'URBO-10']}
names = list(fnameDict.keys())
nestedOptions = fnameDict[names[0]]

app.layout = html.Div(
    [
        html.Div([
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label':name, 'value':name} for name in names],
            value = list(fnameDict.keys())[0]
            ),
            ],style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
        dcc.Dropdown(
            id='opt-dropdown',
            ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),
        html.Hr(),
        html.Div(id='display-selected-values')
    ]
)

@app.callback(
    dash.dependencies.Output('opt-dropdown', 'options'),
    [dash.dependencies.Input('name-dropdown', 'value')]
)
def update_date_dropdown(name):
    return [{'label': i, 'value': i} for i in fnameDict[name]]

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('opt-dropdown', 'value')])
def set_display_children(selected_value):
    return 'you have selected {} option'.format(selected_value)



if __name__ == '__main__':
    app.run_server()