"""Dash interface"""

import os

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Modes",
            children=[
                dbc.DropdownMenuItem("Data Collection"),
                dbc.DropdownMenuItem("Data Analysis"),
            ],
        ),
    ],
    brand="More in Common: Twitter analysis",
    brand_href="#",
    sticky="top",
)

key_input = dbc.FormGroup(
    [
        dbc.Label("Key input:", html_for="example-email-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="key-input", placeholder="Enter keyword to track"
            ),
            width=10,
        ),
    ],
    row=True,
)

query_name = dbc.FormGroup(
    [
        dbc.Label("Query name:", html_for="example-password-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text",
                id="query-name-input",
                placeholder="Enter query name (should not contain any space)",
            ),
            width=10,
        ),
    ],
    row=True,
)

query_type_dropdown = dbc.FormGroup(
    [
        dbc.Label("Type of Query:", html_for="dropdown"),
        dcc.Dropdown(
            id="query-type",
            options=[
                {"label": "Search", "value": 1},
                {"label": "Track", "value": 2},
            ],
        ),
    ]
)

add_query_button = html.Div(
    [
        dbc.Button("Add query", color="primary", className="mr-1", id="add-query-button"),
    ]
)

query_input = dbc.Container(
    [
        query_name,
        key_input,
        query_type_dropdown,
        add_query_button
    ],
    className="custom-container container"
)


query_list_component = html.Div(
    [
    html.Div(id='controls-container', children='Enter a value and press submit')
    ]
)


list_query = [];

def generate_control_id(value):
    return 'Control {}'.format(value)


@app.callback(
    Output('controls-container', 'children'),
    [Input('add-query-button', 'n_clicks')])
def update_output(n_clicks):
    DYNAMIC_QUERY_LIST = {}
    for each in range(len(list_query)):
        DYNAMIC_QUERY_LIST[each+1]= dcc.Input(
            id=generate_control_id(each+1),
            value=generate_control_id(each+1)
        )

    List = []
    for i in range(len(list_query)):
        List.append(DYNAMIC_QUERY_LIST[i+1])

    list_query.append("1");

    return html.Div(
        List
    )





app.layout = html.Div([navbar, query_input, query_list_component]);

if __name__ == "__main__":
    app.run_server(debug=True)
