import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import plotly.express as px
import pandas as pd
import numpy as np

import requests
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

hashtag = 'netflix'
consumer_key = '5sFcqEobkFobWD6r3L4T5mUiv'
consumer_secret = 'zbiOdLyUbtLYbbiqXrz2vExyJAvo1cJS6jaJGYbFZ9r3Ve9pCj'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAM1eGwEAAAAAyBh6seqjqT7jP9S3yCqPVKiHYSA%3DXd5j3spF7bWJvUHgCayI3LzEpUbf6JiidMPiSQiPs9fAdDVVTk'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(
    html.Div([
        html.H4('Twitter Live Keywords Analysis'),
        dcc.Input(id='htag', type='text', placeholder='track hashtag'),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    df = get_tweets_df()
    fig = px.bar(df, x=df.index, y=df, barmode="group")
    return fig

@app.callback(
    Output('container-button-basic', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('htag', 'value')])
def update_output(n_clicks, htag):
    global hashtag 
    if htag:
        hashtag = htag
    return f'Tracking {hashtag} as defualt.'


def get_tweets_df():
    global hashtag
    query = f'"{hashtag}" -is:retweet'
    print(query)
    tweet_fields = "tweet.fields=author_id,public_metrics,source"
    url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&{tweet_fields}&max_results=100'
    headers = {'Authorization': f'Bearer {bearer_token}'}
    
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code!=200:
        print(response.text)
    
    df = pd.DataFrame(response.json()['data'])
    df['len'] = df.text.str.len()
    df.text = df.text.apply(lambda x: [i for i in x.lower().split() if i.isalpha()])
    stopwords.words('english')[:5]
    
    stop = stopwords.words('english') + []
    df.text = df.text.apply(lambda x: [i for i in x if i not in stop])
    
    lemmatizer = WordNetLemmatizer()
    
    df.text = df.text.apply(lambda x: [lemmatizer.lemmatize(i) for i in x])
    
    hval = pd.Series(Counter([j for i in df.text for j in i])).sort_values(ascending=False)[:20]
    hval = hval + np.random.randint(1, 10, len(hval))
    hval = hval.sort_values()
    return hval

if __name__ == '__main__':
    app.run_server(debug=True)
