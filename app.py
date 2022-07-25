from sys import implementation
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
from utility.form_group import formGroup
from datetime import datetime as dt
import skrf as rf
from skrf.time import detect_span
from utility.utils import callback_fuc
external_stylesheets = [
    # dbc.themes.BOOTSTRAP,
    # #"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
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
                                "太陽光電發電系統"
                            ],
                        ),
                        formGroup,
                    ]
                ),
            ],
        )
    ],
)


# @app.callback(
#     Output(component_id="case_name_row_output", component_property='children'),
#     Input(component_id="case_name_row", component_property='value')
#     )
# def update_output_div_case_name_row(input_value):
#     return (input_value)

@app.callback(
    Output('area_output', 'children'),
    Input('area', 'value')
)
def regional_bonus(value):
    return callback_fuc.regional_bonus(value)


# table result

@app.callback(
    Output('customer_discount_program_percent_output', 'children'),
    Input('customer_offers', 'value')
)
def customer_discount_program_percent(customer_offers):
    return callback_fuc.customer_discount_program_percent(customer_offers)


@app.callback(
    Output('actual_expenses_percent_output', 'children'),
    [Input('program_type', 'value'), Input('bank_loan_ratio', 'value')]
)
def actual_expenses_percent(program_type, bank_loan_ratio):
    return callback_fuc.actual_expenses_percent(program_type, bank_loan_ratio)



@app.callback(
    Output('bank_loan_percent_output', 'children'),
    [Input('program_type', 'value'), Input('bank_loan_ratio', 'value')]
)
def bank_loan_percent(program_type, bank_loan_ratio):
    return callback_fuc.bank_loan_percent(program_type, bank_loan_ratio)


@app.callback(
    Output('tax_free_construction_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value')]
)
def tax_free_construction_costs(construction, other):
    return callback_fuc.tax_free_construction_costs(construction, other)


# modal_table

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# app.callback(
#     Output("modal_project_costs", "is_open"),
#     [Input("open_project_costs", "n_clicks"),
#      Input("close_project_costs", "n_clicks")],
#     [State("modal_project_costs", "is_open")],
# )(toggle_modal)

app.callback(
    Output("modal_customer_offers", "is_open"),
    [Input("open_customer_offers", "n_clicks"),
     Input("close_customer_offers", "n_clicks")],
    [State("modal_customer_offers", "is_open")],
)(toggle_modal)

app.callback(
    Output("modal_warranty_cost", "is_open"),
    [Input("open_warranty_cost", "n_clicks"),
     Input("close_warranty_cost", "n_clicks")],
    [State("modal_warranty_cost", "is_open")],
)(toggle_modal)


if __name__ == "__main__":
    app.run_server(debug=True)
