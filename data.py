import json
import pandas as pd
from keys import FRED_API_KEY
from fredapi import Fred

ECONOMIC_INDICATORS = json.load(open('assets/identifiers.json'))['economic_indicators']
FRED = Fred(FRED_API_KEY)

def get_fred_data(indicator, drop=True):
    if indicator not in ECONOMIC_INDICATORS:
        return {'status': False, 'metadata': None, 'data': None}

    metadata = FRED.search(ECONOMIC_INDICATORS[indicator])
    data = FRED.get_series_latest_release(ECONOMIC_INDICATORS[indicator])
    data.columns = ['Data', metadata['units']]
    return {'status': True , 'metadata': metadata, 'data': data.dropna() if drop else data}

def search_fred(indicator):
    try:
        metadata = FRED.search(ECONOMIC_INDICATORS[indicator])
        return {'status': True , 'metadata': metadata}
    except:
        return {'status': False , 'metadata': None}

