import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np


import skrf as rf
from skrf.time import detect_span

app = dash.Dash(__name__)
server = app.server

email_input = dbc.Row(
    [
        dbc.Label("Email", html_for="example-email-row", width=2),
        dbc.Col(
            dbc.Input(
                type="email", id="example-email-row", placeholder="Enter email"
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
                id="example-password-row",
                placeholder="Enter password",
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

radios_input = dbc.Row(
    [
        dbc.Label("Radios", html_for="example-radios-row", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="example-radios-row",
                options=[
                    {"label": "First radio", "value": 1},
                    {"label": "Second radio", "value": 2},
                    {
                        "label": "Third disabled radio",
                        "value": 3,
                        "disabled": True,
                    },
                ],
            ),
            width=10,
        ),
    ],
    className="mb-3",
)


form1 = dbc.Form([email_input], className="border border-primary", style={'border-width':'3px', 'border-style':'dashed', 'border-color':'#FFAC55', 'padding':'5px'})
form2 = dbc.Form([password_input, radios_input])
form3 = dbc.Form(
    dbc.Row(
        [
            dbc.Label("Email", width="auto"),
            dbc.Col(
                dbc.Input(type="email", placeholder="Enter email"),
                className="me-3",
            ),
            dbc.Label("Password", width="auto"),
            dbc.Col(
                dbc.Input(type="password", placeholder="Enter password"),
                className="me-3",
                style={'border': 'solid 0.1rem'},
            ),
            dbc.Col(dbc.Button("Submit", color="primary"), width="auto"),
        ],
        className="g-2",
    )
)

form4 = dbc.Form(
    dbc.Row(
        [
            dbc.Label("Email", width="auto"),
            dbc.Col(
                dbc.Input(type="email", placeholder="Enter email"),
                className="me-3",
            ),
            dbc.Label("Password", width="auto"),
            dbc.Col(
                dbc.Input(type="password", placeholder="Enter password"),
                className="me-3",
                style={'border': 'solid 0.1rem'},
            ),
            dbc.Col(dbc.Button("Submit", color="primary"), width="auto"),
        ],
        className="g-2",
    )
)


# the APP
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
                        html.Div(
                            className="row",
                            children=[
                                html.Div(form1),
                                html.Div(form2),
                                html.Div(form3),
                                html.Div(
                                    className="col-4",
                                    children=[
                                        html.Span(
                                            children=[
                                                html.Label(
                                                    "S-parameter: ", className="inline"
                                                ),
                                                dcc.RadioItems(
                                                    id="sparam-radio",
                                                    options=[
                                                        {
                                                            "label": "S11",
                                                            "value": "s11",
                                                        },
                                                        {
                                                            "label": "S21",
                                                            "value": "s21",
                                                        },
                                                        {
                                                            "label": "S12",
                                                            "value": "s12",
                                                        },
                                                        {
                                                            "label": "S22",
                                                            "value": "s22",
                                                        },
                                                    ],
                                                    value="s11",
                                                    labelStyle={
                                                        "display": "inline-block",
                                                        "margin": "6px",
                                                    },
                                                ),
                                            ]
                                        ),
                                        html.Label("Window Type: "),
                                        html.Div(
                                            [
                                                dbc.InputGroup(
                                                    [
                                                        dbc.InputGroupText(
                                                            "$"),
                                                        dbc.Input(
                                                            placeholder="Amount", type="number"),
                                                        # dbc.InputGroupText(
                                                        #     ".00"),
                                                    ],
                                                    className="mb-3",
                                                ),
                                            ]
                                        ),
                                    ],
                                ),

                            ],
                        ),
                    ]
                ),
            ],
        )
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
