import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
from utility.form_group import formGroup

import skrf as rf
from skrf.time import detect_span

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="sub_page",
            children=[
                html.Div(
                    children=[
                        html.H3(
                            className="product",
                            children=[
                                "投資試算表"
                            ],
                        ),
                        formGroup,
                    ]
                ),
            ],
        )
    ],
)


@app.callback(
    Output(component_id="case_name_row_output", component_property='children'),
    Input(component_id="case_name_row", component_property='value')
    )
def update_output_div_case_name_row(input_value):
    return (input_value)


if __name__ == "__main__":
    app.run_server(debug=True)
