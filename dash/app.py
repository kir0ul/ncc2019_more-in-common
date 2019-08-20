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

ROW_STYLE = {"marginBottom": 30, "marginTop": 30}


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
        dbc.Container(
            children=[
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            options=[
                                {"label": "Hashtags", "value": "hashtags"},
                                {"label": "Tweets", "value": "tweets"},
                                {"label": "Users", "value": "users"},
                            ]
                        ),
                        width=12,
                    ),
                    justify="center",
                    style=ROW_STYLE,
                ),
                dbc.Row([generate_table(DF)], justify="center", style=ROW_STYLE),
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
