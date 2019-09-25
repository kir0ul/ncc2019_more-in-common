"""Dash interface"""

import os

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

from process import read_json_tweets
from process.aggregate import Aggregate


ROW_STYLE = {"marginBottom": 30, "marginTop": 30}
DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data"
)


def compute_dataframe(tweets_folder):
    import_path = os.path.join(DATA_PATH, tweets_folder)
    export_path = os.path.join(import_path, "CSV")

    read_json_tweets.main(import_path, export_path)
    aggregate = Aggregate(export_path)
    res = aggregate.top_hashtags()
    return res


def get_tweets_folders_names(folder_path):
    list_dir = os.listdir(folder_path)
    tweets_folders = []
    for item in list_dir:
        if os.path.isdir(os.path.join(folder_path, item)):
            tweets_folders.append({"label": item, "value": item})
    return tweets_folders


def generate_html_table_from_df(dataframe):
    """Generate table from DataFrame"""
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict("records"),
    )


APP = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
APP.layout = html.Div(
    [
        dbc.Container(
            children=[
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id="dropdown", options=get_tweets_folders_names(DATA_PATH)
                        ),
                        width=12,
                    ),
                    justify="center",
                    style=ROW_STYLE,
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            id="submit",
                            n_clicks=0,
                            children="Submit",
                            block=True,
                            color="primary",
                        ),
                        width=12,
                    ),
                    justify="center",
                    style=ROW_STYLE,
                ),
                dbc.Row([html.Div(id="results")], justify="center", style=ROW_STYLE),
            ]
        )
    ]
)


@APP.callback(
    [Output("results", "children")],
    [Input("dropdown", "value")],
    [State("submit", "children")],
)
def update_table(value, children):
    """Update table"""

    if value:
        df = compute_dataframe(value)
        dt = generate_html_table_from_df(df)
        return [dt]
    else:
        return [html.Div(id="results")]


if __name__ == "__main__":
    APP.run_server(debug=True)
