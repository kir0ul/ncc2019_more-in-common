import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


df = pd.read_csv("./data/usa-agricultural-exports-2011.csv")


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])]
        +
        # Body
        [
            html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns])
            for i in range(min(len(dataframe), max_rows))
        ]
    )


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(dcc.Input(id="input-box", type="text")),
        html.Button("Submit", id="button"),
        html.Div(
            id="output-container-button", children="Enter a value and press submit"
        ),
        html.H4(children="US Agriculture Exports (2011)"),
        generate_table(df),
    ]
)


@app.callback(
    dash.dependencies.Output("output-container-button", "children"),
    [dash.dependencies.Input("button", "n_clicks")],
    [dash.dependencies.State("input-box", "value")],
)
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value, n_clicks
    )


if __name__ == "__main__":
    app.run_server(debug=True)
