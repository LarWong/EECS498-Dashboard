import json
import collections
import pandas as pd
import nltk
import wordcloud
import plotly
import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, html, dcc
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter

# get stopwords
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# get tokenizer
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

stop = set(stopwords.words('english'))
# manually add more stopwords
stop.update(['would', 'should', 'said', 'also',
            'n\'t', 'wouldnt', 'get', 'told'])
sentence_mapping = {}
ctr = Counter()


def map_word_to_index(df):
    '''
    Map word to all text that contains word
    '''
    mapping = {}
    for i in range(len(df)):
        mapping[df[i]] = i
    return mapping


def preprocess_text():
    '''
    Preprocess text
    TODO: Replace with real data
    '''
    # read in example text
    df = pd.read_csv('./assets/reuters_headlines.csv')
    df.rename(columns={'Headlines': 'content'}, inplace=True)
    del df['Time']
    del df['Description']
    

    cleaned_sentence = []
    for sent_idx in range(len(df['content'])):
        cleaned_tokens = [w.lower() for w in word_tokenize(df['content'][sent_idx])
                          if (len(w) > 2 and (w.lower() not in stop))]
        for token in cleaned_tokens:
            if token not in sentence_mapping:
                sentence_mapping[token] = set()
            sentence_mapping[token].add(sent_idx)
        cleaned_sentence.append(' '.join)
        ctr.update(cleaned_tokens)

    df['newContentRemove'] = pd.DataFrame(cleaned_sentence)

    return df


def get_counter(df):
    '''
    Count the frequency of words
    '''
    words, count = map(list, zip(*ctr.most_common()))
    return pd.DataFrame({'Word': words, 'Frequency': count})


def generate_bar_data(df, title):
    '''
    Create bar chart of top n words by frequency
    '''

    fig = px.bar(df.reset_index(drop=True), x='Word',
                 y='Frequency', title=title)
    fig.update_layout(
        # transition_duration=300,
        title_font_family='Times New Roman',
        title_font_color='white',
        title_font_size=15,
        font_color='white',
        font_size=12,
        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',
        hoverlabel=dict(
            font_size=20,
        )
    )

    return fig


def generate_word_cloud(df):
    '''
    Create word cloud of top n words by frequency
    '''
    data = dict(zip(df['Word'], df['Frequency']))

    wc = WordCloud(random_state=2, width=800, height=400,
                   colormap='Set3', background_color='#1e1e1e')
    wc.generate_from_frequencies(data)

    return wc.to_image()
