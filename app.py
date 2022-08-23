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
from utility.utils import callback_fuc, feature_fuc

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
    return feature_fuc.to_currency_format(callback_fuc.regional_bonus(value))


# table result

@app.callback(
    Output('customer_discount_program_percent_output', 'children'),
    Input('customer_offers', 'value')
)
def customer_discount_program_percent(customer_offers):
    return feature_fuc.to_currency_format(callback_fuc.customer_discount_program_percent(customer_offers))


@app.callback(
    Output('actual_expenses_percent_output', 'children'),
    [Input('program_type', 'value'), Input('bank_loan_ratio', 'value')]
)
def actual_expenses_percent(program_type, bank_loan_ratio):
    return feature_fuc.to_currency_format(callback_fuc.actual_expenses_percent(program_type, bank_loan_ratio))


def bank_loan_percent(program_type, bank_loan_ratio):
    return feature_fuc.to_currency_format(callback_fuc.bank_loan_percent(program_type, bank_loan_ratio))


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
    return feature_fuc.to_currency_format(callback_fuc.loan_annual_interest_rate_percent(program_type, bank_loan_rate))


@app.callback(
    Output('loan_term_percent_output', 'children'),
    [Input('bank_loan_term', 'value'), Input(
        'program_type', 'value'), Input('bank_loan_ratio', 'value')]
)
def loan_term_percent(bank_loan_term, program_type, bank_loan_ratio):
    return feature_fuc.to_currency_format(callback_fuc.loan_term_percent(bank_loan_term, program_type, bank_loan_ratio))


@app.callback(
    Output('loan_fee_percent_output', 'children'),
    Input('program_type', 'value'))
def loan_fee_percent(program_type):
    return feature_fuc.to_currency_format(callback_fuc.loan_fee_percent(program_type))


@app.callback(
    Output('pay_after_loan_percent_output', 'children'),
    [Input('customer_offers', 'value'), Input('bank_loan_ratio', 'value'), Input('program_type', 'value')])
def pay_after_loan_percent(customer_offers, bank_loan_ratio, program_type):
    return feature_fuc.to_currency_format(callback_fuc.pay_after_loan_percent(customer_offers, bank_loan_ratio, program_type))


@app.callback(
    Output('tax_free_construction_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value')]
)
def tax_free_construction_costs(construction_cost, other_costs):
    return feature_fuc.to_currency_format(callback_fuc.tax_free_construction_costs(construction_cost, other_costs), num=0)


@app.callback(
    Output('bank_loan_fee_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value')]
)
def bank_loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio):
    return feature_fuc.to_currency_format(callback_fuc.bank_loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio), num=0)


@app.callback(
    Output('actual_expenses_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value')]
)
def actual_expenses_costs(construction_cost, other_costs, program_type, bank_loan_ratio):
    return feature_fuc.to_currency_format(callback_fuc.actual_expenses_costs(construction_cost, other_costs, program_type, bank_loan_ratio), num=0)


@app.callback(
    Output('total_project_costs_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value')])
def total_project_costs(system_capacity, construction_cost, other_costs):
    return feature_fuc.to_currency_format(callback_fuc.total_project_costs(system_capacity, construction_cost, other_costs), num=0)


@app.callback(
    Output('actual_total_expenses_costs_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value')])
def actual_total_expenses_costs(system_capacity, construction, other, program_type, bank_loan_ratio):
    return feature_fuc.to_currency_format(callback_fuc.actual_total_expenses_costs(system_capacity, construction, other, program_type, bank_loan_ratio), num=0)


@app.callback(
    Output('customer_discount_program_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value'), Input('customer_offers', 'value')])
def customer_discount_program_costs(construction_cost, other_costs, system_capacity, customer_offers):
    return feature_fuc.to_currency_format(callback_fuc.customer_discount_program_costs(construction_cost, other_costs, system_capacity, customer_offers), num=0)


@app.callback(
    Output('bank_loan_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input('system_capacity', 'value')])
def bank_loan_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.bank_loan_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity), num=0)


@app.callback(
    Output('annual_loan_repayment_amount_costs_output', 'children'),
    [Input('program_type', 'value'), Input('bank_loan_rate', 'value'), Input('bank_loan_term', 'value'), Input('bank_loan_ratio', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def annual_loan_repayment_amount_costs(program_type, bank_loan_rate, bank_loan_term, bank_loan_ratio, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.annual_loan_repayment_amount_costs(program_type, bank_loan_rate, bank_loan_term, bank_loan_ratio, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('taipower_line_subsidy_costs_output', 'children'),
    [Input('shape', 'value'), Input('strengthen_power_grid', 'value'), Input('system_capacity', 'value'), Input('roof_type_parallel_connection_method', 'value'), Input('installed_kw', 'value')])
def taipower_line_subsidy_costs(shape, strengthen_power_grid, system_capacity, roof_type_parallel_connection_method, installed_kw):
    return feature_fuc.to_currency_format(callback_fuc.taipower_line_subsidy_costs(shape, strengthen_power_grid, system_capacity, roof_type_parallel_connection_method, installed_kw), num=0)


@app.callback(
    Output('loan_fee_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input('system_capacity', 'value')])
def loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity), num=0)


@app.callback(
    Output('pay_after_loan_costs_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('shape', 'value'), Input('strengthen_power_grid', 'value'), Input('roof_type_parallel_connection_method', 'value'), Input('installed_kw', 'value'), Input('customer_offers', 'value'), Input('development_costs', 'value')])
def pay_after_loan_costs(system_capacity, construction_cost, other_costs, program_type, bank_loan_ratio, shape, strengthen_power_grid,  roof_type_parallel_connection_method, installed_kw, customer_offers, development_costs):
    return feature_fuc.to_currency_format(callback_fuc.pay_after_loan_costs(system_capacity, construction_cost, other_costs, program_type, bank_loan_ratio, shape, strengthen_power_grid,  roof_type_parallel_connection_method, installed_kw, customer_offers, development_costs), num=0)

# customer_offers


@app.callback(
    Output('customer_offers_costs_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value'), Input('customer_offers', 'value')])
def customer_offers_costs(construction_cost, other_costs, system_capacity, customer_offers):
    return feature_fuc.to_currency_format(callback_fuc.customer_offers_costs(construction_cost, other_costs, system_capacity, customer_offers), num=0)

# warranty_cost_df


@app.callback(
    Output('illustrate_7years_output', 'children'), Input('warranty_annual_increment_rate', 'value'))
def illustrate_7years(warranty_annual_increment_rate):
    return f"售電收入{callback_fuc.illustrate_7years(warranty_annual_increment_rate)} % "


@app.callback(
    Output('illustrate_20years_output', 'children'), Input('warranty_annual_increment_rate', 'value'))
def illustrate_20years(warranty_annual_increment_rate):
    return f"售電收入{callback_fuc.illustrate_20years(warranty_annual_increment_rate)} % "


@app.callback(
    Output('scale_7years_output', 'children'), Input('warranty_annual_increment_rate', 'value'))
def scale_7years(warranty_annual_increment_rate):
    return f" {callback_fuc.scale_7years(warranty_annual_increment_rate)} % "


@app.callback(
    Output('scale_20years_output', 'children'), Input('warranty_annual_increment_rate', 'value'))
def scale_20years(warranty_annual_increment_rate):
    return f" {callback_fuc.scale_20years(warranty_annual_increment_rate)} % "


@app.callback(
    Output('amount_6years_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def amount_6years(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                  system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                  strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                  estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.amount_6years(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                      system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                      strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                      estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('amount_7years_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def amount_7years(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                  system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                  strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                  estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.amount_7years(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                      system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                      strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                      estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('amount_20years_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def amount_20years(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                   system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                   strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                   estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.amount_20years(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                       system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                       strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                       estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('amount_total_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input(
         'roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee_basic(construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                       strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                       estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.amount_total(construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.amount_cleaning_fee_water(system_capacity, construction_cost, other_costs), num=0)


@app.callback(
    Output('amount_property_insurance_costs_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value')])
def amount_property_insurance_costs(system_capacity, construction_cost, other_costs):
    return feature_fuc.to_currency_format(callback_fuc.amount_property_insurance_costs(system_capacity, construction_cost, other_costs), num=0)


@app.callback(
    Output('amount_module_recycling_fund_output', 'children'),
    [Input('module_recycling_fund', 'value'), Input('system_capacity', 'value')])
def amount_module_recycling_fund(module_recycling_fund, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.amount_module_recycling_fund(module_recycling_fund, system_capacity), num=0)


@app.callback(
    Output('amount_removal_fee_output', 'children'),
    [Input('system_capacity', 'value'), Input('demolition_cost', 'value')])
def amount_removal_fee(system_capacity, demolition_cost):
    return feature_fuc.to_currency_format(callback_fuc.amount_removal_fee(system_capacity, demolition_cost), num=0)


@app.callback(
    Output('scale_installation_space_cost_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def scale_installation_space_cost(annual_rent_money, annual_rent, construction_cost, other_costs, system_capacity, customer_offers,
                                  program_type, bank_loan_ratio, shape, roof_type_grid_connection_engineering,
                                  module_recycling_fund, installed_kw, annual_wholesale_rate_year, annual_wholesale_rate_period,
                                  area, strengthen_power_grid, high_efficiency_bonus, fishing_environment,
                                  agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return f"""{callback_fuc.scale_installation_space_cost(annual_rent_money, annual_rent, construction_cost, other_costs, system_capacity, customer_offers,
                                                      program_type, bank_loan_ratio, shape, roof_type_grid_connection_engineering,
                                                      module_recycling_fund, installed_kw, annual_wholesale_rate_year, annual_wholesale_rate_period,
                                                      area, strengthen_power_grid, high_efficiency_bonus, fishing_environment,
                                                      agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate)} %"""


@app.callback(
    Output('amount_installation_space_cost_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def amount_installation_space_cost(annual_rent_money, annual_rent, system_capacity, construction_cost, other_costs, customer_offers,
                                   program_type, bank_loan_ratio, shape, roof_type_grid_connection_engineering,
                                   module_recycling_fund, installed_kw, annual_wholesale_rate_year, annual_wholesale_rate_period,
                                   area, strengthen_power_grid, high_efficiency_bonus, fishing_environment,
                                   agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system,
                                   pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.amount_installation_space_cost(annual_rent_money, annual_rent, system_capacity, construction_cost, other_costs, customer_offers,
                                                       program_type, bank_loan_ratio, shape, roof_type_grid_connection_engineering,
                                                       module_recycling_fund, installed_kw, annual_wholesale_rate_year, annual_wholesale_rate_period,
                                                       area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                                       estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('amount_operating_expense_total_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def amount_operating_expense_total(annual_rent_money, annual_rent, system_capacity, construction_cost,
                                   other_costs, customer_offers, program_type, bank_loan_ratio,
                                   shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                   annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                   high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                   estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.amount_operating_expense_total(annual_rent_money, annual_rent, system_capacity, construction_cost,
                                                       other_costs, customer_offers, program_type, bank_loan_ratio,
                                                       shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                                       estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system,
                                                       pr_annual_decline_rate), num=0)

# return_on_investment_df


@app.callback(
    Output('ese_1_output', 'children'),
    Input('estimated_first_year_system', 'value'))
def ese_1(estimated_first_year_system):
    return feature_fuc.to_currency_format(callback_fuc.ese_1(estimated_first_year_system), num=0)


@app.callback(
    Output('ese_2_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(2, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_3_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(3, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_4_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(4, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_5_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(5, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_6_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(6, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_7_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(7, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_8_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(8, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_9_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(9, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_10_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(10, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_11_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(11, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_12_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(12, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_13_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(13, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_14_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(14, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_15_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(15, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_16_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(16, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_17_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(17, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_18_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(18, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_19_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(19, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_20_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency(20, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_sum_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency_basic(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency_basic("sum", estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('ese_average_output', 'children'),
    [Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def estimated_system_efficiency_basic(estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.estimated_system_efficiency_basic("average", estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(1, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(2, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(3, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(4, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(5, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(6, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(7, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(8, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(9, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(10, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(11, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(12, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(13, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(14, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(15, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(16, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(17, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(18, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(19, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


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
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement(20, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('eis_sum_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement_basic(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                       system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                       strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                       estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement_basic("sum", shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('eis_average_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def electricity_income_statement_basic(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                       system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                       strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                       estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.electricity_income_statement_basic("average", shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('lds_1_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(1, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_2_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(2, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_3_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(3, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_4_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(4, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_5_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(5, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_6_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(6, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_7_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(7, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_8_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(8, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_9_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(9, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_10_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(10, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_11_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(11, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_12_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(12, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_13_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(13, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_14_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(14, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_15_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(15, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_16_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(16, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_17_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(17, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_18_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(18, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_19_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(19, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_20_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement(20, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


@app.callback(
    Output('lds_sum_output', 'children'),
    [Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('system_capacity', 'value')])
def loan_disbursement_statement(repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                bank_loan_rate, construction_cost, other_costs, system_capacity):
    return feature_fuc.to_currency_format(callback_fuc.loan_disbursement_statement_basic("sum", repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, system_capacity), num=0)


def customer_discount_program(construction_cost, other_costs, system_capacity, customer_offers):
    return feature_fuc.to_currency_format(callback_fuc.customer_discount_program(construction_cost, other_costs, system_capacity, customer_offers), num=0)


app.callback(
    Output('cdp_1_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(customer_discount_program)
app.callback(
    Output('cdp_2_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(customer_discount_program)
app.callback(
    Output('cdp_3_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(customer_discount_program)
app.callback(
    Output('cdp_4_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(customer_discount_program)
app.callback(
    Output('cdp_5_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(customer_discount_program)


@app.callback(
    Output('cdp_sum_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)
def customer_discount_program(construction_cost, other_costs, system_capacity, customer_offers):
    return feature_fuc.to_currency_format(callback_fuc.customer_discount_program_basic("sum", construction_cost, other_costs, system_capacity, customer_offers), num=0)


def warranty_fee_before_5(construction_cost, other_costs, system_capacity, customer_offers):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee_before_5(construction_cost, other_costs, system_capacity, customer_offers), num=0)


app.callback(
    Output('warranty_1_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(warranty_fee_before_5)
app.callback(
    Output('warranty_2_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(warranty_fee_before_5)
app.callback(
    Output('warranty_3_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(warranty_fee_before_5)
app.callback(
    Output('warranty_4_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(warranty_fee_before_5)
app.callback(
    Output('warranty_5_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input(
        'system_capacity', 'value'), Input('customer_offers', 'value')]
)(warranty_fee_before_5)


@app.callback(
    Output('warranty_6_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(6, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_7_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(7, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_8_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(8, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_9_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(9, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_10_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(10, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_11_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(11, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_12_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(12, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_13_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(13, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_14_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(14, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_15_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(15, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_16_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(16, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_17_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(17, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_18_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(18, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_19_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(19, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_20_output', 'children'),
    [Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee(warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                 system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                 strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                 estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee(20, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('warranty_sum_output', 'children'),
    [Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('shape', 'value'), Input(
         'roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def warranty_fee_basic(construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                       strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                       estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.warranty_fee_basic("sum", construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                           strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                           estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_1_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(1, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_2_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(2, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_3_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(3, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_4_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(4, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_5_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(5, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_6_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(6, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_7_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(7, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_8_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(8, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_9_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(9, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_10_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(10, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_11_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(11, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_12_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(12, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_13_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(13, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_14_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(14, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_15_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(15, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_16_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(16, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_17_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(17, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_18_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(18, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_19_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(19, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_20_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses(annual_rent_money, annual_rent, development_costs,
                       demolition_cost, system_capacity, whether_to_remove, construction_cost,
                       other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                       roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                       annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                       high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                       estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses(20, annual_rent_money, annual_rent, development_costs,
                                           demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                           other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                           roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                           annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                           estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


@app.callback(
    Output('oe_sum_output', 'children'),
    [Input('annual_rent_money', 'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'), Input('demolition_cost', 'value'),
     Input('system_capacity', 'value'), Input('whether_to_remove', 'value'), Input(
         'construction_cost', 'value'), Input('other_costs', 'value'), Input('customer_offers', 'value'),
     Input('program_type', 'value'), Input('bank_loan_ratio', 'value'), Input(
         'shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'),
     Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'), Input(
         'annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'),
     Input('area', 'value'), Input('strengthen_power_grid', 'value'), Input(
         'high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'),
     Input('agriculture_fishing_green_energy', 'value'), Input(
         'estimated_rate_reduction_next_year', 'value'),
     Input('estimated_sunshine', 'value'), Input('estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value')])
def operating_expenses_basic(annual_rent_money, annual_rent, development_costs,
                             demolition_cost, system_capacity, whether_to_remove, construction_cost,
                             other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                             roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                             annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                             high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                             estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
    return feature_fuc.to_currency_format(callback_fuc.operating_expenses_basic("sum", annual_rent_money, annual_rent, development_costs,
                                                 demolition_cost, system_capacity, whether_to_remove, construction_cost,
                                                 other_costs, customer_offers, program_type, bank_loan_ratio, shape,
                                                 roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                                 annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                 high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year,
                                                 estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate), num=0)


def total_cash_flow_0(system_capacity, construction_cost, other_costs, program_type, bank_loan_ratio, shape, strengthen_power_grid,  roof_type_parallel_connection_method, installed_kw, customer_offers, development_costs):
    return feature_fuc.to_currency_format(callback_fuc.total_cash_flow_0(system_capacity, construction_cost, other_costs, program_type, bank_loan_ratio, shape, strengthen_power_grid,  roof_type_parallel_connection_method, installed_kw, customer_offers, development_costs), num=0)


app.callback(
    Output('total_r_0_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('shape', 'value'), Input('strengthen_power_grid', 'value'), Input('roof_type_parallel_connection_method', 'value'), Input('installed_kw', 'value'), Input('customer_offers', 'value'), Input('development_costs', 'value')])(total_cash_flow_0)
app.callback(
    Output('cash_flow_0_output', 'children'),
    [Input('system_capacity', 'value'), Input('construction_cost', 'value'), Input('other_costs', 'value'), Input('program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('shape', 'value'), Input('strengthen_power_grid', 'value'), Input('roof_type_parallel_connection_method', 'value'), Input('installed_kw', 'value'), Input('customer_offers', 'value'), Input('development_costs', 'value')])(total_cash_flow_0)


@app.callback(
    Output('total_r_1_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(1, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)

@app.callback(
    Output('total_r_2_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(2, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_3_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(3, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_4_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(4, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_5_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(5, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_6_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(6, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_7_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(7, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_8_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(8, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_9_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(9, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_10_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(10, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_11_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(11, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_12_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(12, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_13_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(13, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_14_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(14, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_15_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(15, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_16_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(16, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_17_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(17, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_18_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(18, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_19_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(19, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_20_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_r(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
            system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
            estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
            repayment_type, bank_loan_term, program_type, bank_loan_ratio,
            bank_loan_rate, construction_cost, other_costs, customer_offers,
            warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
            demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_r(20, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('total_r_sum_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value')])
def total_return_on_investment_basic(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
                                     system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
                                     strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
                                     estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
                                     repayment_type, bank_loan_term, program_type, bank_loan_ratio,
                                     bank_loan_rate, construction_cost, other_costs, customer_offers,
                                     warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
                                     demolition_cost, whether_to_remove):
    return feature_fuc.to_currency_format(callback_fuc.total_return_on_investment_basic("sum", shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove), num=0)


@app.callback(
    Output('cash_flow_1_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(1, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_2_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(2, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_3_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(3, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_4_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(4, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_5_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(5, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_6_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(6, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_7_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(7, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_8_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(8, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_9_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(9, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_10_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(10, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_11_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(11, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_12_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(12, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_13_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(13, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_14_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(14, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_15_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(15, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_16_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(16, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_17_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(17, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_18_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(18, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_19_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(19, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)


@app.callback(
    Output('cash_flow_20_output', 'children'),
    [Input('shape', 'value'), Input('roof_type_grid_connection_engineering', 'value'), Input('module_recycling_fund', 'value'), Input('installed_kw', 'value'),
     Input('system_capacity', 'value'), Input('annual_wholesale_rate_year', 'value'), Input(
         'annual_wholesale_rate_period', 'value'), Input('area', 'value'),
     Input('strengthen_power_grid', 'value'), Input('high_efficiency_bonus', 'value'), Input(
         'fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'),
     Input('estimated_rate_reduction_next_year', 'value'), Input('estimated_sunshine', 'value'), Input(
         'estimated_first_year_system', 'value'), Input('pr_annual_decline_rate', 'value'),
     Input('repayment_type', 'value'), Input('bank_loan_term', 'value'), Input(
         'program_type', 'value'), Input('bank_loan_ratio', 'value'),
     Input('bank_loan_rate', 'value'), Input('construction_cost', 'value'), Input(
         'other_costs', 'value'), Input('customer_offers', 'value'),
     Input('warranty_annual_increment_rate', 'value'), Input('annual_rent_money',
                                                             'value'), Input('annual_rent', 'value'), Input('development_costs', 'value'),
     Input('demolition_cost', 'value'), Input('whether_to_remove', 'value'), Input('roof_type_parallel_connection_method', 'value')])
def cash_flow(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw,
              system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area,
              strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy,
              estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate,
              repayment_type, bank_loan_term, program_type, bank_loan_ratio,
              bank_loan_rate, construction_cost, other_costs, customer_offers,
              warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs,
              demolition_cost, whether_to_remove, roof_type_parallel_connection_method):
    return feature_fuc.to_currency_format(callback_fuc.cash_flow(20, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate, repayment_type, bank_loan_term, program_type, bank_loan_ratio, bank_loan_rate, construction_cost, other_costs, customer_offers, warranty_annual_increment_rate, annual_rent_money, annual_rent, development_costs, demolition_cost, whether_to_remove, roof_type_parallel_connection_method), num=0)

# wholesale_rate_df


@app.callback(
    Output('fit_1_output', 'children'),
    [Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value')])
def fit_1(annual_wholesale_rate_year, annual_wholesale_rate_period):
    return callback_fuc.fit_1(annual_wholesale_rate_year, annual_wholesale_rate_period)


@app.callback(
    Output('fit_2_output', 'children'),
    [Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value')])
def fit_1(annual_wholesale_rate_year, annual_wholesale_rate_period):
    return callback_fuc.fit_2(annual_wholesale_rate_year, annual_wholesale_rate_period)


@app.callback(
    Output('fit_3_output', 'children'),
    [Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value')])
def fit_1(annual_wholesale_rate_year, annual_wholesale_rate_period):
    return callback_fuc.fit_3(annual_wholesale_rate_year, annual_wholesale_rate_period)


@app.callback(
    Output('fit_4_output', 'children'),
    [Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value')])
def fit_1(annual_wholesale_rate_year, annual_wholesale_rate_period):
    return callback_fuc.fit_4(annual_wholesale_rate_year, annual_wholesale_rate_period)


@app.callback(
    Output('fit_5_output', 'children'),
    [Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value')])
def fit_1(annual_wholesale_rate_year, annual_wholesale_rate_period):
    return callback_fuc.fit_5(annual_wholesale_rate_year, annual_wholesale_rate_period)


@app.callback(
    Output('fit_6_output', 'children'),
    [Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value')])
def fit_1(annual_wholesale_rate_year, annual_wholesale_rate_period):
    return callback_fuc.fit_6(annual_wholesale_rate_year, annual_wholesale_rate_period)


def addition(area):
    return f"{callback_fuc.addition(area)} % "


app.callback(
    Output('addition_1_output', 'children'), Input('area', 'value'))(addition)
app.callback(
    Output('addition_2_output', 'children'), Input('area', 'value'))(addition)
app.callback(
    Output('addition_3_output', 'children'), Input('area', 'value'))(addition)
app.callback(
    Output('addition_4_output', 'children'), Input('area', 'value'))(addition)
app.callback(
    Output('addition_5_output', 'children'), Input('area', 'value'))(addition)
app.callback(
    Output('addition_6_output', 'children'), Input('area', 'value'))(addition)


@app.callback(
    Output('plus_rate_total_1_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('strengthen_power_grid', 'value'),
     Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value')])
def plus_rate_total_output(roof_type_grid_connection_engineering, strengthen_power_grid,
                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy):
    return callback_fuc.plus_rate_total_output(1, roof_type_grid_connection_engineering, strengthen_power_grid,
                                               high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy)


@app.callback(
    Output('plus_rate_total_2_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('strengthen_power_grid', 'value'),
     Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value')])
def plus_rate_total_output(roof_type_grid_connection_engineering, strengthen_power_grid,
                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy):
    return callback_fuc.plus_rate_total_output(2, roof_type_grid_connection_engineering, strengthen_power_grid,
                                               high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy)


@app.callback(
    Output('plus_rate_total_3_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value')])
def plus_rate_total_output(roof_type_grid_connection_engineering, strengthen_power_grid,
                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy):
    return callback_fuc.plus_rate_total_output(3, roof_type_grid_connection_engineering, strengthen_power_grid,
                                               high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy)


@app.callback(
    Output('plus_rate_total_4_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value')])
def plus_rate_total_output(roof_type_grid_connection_engineering, strengthen_power_grid,
                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy):
    return callback_fuc.plus_rate_total_output(4, roof_type_grid_connection_engineering, strengthen_power_grid,
                                               high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy)


@app.callback(
    Output('plus_rate_total_5_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value')])
def plus_rate_total_output(roof_type_grid_connection_engineering, strengthen_power_grid,
                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy):
    return callback_fuc.plus_rate_total_output(5, roof_type_grid_connection_engineering, strengthen_power_grid,
                                               high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy)


@app.callback(
    Output('plus_rate_total_6_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value')])
def plus_rate_total_output(roof_type_grid_connection_engineering, strengthen_power_grid,
                           high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy):
    return callback_fuc.plus_rate_total_output(6, roof_type_grid_connection_engineering, strengthen_power_grid,
                                               high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy)

@app.callback(
    Output('electricity_sales_rate_1_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'), Input('area', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'), Input('estimated_rate_reduction_next_year', 'value')])
def electricity_sales_rate_output(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                  high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year):
    return callback_fuc.electricity_sales_rate_output(1, roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                      high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year)
@app.callback(
    Output('electricity_sales_rate_2_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'), Input('area', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'), Input('estimated_rate_reduction_next_year', 'value')])
def electricity_sales_rate_output(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                  high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year):
    return callback_fuc.electricity_sales_rate_output(2, roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                      high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year)
@app.callback(
    Output('electricity_sales_rate_3_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'), Input('area', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'), Input('estimated_rate_reduction_next_year', 'value')])
def electricity_sales_rate_output(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                  high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year):
    return callback_fuc.electricity_sales_rate_output(3, roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                      high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year)
@app.callback(
    Output('electricity_sales_rate_4_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'), Input('area', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'), Input('estimated_rate_reduction_next_year', 'value')])
def electricity_sales_rate_output(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                  high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year):
    return callback_fuc.electricity_sales_rate_output(4, roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                      high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year)
@app.callback(
    Output('electricity_sales_rate_5_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'), Input('area', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'), Input('estimated_rate_reduction_next_year', 'value')])
def electricity_sales_rate_output(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                  high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year):
    return callback_fuc.electricity_sales_rate_output(5, roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                      high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year)
@app.callback(
    Output('electricity_sales_rate_6_output', 'children'),
    [Input('roof_type_grid_connection_engineering', 'value'), Input('annual_wholesale_rate_year', 'value'), Input('annual_wholesale_rate_period', 'value'), Input('area', 'value'), Input('strengthen_power_grid', 'value'),
        Input('high_efficiency_bonus', 'value'), Input('fishing_environment', 'value'), Input('agriculture_fishing_green_energy', 'value'), Input('estimated_rate_reduction_next_year', 'value')])
def electricity_sales_rate_output(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                  high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year):
    return callback_fuc.electricity_sales_rate_output(6, roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                      high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year)



if __name__ == "__main__":
    app.run_server(debug=True)
