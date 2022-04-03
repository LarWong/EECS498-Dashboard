import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data import import_demo_data
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

test_options1 = ['a', 'b', 'c']
test_options2 = ['d', 'e', 'f']
test_value = [1, 2, 3]


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='four columns div-user-controls',
                    children=[
                        html.H2('DASH - STOCK PRICES'),
                        html.P('Visualising time series with Plotly - Dash.'),
                        html.P('Pick one data type below.'),
                    ]),
                html.Div(
                    className='eight columns div-for-charts bg-grey')
            ]),
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='three columns div-user-controls',
                    children=[
                        html.H2('DATA VISUALIZATION'),
                        html.P('Visualising ECONOMIC and TEXT data.'),
                        html.P('Pick one data type below.'),
                        
                        html.Div(
                            className='div-for-radio',
                            children=[
                                dcc.RadioItems(id='dataradio', options=[' Economic', ' Text'], value=' Economic'),
                            ]),

                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='datadropdown',
                                             searchable=False,
                                             style={'backgroundColor': '#1E1E1E'}),
                            ]),
                    ]),
            html.Div(
                className='nine columns div-for-charts bg-grey',
                children=[])
            ])
    ])


@app.callback(Output('datadropdown', 'options'), Input('dataradio', 'value'))

def dropdown_options(radio_value):
    
    if radio_value == ' Economic':
        options = [{'label': x, 'value': x} for x in test_options1]
    else:
        options = [{'label': x, 'value': x} for x in test_options2]
    
    return options


if __name__ == '__main__':
    app.run_server(debug=True)