import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from keys import FRED_API_KEY
from fredapi import Fred

ECONOMIC_INDICATORS = json.load(
    open('assets/identifiers.json'))['economic_indicators']
FRED = Fred(FRED_API_KEY)


def get_eco_indicators():
    '''
    Get list of economic indicators from json
    '''
    return list(ECONOMIC_INDICATORS.keys())


def get_fred_data(indicator, drop=True):
    '''
    Quwery Fred API for series data
    '''
    if indicator not in ECONOMIC_INDICATORS:
        return {'status': False, 'metadata': None, 'data': None}

    metadata = FRED.search(ECONOMIC_INDICATORS[indicator])
    data = FRED.get_series_latest_release(
        ECONOMIC_INDICATORS[indicator]).to_frame().reset_index(drop=False)
    data.columns = ['Date', metadata['units'][0]]
    return {'status': True, 'metadata': metadata, 'data': data.dropna() if drop else data}


def get_paired_data(first_ind, second_ind):
    '''
    Merge two economic indicator data based on common dates of measurement
    '''
    if first_ind not in ECONOMIC_INDICATORS or second_ind not in ECONOMIC_INDICATORS:
        return {'status': False, 'merged': None}

    first_ind_data = get_fred_data(first_ind)
    second_ind_data = get_fred_data(second_ind)

    merged = pd.merge(
        first_ind_data['data'], second_ind_data['data'], how='inner', on=['Date', 'Date'])

    return {'status': True, 'merged': merged}


def search_fred(indicator):
    '''
    Search Fred API for relevant economic indicators
    For testing purposes
    '''
    try:
        metadata = FRED.search(ECONOMIC_INDICATORS[indicator])
        return {'status': True, 'metadata': metadata}
    except:
        return {'status': False, 'metadata': None}


def create_graph_and_data(ind):
    '''
    Fetch economic indicator data and create line plot with data
    '''
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
        title_font_family='Times New Roman',
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
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ]),
                font=dict(color='black')
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )

    return [html.P(x) for x in data_description], fig
