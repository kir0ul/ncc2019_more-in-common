"""Dash interface"""

import os

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_bootstrap_components as dbc
import pandas as pd

from process import read_json_tweets
from process.aggregate import Aggregate


ROW_STYLE = {"marginBottom": 30, "marginTop": 30}
DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data"
)

IMPORT_FOLDER = "derugy"


def compute_dataframe(tweets_folder):
    import_path = os.path.join(DATA_PATH, tweets_folder)
    export_path = os.path.join(import_path, "CSV")

    read_json_tweets.main(import_path, export_path)
    aggregate = Aggregate(export_path)
    res = aggregate.top_hashtags()
    return res


DF = compute_dataframe(IMPORT_FOLDER)


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
                        dcc.Dropdown(options=get_tweets_folders_names(DATA_PATH)),
                        width=12,
                    ),
                    justify="center",
                    style=ROW_STYLE,
                ),
                dbc.Row(
                    [generate_html_table_from_df(DF)], justify="center", style=ROW_STYLE
                ),
            ]
        )
    ]
)


# @APP.callback(
#     Output("input-box", "value"),
#     [Input("choose-folder", "contents")],
#     [State("choose-folder", "filename")],
# )
# def update_output(list_of_contents, list_of_names):
#     if list_of_names:
#         children = list_of_names
#         return children


# @APP.callback(
#     [
#         dash.dependencies.Output("table", "columns"),
#         dash.dependencies.Output("table", "data"),
#     ],
#     [dash.dependencies.Input("button", "n_clicks")],
#     [dash.dependencies.State("input-box", "value")],
# )
# def update_output(n_clicks, value):
#     """Update table"""
#     columns = [{"name": i, "id": i} for i in DF.columns]
#     data = DF.to_dict("records")
#     return columns, data


if __name__ == "__main__":
    APP.run_server(debug=True)
