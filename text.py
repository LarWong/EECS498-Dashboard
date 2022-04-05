import json
import collections
import pandas as pd
import nltk
import wordcloud
import plotly
import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

from nltk.corpus import stopwords
from collections import Counter

# get stopwords
nltk.download('stopwords')
stop = set(stopwords.words('english'))
stop.update(['would', 'should', 'said', 'also'])
print('said' in stop)

def preprocess_text():
    # read in example text
    df = pd.read_csv('./assets/example_text/bbc-news-data.csv', sep='\t')

    # make content lower case and remove stopwords
    df['newContent'] = df['content'].apply(lambda x: ' '.join([word for word in x.lower().split() if word not in stop]))

    #Remove Punctuations
    df['newContentRemove'] = df['newContent'].str.replace('[^\w\s]','', regex=True)
    
    return df

def get_counter(df):
    ctr = Counter()
    for row in df.values:
        ctr.update(row.split())
    words, count = map(list, zip(*ctr.most_common()))
    return pd.DataFrame({'Word': words, 'Frequency': count})

def generate_bar_data(ctr, top_n):
    
    fig = px.bar(ctr[:top_n], x='Word', y='Frequency')
    
    fig.update_layout(
        xaxis={
            # 'range': [ctr['AAPL_x']., df['AAPL_x'].max()],
            'rangeslider': {'visible': True},
        }
    )    
    
    fig.update_layout(
        transition_duration=500,
        title_font_family='Times New Roman',
        title_font_color='white',
        title_font_size=25,
        font_color='white',
        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',
    )
    
    fig.show()


    