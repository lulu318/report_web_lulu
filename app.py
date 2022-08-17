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


def bank_loan_percent(program_type, bank_loan_ratio):
    return callback_fuc.bank_loan_percent(program_type, bank_loan_ratio)


app.callback(
    Output('bank_loan_percent_output', 'children'),
    [Input('program_type', 'value'), Input('bank_loan_ratio', 'value')]
)(bank_loan_percent)
app.callback(
    Output('bank_loan_fee_percent_output', 'children'),
    [Input('program_type', 'value'), Input('bank_loan_ratio', 'value')]
)(bank_loan_percent)


@app.callback(
    Output('loan_annual_interest_rate_percent_output', 'children'),
    [Input('program_type', 'value'), Input('bank_loan_rate', 'value')]
)
def loan_annual_interest_rate_percent(program_type, bank_loan_rate):
    return callback_fuc.loan_annual_interest_rate_percent(program_type, bank_loan_rate)


@app.callback(
    Output('loan_term_percent_output', 'children'),
    [Input('bank_loan_term', 'value'), Input(
        'program_type', 'value'), Input('bank_loan_ratio', 'value')]
)
def loan_term_percent(bank_loan_term, program_type, bank_loan_ratio):
    return callback_fuc.loan_term_percent(bank_loan_term, program_type, bank_loan_ratio)


@app.callback(
    Output('loan_fee_percent_output', 'children'),
    Input('program_type', 'value'))
def loan_fee_percent(program_type):
    return callback_fuc.loan_fee_percent(program_type)


@app.callback(
    Output('pay_after_loan_percent_output', 'children'),
    [Input('customer_offers', 'value'), Input('bank_loan_ratio', 'value'), Input('program_type', 'value')])
def pay_after_loan_percent(customer_offers, bank_loan_ratio, program_type):
    return callback_fuc.pay_after_loan_percent(customer_offers, bank_loan_ratio, program_type)


@app.callback(
    Output('tax_free_construction_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value')]
)
def tax_free_construction_costs(construction_cost, other_costs):
    return callback_fuc.tax_free_construction_costs(construction_cost, other_costs)


@app.callback(
    Output('bank_loan_fee_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value')]
)
def bank_loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio):
    return callback_fuc.bank_loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio)


@app.callback(
    Output('actual_expenses_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value')]
)
def actual_expenses_costs(construction_cost, other_costs, program_type, bank_loan_ratio):
    return callback_fuc.actual_expenses_costs(construction_cost, other_costs, program_type, bank_loan_ratio)


@app.callback(
    Output('total_project_costs_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value')])
def total_project_costs(system_capacity, construction_cost, other_costs):
    return callback_fuc.total_project_costs(system_capacity, construction_cost, other_costs)


@app.callback(
    Output('actual_total_expenses_costs_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value')])
def actual_total_expenses_costs(system_capacity, construction, other, program_type, bank_loan_ratio):
    return callback_fuc.actual_total_expenses_costs(system_capacity, construction, other, program_type, bank_loan_ratio)


@app.callback(
    Output('customer_discount_program_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value'), Input('customer_offers', 'value')])
def customer_discount_program_costs(construction_cost, other_costs, system_capacity, customer_offers):
    return callback_fuc.customer_discount_program_costs(construction_cost, other_costs, system_capacity, customer_offers)


@app.callback(
    Output('bank_loan_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input('system_capacity', 'value')])
def bank_loan_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity):
    return callback_fuc.bank_loan_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity)


@app.callback(
    Output('annual_loan_repayment_amount_costs_output', 'children'),
    [Input('program_type', 'value'), Input('bank_loan_rate', 'value'), Input('bank_loan_term', 'value'), Input('bank_loan_ratio', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def annual_loan_repayment_amount_costs(program_type, bank_loan_rate, bank_loan_term, bank_loan_ratio, construction_cost, other_costs, system_capacity):
    return callback_fuc.annual_loan_repayment_amount_costs(program_type, bank_loan_rate, bank_loan_term, bank_loan_ratio, construction_cost, other_costs, system_capacity)


@app.callback(
    Output('taipower_line_subsidy_costs_output', 'children'),
    [Input('shape', 'value'), Input('strengthen_power_grid', 'value'), Input('system_capacity', 'value'), Input('roof_type_parallel_connection_method', 'value'), Input('installed_kw', 'value')])
def taipower_line_subsidy_costs(shape, strengthen_power_grid, system_capacity, roof_type_parallel_connection_method, installed_kw):
    return callback_fuc.taipower_line_subsidy_costs(shape, strengthen_power_grid, system_capacity, roof_type_parallel_connection_method, installed_kw)


@app.callback(
    Output('loan_fee_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input('system_capacity', 'value')])
def loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity):
    return callback_fuc.loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity)


@app.callback(
    Output('pay_after_loan_costs_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('shape', 'value'), Input('strengthen_power_grid', 'value'), Input('roof_type_parallel_connection_method', 'value'), Input('installed_kw', 'value'), Input('customer_offers', 'value'), Input('development_costs', 'value')])
def pay_after_loan_costs(system_capacity, construction_cost, other_costs, program_type, bank_loan_ratio, shape, strengthen_power_grid,  roof_type_parallel_connection_method, installed_kw, customer_offers, development_costs):
    return callback_fuc.pay_after_loan_costs(system_capacity, construction_cost, other_costs, program_type, bank_loan_ratio, shape, strengthen_power_grid,  roof_type_parallel_connection_method, installed_kw, customer_offers, development_costs)

# customer_offers


@app.callback(
    Output('customer_offers_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value'), Input('customer_offers', 'value')])
def customer_offers_costs(construction_cost, other_costs, system_capacity, customer_offers):
    return callback_fuc.customer_offers_costs(construction_cost, other_costs, system_capacity, customer_offers)

# warranty_cost_df


@app.callback(
    Output('illustrate_7years_output', 'children'), Input('warranty_annual_increment_rate', 'value'))
def illustrate_7years(warranty_annual_increment_rate):
    return callback_fuc.illustrate_7years(warranty_annual_increment_rate)


@app.callback(
    Output('illustrate_20years_output', 'children'), Input('warranty_annual_increment_rate', 'value'))
def illustrate_20years(warranty_annual_increment_rate):
    return callback_fuc.illustrate_20years(warranty_annual_increment_rate)


@app.callback(
    Output('scale_7years_output', 'children'), Input('warranty_annual_increment_rate', 'value'))
def scale_7years(warranty_annual_increment_rate):
    return callback_fuc.scale_7years(warranty_annual_increment_rate)


@app.callback(
    Output('scale_20years_output', 'children'), Input('warranty_annual_increment_rate', 'value'))
def scale_20years(warranty_annual_increment_rate):
    return callback_fuc.scale_20years(warranty_annual_increment_rate)


# @app.callback(
#     Output('amount_6years_output', 'children'), Input('none', 'value'))
# def amount_6years():
#     return callback_fuc.amount_6years()


# @app.callback(
#     Output('amount_7years_output', 'children'), Input('none', 'value'))
# def amount_7years():
#     return callback_fuc.amount_7years()


# @app.callback(
#     Output('amount_20years_output', 'children'), Input('none', 'value'))
# def amount_20years():
#     return callback_fuc.amount_20years()


# @app.callback(
#     Output('amount_total_output', 'children'), Input('none', 'value'))
# def amount_total():
#     return callback_fuc.amount_total()


# operating_expense
@app.callback(
    Output('scale_module_recycling_fund_output', 'children'), Input('module_recycling_fund', 'value'))
def scale_module_recycling_fund(module_recycling_fund):
    return callback_fuc.scale_module_recycling_fund(module_recycling_fund)


@app.callback(
    Output('scale_removal_fee_output', 'children'), Input('demolition_cost', 'value'))
def scale_removal_fee(demolition_cost):
    return callback_fuc.scale_removal_fee(demolition_cost)


@app.callback(
    Output('amount_cleaning_fee_water_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value')])
def amount_cleaning_fee_water(system_capacity, construction_cost, other_costs):
    return callback_fuc.amount_cleaning_fee_water(system_capacity, construction_cost, other_costs)


@app.callback(
    Output('amount_property_insurance_costs_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value')])
def amount_property_insurance_costs(system_capacity, construction_cost, other_costs):
    return callback_fuc.amount_property_insurance_costs(system_capacity, construction_cost, other_costs)


@app.callback(
    Output('amount_module_recycling_fund_output', 'children'),
    [Input('module_recycling_fund', 'value'), Input('system_capacity', 'value')])
def amount_module_recycling_fund(module_recycling_fund, system_capacity):
    return callback_fuc.amount_module_recycling_fund(module_recycling_fund, system_capacity)


@app.callback(
    Output('amount_removal_fee_output', 'children'),
    [Input('system_capacity', 'value'), Input('demolition_cost', 'value')])
def amount_removal_fee(system_capacity, demolition_cost):
    return callback_fuc.amount_removal_fee(system_capacity, demolition_cost)

# return_on_investment_df

@app.callback(
    Output('ese_1_output', 'children'),
    Input('estimated_first_year_system', 'value'))
def ese_1(estimated_first_year_system):
    return callback_fuc.ese_1(estimated_first_year_system)
@app.callback(
    Output('ese_2_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(2, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_3_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(3, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_4_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(4, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_5_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(5, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_6_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(6, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_7_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(7, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_8_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(8, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_9_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(9, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_10_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(10, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_11_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(11, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_12_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(12, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_13_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(13, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_14_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(14, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_15_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(15, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_16_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(16, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_17_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(17, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_18_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(18, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_19_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(19, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('ese_20_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.estimated_system_efficiency(20, estimated_first_year_system, pr_annual_decline_rate)


@app.callback(
    Output('eis_1_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(1, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_2_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(2, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_3_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(3, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_4_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(4, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_5_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(5, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_6_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(6, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_7_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(7, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_8_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(8, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_9_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(9, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_10_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(10, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_11_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(11, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_12_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(12, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_13_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(13, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_14_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(14, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_15_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(15, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_16_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(16, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_17_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(17, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_18_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(18, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_19_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(19, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)
@app.callback(
    Output('eis_20_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return callback_fuc.electricity_income_statement(20, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)












# @app.callback(
#     Output('annual_wholesale_rate_output', 'children'),
#     Input('annual_wholesale_rate_year', 'value'))
# def testttt(annual_wholesale_rate_year):
#     return f'Output: {annual_wholesale_rate_year}'

# @app.callback(
#     Output('shape_output', 'children'),
#     Input('shape', 'value'))
# def testttt(shape):
#     if shape == '屋頂型':
#         res = "aa"
#     return res


# modal_table

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


app.callback(
    Output("modal_project_costs", "is_open"),
    [Input("open_project_costs", "n_clicks"),
     Input("close_project_costs", "n_clicks")],
    [State("modal_project_costs", "is_open")],
)(toggle_modal)

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

app.callback(
    Output("modal_operating_expense", "is_open"),
    [Input("open_operating_expense", "n_clicks"),
     Input("close_operating_expense", "n_clicks")],
    [State("modal_operating_expense", "is_open")],
)(toggle_modal)

app.callback(
    Output("modal_wholesale_rate", "is_open"),
    [Input("open_wholesale_rate", "n_clicks"),
     Input("close_wholesale_rate", "n_clicks")],
    [State("modal_wholesale_rate", "is_open")],
)(toggle_modal)

app.callback(
    Output("modal_return_on_investment", "is_open"),
    [Input("open_return_on_investment", "n_clicks"),
     Input("close_return_on_investment", "n_clicks")],
    [State("modal_return_on_investment", "is_open")],
)(toggle_modal)


if __name__ == "__main__":
    app.run_server(debug=True)
