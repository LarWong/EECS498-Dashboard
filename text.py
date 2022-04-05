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
from wordcloud import WordCloud
from nltk.corpus import stopwords
from collections import Counter

# get stopwords
nltk.download('stopwords')
stop = set(stopwords.words('english'))
stop.update(['would', 'should', 'said', 'also'])

def preprocess_text():
    """
    Preprocess text
    TODO: Replace with real data
    """
    # read in example text
    df = pd.read_csv('./assets/example_text/bbc-news-data.csv', sep='\t')

    # make content lower case and remove stopwords
    df['newContent'] = df['content'].apply(lambda x: ' '.join([word for word in x.lower().split() if word not in stop]))

    #Remove Punctuations
    df['newContentRemove'] = df['newContent'].str.replace('[^\w\s]','', regex=True)
    
    return df

def get_counter(df):
    """
    Count the frequency of words
    """
    ctr = Counter()
    for row in df.values:
        ctr.update(row.split())
    words, count = map(list, zip(*ctr.most_common()))
    return pd.DataFrame({'Word': words, 'Frequency': count})

def generate_bar_data(ctr, top_n, start=0):
    """
    Create bar chart of top n words by frequency
    """
    spliced_data = ctr[start:top_n].reset_index(drop=True)
    
    fig = px.bar(ctr[upper_idx:lower_idx].reset_index(drop=True), x='Word', y='Frequency')  
    fig.update_layout(
        transition_duration=500,
        title_font_family='Times New Roman',
        title_font_color='white',
        title_font_size=25,
        font_color='white',
        font_size=100,
        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',
        hoverlabel=dict(
            font_size=50,
        )
    )
    
    return fig

def generate_word_cloud(ctr, top_n, start=0):
    """
    Create word cloud of top n words by frequency
    """
    spliced_data = ctr[start:top_n].reset_index(drop=True)
    
    data = spliced_data.set_index('Word').to_dict()['Frequency']
    
    wc = WordCloud(width=800, height=400, max_words=200)
    wc.generate_from_frequencies(data)
    
    return wc.to_image()

# @app.callback(dd.Output('image_wc', 'src'), [dd.Input('image_wc', 'id')])
# def make_image(b):
#     img = BytesIO()
#     plot_wordcloud(data=dfm).save(img, format='PNG')
#     return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

    