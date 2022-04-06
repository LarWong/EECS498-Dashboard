import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import base64
import wordcloud

from collections import OrderedDict
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from io import BytesIO
from text import *
from data import *

eco_indicators = get_eco_indicators()
text_data = preprocess_text()
text_ctr = get_counter(text_data['newContentRemove'])
index_mapping = map_word_to_index(text_ctr['Word'])
# print(sentence_mapping)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                                            'height': 490
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
                        html.Br(),
                        html.P('Search for word in vocabulary below'),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='textdropdown',
                                             options=text_ctr['Word'],
                                             searchable=True,
                                             multi=False,
                                             clearable=False,
                                             value=text_ctr['Word'][0],
                                             style={'backgroundColor': '#1E1E1E', 'color': 'white'}),
                            ], style={'fontColor': 'white'}),
                    ]),
            html.Div(
                className='nine columns div-for-charts bg-grey',
                children=[
                    html.Div([
                        html.Div([
                            dcc.Graph(id='textvar', 
                                figure={
                                    'layout': {
                                        'plot_bgcolor': '#1E1E1E',
                                        'paper_bgcolor': '#1E1E1E',
                                        'font': {
                                            'color': 'white'
                                        },
                                        # 'height': 600
                                    },
                            }
                        )], style={'width': '50%'}),
                        html.Div([
                            html.Img(id='wordcloud_img',
                                style={'width': '100%', 'height': '100%'})], 
                                # style={'width': '50%'}
                            )
                        ], style={'display': 'flex'}),
                        # Slider
                        html.Div([
                            dcc.Slider(1, 20, 1,
                                    value=10,
                                    marks={
                                        1: {'label': '1', 'style': {'color': 'white', 'font_size': 50}},
                                        20: {'label': '50', 'style': {'color': 'white', 'font_size': 50}}
                                    },
                                   id='top_n_slider'
                        )], style={'background': '#1e1e1e', 'padding': '5px 5px'}),
                        dash_table.DataTable(
                            id='relevanttext',
                            # page_size=30,
                            style_table={'backgroundColor': 'black',
                                         'fontWeight': 'bold',
                                         'height': '100%'}
                        )
                ], style={'padding': '10px 5px'})
            ]),
])

################## Economic Data ##################
@app.callback(
    Output('ecodropdown1', 'value'),
    Output('ecodropdown2', 'value'),
    Input('btn-swap', 'n_clicks'),
    State('ecodropdown1', 'value'),
    State('ecodropdown2', 'value')
)
def swap_graphs(clicks, ind1, ind2):
    """
    Swap the two economic data graphs
    """
    return ind2, ind1

@app.callback(
    Output('ecodesc1', 'children'),
    Output('ecofig1', 'figure'),
    Input('ecodropdown1', 'value')
)
def output_fig1(ind):
    """
    Display economic data graph and metadata
    """
    return create_graph_and_data(ind)

@app.callback(
    Output('ecodesc2', 'children'),
    Output('ecofig2', 'figure'),
    Input('ecodropdown2', 'value')
)
def output_fig2(ind):
    """
    Display economic data graph and metadata
    """
    return create_graph_and_data(ind)

@app.callback(
    Output('ecomerge', 'figure'),
    Input('ecodropdown1', 'value'),
    Input('ecodropdown2', 'value')
)
def output_merged(ind1, ind2):
    """
    Display economic data merged graph and metadata
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

################## Text Data ##################
@app.callback(
    Output('textvar', 'figure'),
    Output('wordcloud_img', 'src'),
    Input('textdropdown', 'value'),
    Input('top_n_slider', 'value')
)
def output_text_viz(word, top_n):
    """
    Display text data graph
    """
    # Bar chart
    word_index = index_mapping[word]
    freq_data = text_ctr[word_index: word_index + top_n]
    title = '{} Frequency {}'.format(word.upper(), 
                                     '' if top_n == 1 else 'and the Next {}Largest Word(s)'.format(
                                         '' if top_n == 2 else str(top_n-1) + ' '))
    
    # Word Cloud
    img = BytesIO()
    generate_word_cloud(freq_data).save(img, format='PNG')
    
    return generate_bar_data(freq_data, title), 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(
    Output('relevanttext', 'data'),
    Input('textdropdown', 'value'),
)
def output_text(word):
    """
    Display text data graph
    """
    t = text_data['content'][sentence_mapping[word]]
    print(sentence_mapping[word])
    # print(t)
    # for x in t:
    #     print(x)

if __name__ == '__main__':
    app.run_server(debug=True)