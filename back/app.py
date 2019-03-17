from flask import Flask
import json
from flask.json import jsonify
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random
import plotly.io as pio
import pandas as pd

app = Flask(__name__)

# ---------- Hard coded data ----------
WORDS = dir(go)[:30]
WEIGHTS = [random.randint(15, 35) for i in range(30)]

WORDCLOUD_FILE_PATH = "../data/emergency.csv"
NAMES = ["words", "tweets"]
WORDS_DF = pd.read_csv(WORDCLOUD_FILE_PATH, names=NAMES)
WORDS = WORDS_DF[NAMES[0]]
WEIGHTS = WORDS_DF[NAMES[1]]
WEIGHTS = WEIGHTS*100/WEIGHTS.max()+20


@app.route("/")
def api_root():
    """API root"""
    return "<h2>Welcome to the API</h2>"


@app.route("/hashtag/<hashtag>")
def get_hashtag(hashtag):
    """Hashtag route"""

    # Mocked JSON
    mocked_json_path = "../data/api_out.json"
    with open(mocked_json_path, "r") as fh:
        data = fh.readlines()
        data = "".join(data)
    response = json.loads(data)
    response = jsonify(response)

    return response


def generate_wordcloud(words=WORDS, weights=WEIGHTS):

    colors = [
        plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)]
        for i in range(30)
    ]

    data = go.Scatter(
        x=[random.random() for i in range(30)],
        y=[random.random() for i in range(30)],
        mode='text',
        text=words,
        marker={'opacity': 0.3},
        textfont={
            'size': weights,
            'color': colors
        })
    layout = go.Layout({
        'xaxis': {
            'showgrid': False,
            'showticklabels': False,
            'zeroline': False
        },
        'yaxis': {
            'showgrid': False,
            'showticklabels': False,
            'zeroline': False
        }
    })
    fig = go.Figure(data=[data], layout=layout)

    plot(fig)
    pio.write_image(fig, 'fig.svg')


if __name__ == '__main__':
    generate_wordcloud()
