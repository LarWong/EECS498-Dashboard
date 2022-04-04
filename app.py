import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from data import get_eco_indicators, get_fred_data

test_options1 = ['a', 'b', 'c']
test_options2 = ['d', 'e', 'f']
test_value = [1, 2, 3]
eco_indicators = get_eco_indicators()


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='three columns div-user-controls',
                    children=[
                        html.H2('ECONOMIC VISUALIZATION'),
                        html.P('Visualising ECONOMIC data.'),

                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='ecodropdown1',
                                             options=eco_indicators,
                                             value='Real GDP',
                                             clearable=False,
                                             searchable=False,
                                             style={'backgroundColor': '#1E1E1E'}),
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
                    className='nine columns bg-grey',
                    children=[
                        html.Div([
                                html.Div([dcc.Graph(id='ecofig1', 
                                        figure={
                                            'layout': {
                                                'plot_bgcolor': '#1E1E1E',
                                                'paper_bgcolor': '#1E1E1E',
                                                'font': {
                                                    'color': 'white'
                                                }
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
                                                }
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
                                                'color': 'white'
                                            }
                                        }
                                      }
                            ),
                    ], style={'padding': '10px 5px', 'white-space': 'nowrap'}
                    ), 
            ]),
        
        
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='four columns div-user-controls',
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
                className='eight columns div-for-charts bg-grey',
                children=[])
            ]),
])

@app.callback(
    Output('ecodropdown1', 'value'),
    Output('ecodropdown2', 'value'),
    Input('btn-swap', 'n_clicks')
)
def swap_graphs(ind1, ind2):
    print('yo')
    return ind2, ind1

@app.callback(
    Output('ecodesc1', 'children'),
    Output('ecofig1', 'figure'),
    Input('ecodropdown1', 'value')
)
def output_fig(ind):
    fred_info = get_fred_data(ind)
    metadata = fred_info['metadata']
    data = fred_info['data']
    
    data_description = ['{}'.format(metadata['title'][0]),
                        'Unit: {}'.format(metadata['units'][0]),
                        'Frequency: {}'.format(metadata['frequency'][0]),
                        'Last Updated: {}'.format(metadata['last_updated'][0])]

    fig = px.line(data, x='Date', y=metadata['units'][0], title=ind)
    fig.update_traces(line_color='#ff0000', hovertemplate=None)
    
    fig.update_layout(
        transition_duration=500,
        title_font_family="Times New Roman",
        title_font_color='white',
        title_font_size=25,
        font_color='white',
        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',
    )
    
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ]),
                font=dict(color='black')
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
)

    date_min = pd.to_datetime(data['Date']).min()
    date_max = pd.to_datetime(data['Date']).max()
    slider_value = data['Date'].max()
    
    
    return [html.P(x) for x in data_description], fig


if __name__ == '__main__':
    app.run_server(debug=True)