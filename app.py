import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import re
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
top_n = 10
# print(text_ctr.tail())
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
                            html.Button('SWAP', id='btn-swap', n_clicks=0,
                                        style={'width': '100%', 'color': 'white'}),
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
                        html.Div(id='wordstats')
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
                            dcc.Slider(0, len(text_ctr['Word']) - top_n, 1,
                                       value=0,
                                       marks={
                                1: {'label': 'Frequent', 'style': {'color': 'white', 'font_size': 50}},
                                len(text_ctr['Word']) - top_n: {'label': 'Rare', 'style': {'color': 'white', 'font_size': 50}}
                            },
                                id='word_slider'
                            )], style={'background': '#1e1e1e', 'padding': '5px 5px'}),
                        html.Div(id='relevanttext')
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
    '''
    Swap the two economic data graphs
    '''
    return ind2, ind1


@app.callback(
    Output('ecodesc1', 'children'),
    Output('ecofig1', 'figure'),
    Input('ecodropdown1', 'value')
)
def output_fig1(ind):
    '''
    Display economic data graph and metadata
    '''
    return create_graph_and_data(ind)


@app.callback(
    Output('ecodesc2', 'children'),
    Output('ecofig2', 'figure'),
    Input('ecodropdown2', 'value')
)
def output_fig2(ind):
    '''
    Display economic data graph and metadata
    '''
    return create_graph_and_data(ind)


@app.callback(
    Output('ecomerge', 'figure'),
    Input('ecodropdown1', 'value'),
    Input('ecodropdown2', 'value')
)
def output_merged(ind1, ind2):
    '''
    Display economic data merged graph and metadata
    '''
    merged_data = get_paired_data(ind1, ind2)['merged']
    indicators = merged_data.columns[1:]

    fig = px.scatter(merged_data[indicators], x=indicators[0], y=indicators[1],
                     title='{} vs. {}'.format(ind1, ind2))
    fig.update_traces(line_color='#ff0000')

    fig.update_layout(
        transition_duration=500,
        title_font_family='Times New Roman',
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
    Input('word_slider', 'value')
)
def output_text_bar(word_idx):
    '''
    Display text data graph
    '''
    # Bar chart
    # word_index = index_mapping[word]
    word = text_ctr['Word'][word_idx]
    freq_data = text_ctr[word_idx: word_idx + top_n + 1]
    title = '{} Frequency {}'.format(
        word.upper(), 'and the Next {} Largest Word(s)'.format(top_n))

    # Word Cloud
    img = BytesIO()
    generate_word_cloud(freq_data).save(img, format='PNG')

    return generate_bar_data(freq_data, title), 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


@app.callback(
    Output('word_slider', 'value'),
    Input('textdropdown', 'value')
)
def update_slider(word):
    '''
    Move slider to match selected word in dropdown
    '''
    return index_mapping[word]


@app.callback(
    Output('wordstats', 'children'),
    Input('textdropdown', 'value')
)
def output_word_stats(word):
    '''
    Display statistics of word
    '''
    data_description = ['Frequency: {}'.format(text_ctr['Frequency'][index_mapping[word]]),
                        'Number of Texts: {}'.format(
                            len(sentence_mapping[word])),
                        "Percentile: {:.0f}".format((1-((index_mapping[word])/len(index_mapping)))*100)]
    return [html.P(x) for x in data_description]


@app.callback(
    Output('relevanttext', 'children'),
    Input('textdropdown', 'value'),
)
def output_text(word):
    '''
    Display text data graph
    '''
    df = pd.DataFrame(text_data['content'][list(
        sentence_mapping[word])]).reset_index(drop=True)
    df.columns = ['Text']
    df['Text'] = df['Text'].apply(lambda x: re.sub(
        r'({})'.format(word), r'**\g<1>**', x, flags=re.IGNORECASE))
    return dash_table.DataTable(df.to_dict('records'),
                                [{'name': i, 'id': i, 'type': 'text',
                                    'presentation': 'markdown'} for i in df.columns],
                                style_data={
                                    'whiteSpace': 'normal',
                                    'textAlign': 'left'
    },
        style_header={'backgroundColor': 'black',
                      'color': 'white',
                      'textAlign': 'center'},
        style_cell={
                                    'backgroundColor': 'rgb(50, 50, 50)',
                                    'color': 'white',
                                    'hover': 'black'
    },
        style_table={'height': '500px', 'overflowY': 'auto', 'hover': 'black'})


@app.callback(
    Output('textdropdown', 'value'),
    Input('textvar', 'clickData')
)
def update_from_bar(word):
    '''
    Display statistics of word by clicking on bars
    '''
    if not word:
        return text_ctr['Word'][0]
    # print(word['label'])
    return word['points'][0]['label']


if __name__ == '__main__':
    app.run_server(debug=True)
