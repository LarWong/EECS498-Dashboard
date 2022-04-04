import json
import pandas as pd
from keys import FRED_API_KEY
from fredapi import Fred

ECONOMIC_INDICATORS = json.load(open('assets/identifiers.json'))['economic_indicators']
FRED = Fred(FRED_API_KEY)

def get_eco_indicators():
    """
    Get list of economic indicators from json
    """
    return list(ECONOMIC_INDICATORS.keys())

def get_fred_data(indicator, drop=True):
    """
    Quwery Fred API for series data
    """
    if indicator not in ECONOMIC_INDICATORS:
        return {'status': False, 'metadata': None, 'data': None}

    metadata = FRED.search(ECONOMIC_INDICATORS[indicator])
    data = FRED.get_series_latest_release(ECONOMIC_INDICATORS[indicator]).to_frame().reset_index(drop=False)
    data.columns = ['Date', metadata['units'][0]]
    return {'status': True , 'metadata': metadata, 'data': data.dropna() if drop else data}

def get_paired_data(first_ind, second_ind):
    """
    Merge two economic indicator data based on common dates of measurement
    """
    if first_ind not in ECONOMIC_INDICATORS or second_ind not in ECONOMIC_INDICATORS:
        return None
    
    first_ind_data = get_fred_data(first_ind)
    second_ind_data = get_fred_data(second_ind)
    
    merged = pd.merge(first_ind_data['data'], second_ind_data['data'], how='inner', on=['Date','Date'])
    
    return {'status': True, 'indicators': [first_ind_data, second_ind_data], 'merged': merged}

def search_fred(indicator):
    """
    Search Fred API for relevant economic indicators
    For testing purposes
    """
    try:
        metadata = FRED.search(ECONOMIC_INDICATORS[indicator])
        return {'status': True , 'metadata': metadata}
    except:
        return {'status': False , 'metadata': None}

