import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np


import skrf as rf
from skrf.time import detect_span


external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

dut = rf.Network("dut.s2p")


######## ## the APP

email_input = dbc.Row(
    [
        dbc.Label("Email", html_for="example-email-row", width=2),
        dbc.Col(
            dbc.Input(
                type="email",
                placeholder="Enter email"
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

password_input = dbc.Row(
    [
        dbc.Label("Password", html_for="example-password-row", width=2),
        dbc.Col(
            dbc.Input(
                type="password",
                placeholder="Enter password",
            ),
            width=10,
        ),
    ],
    className="mb-3",
)


formGroup = html.Div(
            dbc.Card(
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(
                            [
                                html.H5("Form1"),
                                dbc.Form(
                                    [
                                        email_input,
                                        password_input,
                                    ],
                                ),
                            ]
                        ),
                        dbc.ListGroupItem(
                            [
                                html.H5("Form2"),
                                dbc.Form(
                                    [
                                        email_input,
                                        password_input,
                                    ],
                                ),
                            ]
                        ),
                        dbc.ListGroupItem(
                            [
                                html.H5("Form3"),
                                dbc.Form(
                                    [
                                        email_input,
                                        password_input,
                                    ],
                                ),
                            ]
                        ),
                    ],
                    flush=True,
                ),
                className="w-50",
            ),
    )

app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="sub_page",
            children=[
                # html.Div(className='col-2'),
                html.Div(
                    children=[
                        formGroup
                    ]
                ),
            ],
        )
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
