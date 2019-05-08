"""Dash interface"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd

DF_EN = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
DF_FR = DF_EN.copy(deep=True)
DF_FR.rename(columns={
    'State': 'Etat',
    'Installed Capacity (MW)': 'Capacite installee (MW)',
    "Number of Solar Plants": "Nombre d'installations solaires"
},
             inplace=True)


def generate_table(dataframe):
    """Generate table from DataFrame"""
    return dash_table.DataTable(id="table",
                                columns=[{
                                    "name": i,
                                    "id": i
                                } for i in dataframe.columns],
                                data=dataframe.to_dict('records'))


APP = dash.Dash(__name__)
APP.layout = html.Div([
    html.Div(id="output-container-button",
             children="Enter a hashtag and press submit"),
    html.Div(
        dcc.Input(id="input-box", type="text", placeholder='Search',
                  value='')),
    html.Button("Submit", id="button"),
    html.H4(children="My nice table"),
    generate_table(DF_EN),
])


@APP.callback(
    [
        dash.dependencies.Output("table", "columns"),
        dash.dependencies.Output("table", "data")
    ],
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State("input-box", "value")],
)
def update_output(n_clicks, value):
    """Update table"""
    if value == "fr":
        columns = [{"name": i, "id": i} for i in DF_FR.columns]
        data = DF_FR.to_dict('records')
        return columns, data
    else:
        columns = [{"name": i, "id": i} for i in DF_EN.columns]
        data = DF_EN.to_dict('records')
        return columns, data


if __name__ == "__main__":
    APP.run_server(debug=True)
