"""Dash interface"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_bootstrap_components as dbc
import pandas as pd

DF = pd.read_csv(
    "/home/andrea/Perso/Dev/ncc2019_more-in-common/data/derugy_csv/hashtags.csv"
)


def generate_table(dataframe):
    """Generate table from DataFrame"""
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict("records"),
    )


APP = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
APP.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        id="output-container-button",
                        children="Select the folder where the tweets have been downloaded",
                    ),
                    width={"size": 8, "offset": 1},
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Upload(html.Button("Choose folder")),
                    width={"size": 8, "offset": 1},
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Input(
                        id="input-box",
                        type="text",
                        placeholder="Tweets folder",
                        value="",
                    ),
                    width={"size": 8, "offset": 1},
                )
            ]
        ),
        dbc.Row([html.H4(children="Hashtags table")]),
        dbc.Row([generate_table(DF)]),
    ]
)


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
