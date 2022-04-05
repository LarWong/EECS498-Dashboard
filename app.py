import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
from data import get_eco_indicators, get_fred_data, get_paired_data, create_graph_and_data

eco_indicators = get_eco_indicators()
test_x = ['a', 'b', 'c']
test_y = [10, 1, 5]

data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)

df = pd.DataFrame(
    OrderedDict([(name, col_data * 10) for (name, col_data) in data.items()])
)

app = Dash(__name__)

app.layout = html.Div(
    children=[
        # ECONOMIC
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='three columns div-user-controls',
                    children=[
                        html.H1('ECONOMIC DATA VISUALIZATION'),
                        html.P('Visualising ECONOMIC data.'),

                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='ecodropdown1',
                                             options=eco_indicators,
                                             value='Real GDP',
                                             clearable=False,
                                             searchable=False,
                                             style={'backgroundColor': '#1E1E1E', 'background': '#1E1E1E'}),
                            ]),
                        html.H3('Top Left Description'),
                        
                        html.Div(id='ecodesc1'),
                        
                        html.Br(),
                        
                        html.Div([
                                html.Button('SWAP', id='btn-swap', n_clicks=0, style={'width': '100%', 'color': 'white'}),
                            ]),
                        
                        html.Br(),
                        
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='ecodropdown2',
                                             options=eco_indicators,
                                             value='Real GDP',
                                             clearable=False,
                                             searchable=False,
                                             style={'backgroundColor': '#1E1E1E'}),
                            ]),
                        
                        
                        html.H3('Top Right Description'),
                        
                        html.Div(id='ecodesc2'),
                        # html.Div(),
                    ]),
                html.Div(
                    className='nine columns div-for-charts bg-grey',
                    children=[
                        html.Div([
                                html.Div([dcc.Graph(id='ecofig1', 
                                        figure={
                                            'layout': {
                                                'plot_bgcolor': '#1E1E1E',
                                                'paper_bgcolor': '#1E1E1E',
                                                'font': {
                                                    'color': 'white'
                                                },
                                                'height': 600
                                            }
                                        }
                                )], style={'width': '50%'}),
                                html.Div([dcc.Graph(id='ecofig2', 
                                        figure={
                                            'layout': {
                                                'plot_bgcolor': '#1E1E1E',
                                                'paper_bgcolor': '#1E1E1E',
                                                'font': {
                                                    'color': 'white'
                                                },
                                                'height': 600
                                            }
                                        }
                                )], style={'width': '50%'}),
                        ], style={'display': 'flex', 'width': '100%'}),
                        dcc.Graph(id='ecomerge', 
                                      figure={
                                        'layout': {
                                            'plot_bgcolor': '#1E1E1E',
                                            'paper_bgcolor': '#1E1E1E',
                                            'font': {
                                                'color': 'white',
                                                'size': 15
                                            },
                                            'height': 500
                                        }
                                      }
                            ),
                    ], style={'padding': '10px 5px'}
                    ), 
            ]),
        
        # TEXT
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='three columns div-user-controls',
                    children=[
                        html.H2('TEXT VISUALIZATION'),
                        html.P('Visualising TEXT data.'),

                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='textdropdown',
                                             options=eco_indicators,
                                             searchable=False,
                                             style={'backgroundColor': '#1E1E1E'}),
                            ]),
                    ]),
            html.Div(
                className='nine columns div-for-charts bg-grey',
                children=[
                    html.Div([
                        html.Div([
                            html.Img(src='assets/test.png', 
                                style={'width': '100%', 'height': '100%', 'objectFit': 'contain'})], 
                                style={'width': '50%'}
                            ),
                        html.Div([
                            dcc.Graph(id='textvar', 
                                figure={
                                    'layout': {
                                        'plot_bgcolor': '#1E1E1E',
                                        'paper_bgcolor': '#1E1E1E',
                                        'font': {
                                            'color': 'white'
                                        },
                                        'height': 550
                                    },
                            }
                        )], style={'width': '50%'})
                        ], style={'display': 'flex'}),
                        # Slider
                        html.Div([
                            dcc.Slider(0, 50, 1,
                                   value=10,
                                    marks={
                                        0: {'label': '0', 'style': {'color': '#77b0b1', 'font_size': 20}},
                                        50: {'label': '50', 'style': {'color': '#f50', 'font_size': 20}}
                                    },
                                   id='top_n_slider'
                        )], style={'padding': '30px 5px'}),
                        html.Div([dash_table.DataTable(
                            data=df.to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in df.columns],
                            page_action='none',
                            style_table={'height': '300px', 'overflowY': 'auto'}
                        )])
                ], style={'padding': '30px 5px'})
            ]),
])

@app.callback(
    Output('ecodropdown1', 'value'),
    Output('ecodropdown2', 'value'),
    Input('btn-swap', 'n_clicks'),
    State('ecodropdown1', 'value'),
    State('ecodropdown2', 'value')
)
def swap_graphs(clicks, ind1, ind2):
    """
    Swap the two graphs
    """
    return ind2, ind1

@app.callback(
    Output('ecodesc1', 'children'),
    Output('ecofig1', 'figure'),
    Input('ecodropdown1', 'value')
)
def output_fig1(ind):
    """
    Display graph and metadata
    """
    return create_graph_and_data(ind)

@app.callback(
    Output('ecodesc2', 'children'),
    Output('ecofig2', 'figure'),
    Input('ecodropdown2', 'value')
)
def output_fig2(ind):
    """
    Display graph and metadata
    """
    return create_graph_and_data(ind)

@app.callback(
    Output('ecomerge', 'figure'),
    Input('ecodropdown1', 'value'),
    Input('ecodropdown2', 'value')
)
def output_merged(ind1, ind2):
    """
    Display graph and metadata
    """
    merged_data = get_paired_data(ind1, ind2)['merged']
    indicators = merged_data.columns[1:]
    
    fig = px.scatter(merged_data[indicators], x=indicators[0], y=indicators[1],
                     title="{} vs. {}".format(ind1, ind2))
    fig.update_traces(line_color='#ff0000')
    
    fig.update_layout(
        transition_duration=500,
        title_font_family="Times New Roman",
        title_font_color='white',
        title_font_size=25,
        font_color='white',
        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)