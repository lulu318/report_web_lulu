from cmath import nan
from html.entities import html5
import pandas as pd
from enum import auto
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import numpy_financial as npf
import datetime
import re

year_list = [i for i in range(111, int(datetime.datetime.today().year)-1911+3)]
_F29_ = 0.0656  # _F29~_F35, _J43~_J49
_G29_ = 0.0866  # _G29 ~ G35
_J29_ = 0.3471
_J30_ = 0.2672
_J31_ = 0.2632
_J32_ = 0.238
_J33_ = 0.2384
_J34_ = 0.2321
_J35_ = 0.2557
_I31_ = 0.0688
_I32_ = 0.0963
_I33_ = 0.0413
_L29_ = 0.0387  # _L29~ L35
_M29_ = 0.1934  # _M29~ M34
_H34_ = 0.1356  # H29~H35


class feature_fuc:
    def find_first_number(function_name):
        pattern_float = re.compile(r'[0-9]+\.[0-9]+')
        if pattern_float.findall(function_name)[0]:
            res = float(pattern_float.findall(function_name)[0])
        else:
            pattern = re.compile(r'\d')
            res = int(pattern.findall(function_name)[0])
        return res

    def result(value_id):
        res = html.H5(id=value_id)
        return res

    @staticmethod
    def judge_is_none(value):
        if value is None:
            value = 0
        if type(value) and pd.isnull(value):
            value = 0
        return value

    @staticmethod
    def radio_items(_id, _options: list):
        items = dbc.RadioItems(
            options=_options,
            value=2,
            id=_id,
            inline=True,
            labelCheckedClassName="text-success",
            inputCheckedClassName="border border-success bg-success",
        )
        return items

    @staticmethod
    def group_text(frame, text):
        text = dbc.InputGroup([frame, text])
        return text

    @staticmethod
    def input_frame(_id, _placeholder="Type something...", _type="number", **kwargs):
        frame = dbc.Input(id=_id, placeholder=_placeholder,
                          type=_type, **kwargs)
        return frame

    @staticmethod
    def label_name(label_text, _html_for, **kwargs):
        label = dbc.Label(label_text, html_for=_html_for, **kwargs)
        return label

    @staticmethod
    def dropdown_item(_id, items: list, color):
        dropdown = dcc.Dropdown(
            items, items[0], id=_id, style={
                "background": color,
            })
        return dropdown

    def table_dataframe(df):
        table = dbc.Table.from_dataframe(
            df,
            striped=True,
            bordered=True,
            hover=True,
        )
        return table


class form_func:
    @staticmethod
    def input_frame_label_name(label_text, _id, unit=None, _width=3, type_="number", _disabled=False):
        if unit:
            _group = feature_fuc.group_text(
                feature_fuc.input_frame(_id, _type=type_, disabled=_disabled),
                dbc.InputGroupText(unit)
            )
        else:
            _group = feature_fuc.input_frame(_id, _type=type_)
        col = dbc.Col(
            [
                feature_fuc.label_name(
                    label_text, _id),
                _group
            ],
            width=_width,
            className="mb-4",
        )
        return col

    @staticmethod
    def radio_items_label_name(label_text, _id, _options: list):
        col = dbc.Col(
            [
                feature_fuc.label_name(label_text, _id),
                feature_fuc.radio_items(_id, _options),
            ],
            width=3
        )
        return col

    @staticmethod
    def dropdown_items_label_name(_id, items: list, label_text, color):
        col = dbc.Col(
            [
                feature_fuc.label_name(label_text, _id),
                feature_fuc.dropdown_item(_id, items, color)

            ],
            width=3
        )
        return col

    @staticmethod
    def dropdown_items_label_name_period(_id, items: list, label_text, color: list):
        col = dbc.Col(
            [
                feature_fuc.label_name(label_text, _id),
                dbc.Row([
                    feature_fuc.dropdown_item(
                        f"{_id}_year", items[0], color[0]),
                    dbc.InputGroupText("年"),
                    feature_fuc.dropdown_item(
                        f"{_id}_period", items[1], color[1]),
                    dbc.InputGroupText("期"), ])

            ],
            width=3
        )
        return col

    @staticmethod
    def label_name_text(_id, label_text, text_id, unit):
        col = dbc.Col(
            [
                feature_fuc.label_name(label_text, _id),
                dbc.Row([
                    html.H5(id=text_id),
                    dbc.InputGroupText(unit)
                ])
            ],
            width=3
        )
        return col

    def modal_table(_id, button_name, header, df):
        modal = html.Div(
            [
                dbc.Button(button_name, id=f"open_{_id}",
                           className="m-3", n_clicks=0),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            dbc.ModalTitle(
                                html.H3(header),
                                className="m-3"
                            ),
                            close_button=False,
                        ),
                        dbc.ModalBody([feature_fuc.table_dataframe(df)]),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close", id=f"close_{_id}", className="ms-auto", n_clicks=0
                            )
                        ),
                    ],
                    size="xl",
                    id=f"modal_{_id}",
                    is_open=False,
                    scrollable=True,
                ),
            ]
        )
        return modal


class callback_fuc:
    # area_output
    # _I7
    @staticmethod
    def regional_bonus(area):
        bonus = 0
        if area == "北部地區":
            bonus = 15
        elif area == "台東":
            bonus = 8
        return bonus

    # 投資試算表
    # C5、C10
    @staticmethod
    def bank_loan_percent(program_type, bank_loan_ratio):
        # program_type = feature_fuc.judge_is_none(program_type)
        bank_loan_ratio = feature_fuc.judge_is_none(bank_loan_ratio)
        res = 0
        if program_type == "自付，貸款":
            res = bank_loan_ratio
        elif program_type == "免出資":
            res = 100
        return res

    # C9
    @staticmethod
    def customer_discount_program_percent(customer_offers):
        customer_offers = feature_fuc.judge_is_none(customer_offers)
        return customer_offers

    # C6
    @staticmethod
    def actual_expenses_percent(program_type, bank_loan_ratio):
        program_type = feature_fuc.judge_is_none(program_type)
        bank_loan_ratio = feature_fuc.judge_is_none(bank_loan_ratio)
        res = 100 - \
            callback_fuc.bank_loan_percent(program_type, bank_loan_ratio)
        return res

    # C11

    @staticmethod
    def loan_annual_interest_rate_percent(program_type, bank_loan_rate):
        bank_loan_rate = feature_fuc.judge_is_none(bank_loan_rate)
        res = bank_loan_rate
        if program_type == "自付，無貸款":
            res = 0
        return res

    # C12
    @staticmethod
    def loan_term_percent(bank_loan_term, program_type, bank_loan_ratio):
        bank_loan_term = feature_fuc.judge_is_none(bank_loan_term)
        res = bank_loan_term
        if callback_fuc.bank_loan_percent(program_type, bank_loan_ratio) == 0:
            res = 0
        return res

    # C15
    @staticmethod
    def loan_fee_percent(program_type):
        res = 0
        if program_type == "自付，貸款":
            res = 1
        return res

    # C16
    @staticmethod
    def pay_after_loan_percent(customer_offers, bank_loan_ratio, program_type):
        # C4-C9-C10
        res = 0
        C9 = callback_fuc.customer_discount_program_percent(customer_offers)
        C10 = callback_fuc.bank_loan_percent(program_type, bank_loan_ratio)
        res = 100 - C9 - C10
        if program_type == "免出資":
            res = 0
        return res

    # D4
    @staticmethod
    def tax_free_construction_costs(construction_cost, other_costs):
        # 資料輸入!D7+資料輸入!D8
        res = 0
        construction = feature_fuc.judge_is_none(construction_cost)
        other = feature_fuc.judge_is_none(other_costs)
        res = construction + other
        return res

    # D5
    @staticmethod
    def bank_loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio):
        # D4*C5
        res = 0
        D4 = callback_fuc.tax_free_construction_costs(
            construction_cost, other_costs)
        C5 = callback_fuc.bank_loan_percent(program_type, bank_loan_ratio)
        res = D4 * C5 / 100
        return res

    # D6
    @staticmethod
    def actual_expenses_costs(construction_cost, other_costs, program_type, bank_loan_ratio):
        # D6 = D4-D5
        res = 0
        D4 = callback_fuc.tax_free_construction_costs(
            construction_cost, other_costs)
        D5 = callback_fuc.bank_loan_fee_costs(
            construction_cost, other_costs, program_type, bank_loan_ratio)
        res = D4-D5
        return res

    # D7

    @staticmethod
    def total_project_costs(system_capacity, construction_cost, other_costs):
        # "=ROUND(D4*H3,0)"
        res = 0
        D4 = callback_fuc.tax_free_construction_costs(
            construction_cost, other_costs)
        H3 = feature_fuc.judge_is_none(system_capacity)  # H3 =資料輸入!D6
        res = round(D4 * H3, 0)
        return res

    # D8

    @staticmethod
    def actual_total_expenses_costs(system_capacity, construction_cost, other_costs, program_type, bank_loan_ratio):
        # = "=ROUND(D6*H3,0)"
        res = 0
        D6 = callback_fuc.actual_expenses_costs(
            construction_cost, other_costs, program_type, bank_loan_ratio)
        H3 = feature_fuc.judge_is_none(system_capacity)  # H3 =資料輸入!D6
        res = round(D6*H3, 0)
        return res

    # D9
    @staticmethod
    def customer_discount_program_costs(construction_cost, other_costs, system_capacity, customer_offers):
        # = "=ROUND(D4*H3*C9,0)"
        res = 0
        D4 = callback_fuc.tax_free_construction_costs(
            construction_cost, other_costs)
        H3 = feature_fuc.judge_is_none(system_capacity)  # H3 =資料輸入!D6
        C9 = callback_fuc.customer_discount_program_percent(customer_offers)
        res = round(D4*H3*C9, 0)
        return res

    # D10
    def bank_loan_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity):
        #  = "=ROUND((D4)*$C10*H$3,0)"
        res = 0
        D4 = callback_fuc.tax_free_construction_costs(
            construction_cost, other_costs)
        C10 = callback_fuc.bank_loan_percent(program_type, bank_loan_ratio)
        H3 = feature_fuc.judge_is_none(system_capacity)  # H3 =資料輸入!D6
        res = round(D4*C10*H3/100, 0)
        return res

    # D13
    def annual_loan_repayment_amount_costs(program_type, bank_loan_rate, bank_loan_term, bank_loan_ratio, construction_cost, other_costs, system_capacity):
        # = '=IF(資料輸入!D20="自付，貸款",ROUND(PMT($C11/12,C12*12,D10,0,0)*12,0),0)'
        res = 0
        C11 = callback_fuc.loan_annual_interest_rate_percent(
            program_type, bank_loan_rate)
        C12 = callback_fuc.loan_term_percent(
            bank_loan_term, program_type, bank_loan_ratio)
        D10 = callback_fuc.bank_loan_costs(
            construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity)
        if program_type == "自付，貸款":
            res = round(npf.pmt((C11/100)/12, C12*12, D10, 0, 0)*12, 0)
            res = feature_fuc.judge_is_none(res)
        return res

    # D14
    def taipower_line_subsidy_costs(shape, strengthen_power_grid, system_capacity, roof_type_parallel_connection_method, installed_kw):
        # '=IF(資料輸入!I5="屋頂型",IF(資料輸入!I19="低壓",資料輸入!R52,IF(資料輸入!I19="高壓",資料輸入!Q52,0)),資料輸入!S52)'
        _D6 = feature_fuc.judge_is_none(system_capacity)
        _I17 = feature_fuc.judge_is_none(installed_kw)

        res = callback_fuc.ground_type_subsidy(_D6, strengthen_power_grid)

        if shape == "屋頂型":  # _I5
            res = 0
            if roof_type_parallel_connection_method == '低壓':
                # _R52
                res = callback_fuc.low_pressure_subsidy(_D6, _I17)

            elif roof_type_parallel_connection_method == '高壓':
                res = callback_fuc.high_pressure_subsidy(_D6, _I17)  # _Q52

        return res

    # _S52
    def ground_type_subsidy(_D6, strengthen_power_grid):
        res = _D6*2068  # _S52
        if strengthen_power_grid == "輸電級":  # _I21
            res = _D6*1352  # _S52
        return res

    # _R52
    def low_pressure_subsidy(_D6, _I17):
        res = _D6*1470
        # _low_pressure_judge
        if _I17 <= 50:
            if ((_D6 + _I17) < 100):
                if ((_D6 + _I17 - 50) < 0):
                    _low_pressure_judge = 0
                else:
                    _low_pressure_judge = (_D6 + _I17 - 50) * 1050
            else:
                _low_pressure_judge = 50*1050
        else:
            if ((_D6 + _I17) < 100):
                _low_pressure_judge = _D6*1050
            else:
                if ((100 - _I17) < 0):
                    _low_pressure_judge = 0
                else:
                    (100 - _I17)*1050

        if _I17 < 100:  # _I17
            if (_D6 + _I17 - 100) <= 0:
                res = 0
            else:
                res = ((_D6 + _I17 - 100) * 1470) + _low_pressure_judge
        return res

    # _Q52
    def high_pressure_subsidy(_D6, _I17):
        res = _D6*630
        if _I17 <= 50:
            if (_D6 - 50 + _I17) < 0:
                res = 0
            else:
                res = (_D6 - 50 + _I17)*630
        return res

    # D15
    def loan_fee_costs(construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity):
        #  = "=ROUND(D10*C15,0)
        D10 = callback_fuc.bank_loan_costs(
            construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity)
        C15 = callback_fuc.loan_fee_percent(program_type)
        res = round(D10*C15/100, 0)
        return res

    # # D16
    def pay_after_loan_costs(system_capacity, construction_cost, other_costs, program_type, bank_loan_ratio, shape, strengthen_power_grid,  roof_type_parallel_connection_method, installed_kw, customer_offers, development_costs):
        #  = "=D8+D14-D9+D15+D17"
        res = 0
        D8 = callback_fuc.actual_total_expenses_costs(
            system_capacity, construction_cost, other_costs, program_type, bank_loan_ratio)
        D14 = callback_fuc.taipower_line_subsidy_costs(
            shape, strengthen_power_grid, system_capacity, roof_type_parallel_connection_method, installed_kw)
        D9 = callback_fuc.customer_discount_program_costs(
            construction_cost, other_costs, system_capacity, customer_offers)
        D15 = callback_fuc.loan_fee_costs(
            construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity)
        D17 = feature_fuc.judge_is_none(development_costs)
        res = D8+D14-D9+D15+D17
        return res

    #  D20
    def customer_offers_costs(construction_cost, other_costs, system_capacity, customer_offers):
        #  "=ROUND(D9/5,0)"
        D9 = callback_fuc.customer_discount_program_costs(
            construction_cost, other_costs, system_capacity, customer_offers)
        res = round(D9/5, 0)
        return res

    # warranty_cost_df
    # B24

    def illustrate_5years():
        # '="售電收入"&C24*100&"%"'
        res = callback_fuc.scale_5years()
        return f"售電收入{res}"

    # B25

    def illustrate_6years():
        # '="售電收入"&C25*100&"%"'
        res = callback_fuc.scale_6years()
        return f"售電收入{res}"

    # B26
    def illustrate_7years(warranty_annual_increment_rate):
        # '="售電收入"&C26*100&"%"'
        res = callback_fuc.scale_7years(warranty_annual_increment_rate)
        return f"售電收入{res}"

    # B28
    def illustrate_20years(warranty_annual_increment_rate):
        # '="售電收入"&C28*100&"%"'
        res = callback_fuc.scale_20years(warranty_annual_increment_rate)
        return f"售電收入{res}"

    # C24
    def scale_5years():
        # "0%"
        res = 0
        return f" {res} % "

    # C25
    def scale_6years():
        # "6%"
        res = 6
        return f" {res} % "

    # C26
    def scale_7years(warranty_annual_increment_rate):
        # '=C25+資料輸入!D15'
        D15 = feature_fuc.judge_is_none(warranty_annual_increment_rate)
        res = feature_fuc.find_first_number(callback_fuc.scale_6years()) + D15
        return f" {res} % "

    # C28
    def scale_20years(warranty_annual_increment_rate):
        # "=C25+資料輸入!D15*14"
        D15 = feature_fuc.judge_is_none(warranty_annual_increment_rate)
        res = feature_fuc.find_first_number(
            callback_fuc.scale_6years()) + D15*14
        return f" {res} % "

    # D24
    def amount_5years():
        # "0%"
        res = 0
        return f" {res} % "

    # D25
    def amount_6years():
        # '=-K18'
        res = 0
        return f" {res} % "

    # D26
    def amount_7years():
        # '=-K19''
        res = 0
        return f" {res} % "

    # D28
    def amount_20years():
        # "=-K32"
        res = 0
        return f" {res} % "

    # D29
    def amount_total():
        # "=-K32"
        res = 0
        return f" {res} % "

    # operating_expense_df

    # B33

    def illustrate_cleaning_fee_water():
        # ="每年"&C33*100&"%"
        res = feature_fuc.find_first_number(
            callback_fuc.scale_cleaning_fee_water())
        return f" 每年 {res*100} %"

    # B34=
    def illustrate_property_insurance_costs():
        # "每年"&C34*100&"%""
        res = feature_fuc.find_first_number(
            callback_fuc.scale_property_insurance_costs())
        return f" 每年 {res*100} %"

    # "C33
    def scale_cleaning_fee_water():
        # 0.025%"
        res = 0.025
        return f" {res} % "

    # "C34
    def scale_property_insurance_costs():
        #  0.5%"
        res = 0.05
        return f" {res} % "

    # 'C35
    def scale_installation_space_cost(construction_cost, other_costs, system_capacity, customer_offers, program_type, bank_loan_ratio):
        # =IF(資料輸入!D10>0,ROUND(D35/H34,4),IF(資料輸入!D9>0,資料輸入!D9,0))'
        # todo callback
        res = 0
        # D10 = callback_fuc.bank_loan_costs(
        #     construction_cost, other_costs, program_type, bank_loan_ratio, system_capacity)
        # D9 = callback_fuc.customer_discount_program_costs(
        #     construction_cost, other_costs, system_capacity, customer_offers)
        # D35 = ...
        # H34 = ...
        # if D10 > 0:
        #     res = round(D35/H34, 4)
        # else:
        #     if D9 > 0:
        #         res = D9
        return res

     # 'C37=
    def scale_module_recycling_fund(module_recycling_fund):
        # 資料輸入!I8'
        res = feature_fuc.judge_is_none(module_recycling_fund)
        return res

    # 'C38
    def scale_removal_fee(demolition_cost):
        # =資料輸入!D13'
        res = feature_fuc.judge_is_none(demolition_cost)
        return res

    # 'D33
    def amount_cleaning_fee_water(system_capacity, construction_cost, other_costs):
        #  =ROUND(D7*C33,0)'
        D7 = callback_fuc.total_project_costs(
            system_capacity, construction_cost, other_costs)
        C33 = feature_fuc.find_first_number(
            callback_fuc.scale_cleaning_fee_water())
        res = round(D7*C33, 0)
        return res

     # 'D34
    def amount_property_insurance_costs(system_capacity, construction_cost, other_costs):
        # =ROUND(D7*C34,0)'
        D7 = callback_fuc.total_project_costs(
            system_capacity, construction_cost, other_costs)
        C34 = feature_fuc.find_first_number(
            callback_fuc.scale_property_insurance_costs())
        res = round(D7*C34, 0)
        return res

    # # 'D35
    # def amount_property_insurance_costs(system_capacity, construction_cost, other_costs):
    #     # 'D35=IF(資料輸入!D9>0,ROUND(C35*H34,0),IF(資料輸入!D10="",0,資料輸入!D10))'
    #     D9 =
    #     D10 =
    #     C35 =
    #     H34 =
    #     if D9 > 0:
    #         res = round(C35*H34,0)
    #     else:
    #         if D10 == "":
    #             res = 0
    #         else:
    #             res = D10
    #     return res

    # # 'D36
    # def amount_operating_expense_total(system_capacity, construction_cost, other_costs):
    #     # =SUM(D33:D35)'
    #     D33 = callback_fuc.amount_cleaning_fee_water(system_capacity, construction_cost, other_costs)
    #     D34 = callback_fuc.amount_property_insurance_costs(system_capacity, construction_cost, other_costs)
    #     D35 =
    #     res = D33 + D34 + D35
    #     return res

    # 'D37
    def amount_module_recycling_fund(module_recycling_fund, system_capacity):
        # =ROUND(C37*H3/10,0)'
        C37 = callback_fuc.scale_module_recycling_fund(module_recycling_fund)
        H3 = feature_fuc.judge_is_none(system_capacity)  # H3 =資料輸入!D6
        res = round(C37*H3/10, 0)
        return res

    # ''D38=H3*C38'
    def amount_removal_fee(system_capacity, demolition_cost):
        # H3*C38
        H3 = feature_fuc.judge_is_none(system_capacity)  # H3 =資料輸入!D6
        C38 = callback_fuc.scale_removal_fee(demolition_cost)
        res = H3*C38
        return res

    # 1 G13 =資料輸入!D11
    def ese_1(estimated_first_year_system):
        D11 = feature_fuc.judge_is_none(estimated_first_year_system)
        res = D11
        return res

    # ese_2~ese_20
    def estimated_system_efficiency(ese_num, estimated_first_year_system, pr_annual_decline_rate):
        # G14 =G13-資料輸入!$D$14\
        _D11 = feature_fuc.judge_is_none(estimated_first_year_system)
        G14 = feature_fuc.judge_is_none(pr_annual_decline_rate)
        res = _D11 - ((G14)*(ese_num - 1))
        return res

    # electricity_income_statement eis_1~eis_20 H13~H
    def electricity_income_statement(ese_num, shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, estimated_sunshine, estimated_first_year_system, pr_annual_decline_rate):
        # "=投資試算表!$H$5*ROUND($H$6*$H$3*365*$G13,0)"
        H5 = callback_fuc.estimated_wholesale_rate(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year,
                                                   annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year)  # N9
        # print(f"H5_{H5}")
        H6 = feature_fuc.judge_is_none(estimated_sunshine)  # =資料輸入!D5
        H3 = feature_fuc.judge_is_none(system_capacity)  # H3 =資料輸入!D6

        if ese_num == 1:
            ese = callback_fuc.ese_1(estimated_first_year_system) / 100  # G13
        else:
            # G14~~
            ese = callback_fuc.estimated_system_efficiency(
                ese_num, estimated_first_year_system, pr_annual_decline_rate) / 100
        # print(f"{ese_num}_{ese}")
        res = round(H5*round(H6*H3*365*ese, 0), 0)
        return res

    # H5
    # _N9 # =IF(I5="地面型",資料輸入!O56,IF(I5="水面型",資料輸入!O57,IF(D6="","",IF(I18="是",資料輸入!O55,IF((I17+D6)<20,資料輸入!O51,IF((I17+D6)<100,資料輸入!L59,IF((I17+D6)<500,資料輸入!O54,資料輸入!O55)))))))
    def estimated_wholesale_rate(shape, roof_type_grid_connection_engineering, module_recycling_fund, installed_kw, system_capacity, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year):
        _I5 = shape
        _I20 = roof_type_grid_connection_engineering
        _I8 = feature_fuc.judge_is_none(module_recycling_fund)
        _I17 = feature_fuc.judge_is_none(installed_kw)
        _O51 = callback_fuc.electricity_sales_rate(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                   high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, 5.8952, 5.7848, _J29_)
        _O52 = callback_fuc.electricity_sales_rate(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                   high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, 4.5549, 4.4538, _J30_)
        _O53 = callback_fuc.electricity_sales_rate(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                   high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, 4.4861, 4.3864, _J31_, _I31_)
        _O54 = callback_fuc.electricity_sales_rate(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                   high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, 4.0970, 3.9666, _J32_, _I32_)
        _O55 = callback_fuc.electricity_sales_rate(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                   high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, 4.1122, 3.9727, _J33_, _I33_)
        _O56 = callback_fuc.electricity_sales_rate_type(annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                        high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, 4.0031, 3.8680, _J34_)
        _O57 = callback_fuc.electricity_sales_rate_type(annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid,
                                                        high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, 4.3960, 4.2612, _J35_)
        # _L59 = =IF(I20="是",O52,O53)
        _L59 = _O52 if _I20 == 1 else _O53
        # print(f"_O51~_O57 {_O51}, {_O52}, {_O53}, {_O54}, {_O55}, {_O56}, {_O57}")
        _D6 = feature_fuc.judge_is_none(system_capacity)
        # print(('========'))

        res = _O55
        if _I5 == "地面型":
            res = _O56
        if _I5 == "水面型":
            res = _O57
        if _D6 == "":
            res = ""
        if _I8 == "是":
            # TODO: I8 不可能為是?
            res = _O55
        if (_I17 + _D6) < 20:
            res = _O51
        if (_I17 + _D6) < 100:
            res = _L59
        if (_I17 + _D6) < 500:
            res = _O54
        return res

    # _O51 ~ O55
    def electricity_sales_rate(roof_type_grid_connection_engineering, annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, period_1, period_2, j_input, t_input=None):
        # =ROUND((ROUND(L51*(1+M51),4)+N51)*(1-$I$4),4)
        _L51 = callback_fuc.fit_upper_limit(
            annual_wholesale_rate_year, annual_wholesale_rate_period, period_1, period_2)
        _M51 = callback_fuc.regional_bonus(area) / 100  # _M51~_M57 _I7
        _N51 = callback_fuc.plus_rate_total(roof_type_grid_connection_engineering, strengthen_power_grid,
                                            high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, j_input, t_input)
        _I4 = feature_fuc.judge_is_none(estimated_rate_reduction_next_year)
        # print(_L51, _M51, _N51, _I4)
        res = round((round(_L51*(1+_M51), 4) + _N51)*(1 - _I4), 4)
        return res

    # _N51 ~ _N55 ( 地面型&水面型分開 )

    def plus_rate_total(roof_type_grid_connection_engineering, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, j_input, t_input=None):
        _G29 = _G29_
        _I21 = strengthen_power_grid
        _J = j_input
        _I9 = high_efficiency_bonus
        _L29 = _L29_
        _I12 = fishing_environment
        _M29 = _M29_
        _I13 = agriculture_fishing_green_energy
        _I20 = roof_type_grid_connection_engineering
        # TODO:let it work ( _L43, _N43 )

        # =  _J43 + _K43 + _L53 + _M53 + _N53 + _O53 + _P53 + _Q53 + _R53 + _S53 + _T53
        # _J43 = (_J43 ~ _J49)
        _J43 = _F29_
        # _K43=IF($I$21="輸電級",$G29,0)
        _K43 = _G29 if _I21 == "輸電級" else 0
        # _L43
        _L43 = 0
        # _M43
        # =IF($I$9="是",J29,0)
        _M43 = _J if _I9 == 1 else 0
        # _N43
        _N43 = 0
        # _O43
        # =IF($I$12="是",L29,0)
        _O43 = _L29 if _I12 == 1 else 0
        # _P43
        # =IF($I$13="是",M29,0)
        _P43 = _M29 if _I13 == 1 else 0

        _T45 = 0
        # ( 只有45-47有 )
        if t_input:
            # =IF($I$20="是",I31,0)
            _T45 = t_input if _I20 == 1 else 0

        # print("plus_rate_total")
        # print(_J43, _K43, _L43, _M43, _N43, _O43, _P43)

        res = _J43 + _K43 + _L43 + _M43 + _N43 + _O43 + _P43 + _T45
        return res

    # _O56 ~ O57 ( 地面型水面型 )

    def electricity_sales_rate_type(annual_wholesale_rate_year, annual_wholesale_rate_period, area, strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, estimated_rate_reduction_next_year, period_1, period_2, j_input):
        # =ROUND((ROUND(L56*(1+M56),4)+N56)*(1-$I$4),4)
        _L51 = callback_fuc.fit_upper_limit(
            annual_wholesale_rate_year, annual_wholesale_rate_period, period_1, period_2)
        _M51 = callback_fuc.regional_bonus(area) / 100  # _M51~_M57 _I7
        _N51 = callback_fuc.plus_rate_total_type(
            strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, j_input)
        _I4 = feature_fuc.judge_is_none(estimated_rate_reduction_next_year)
        # print(_L51, _M51, _N51, _I4)
        res = round((round(_L51*(1+_M51), 4) + _N51)*(1 - _I4), 4)
        return res

    # _N51 ~ _N55 ( 地面型&水面型分開 )
    def plus_rate_total_type(strengthen_power_grid, high_efficiency_bonus, fishing_environment, agriculture_fishing_green_energy, j_input):
        _G29 = _G29_
        _I21 = strengthen_power_grid
        _J = j_input
        _I9 = high_efficiency_bonus
        _L29 = _L29_
        _I12 = fishing_environment
        _M29 = _M29_
        _I13 = agriculture_fishing_green_energy
        _H34 = _H34_
        # TODO:let it work ( _L43, _N43 )

        # =  _J43 + _K43 + _L53 + _M53 + _N53 + _O53 + _P53 + _Q53 + _R53 + _S53 + _T53
        # _J43 = (_J43 ~ _J49)
        _J43 = _F29_
        # _K43=IF($I$21="輸電級",$G29,0)
        _K43 = _G29 if _I21 == "輸電級" else (_H34 if _I21 == "配電級" else 0)
        # _L43
        _L43 = 0
        # _M43
        # =IF($I$9="是",J29,0)
        _M43 = _J if _I9 == 1 else 0
        # _N43
        _N43 = 0
        # _O43
        # =IF($I$12="是",L29,0)
        _O43 = _L29 if _I12 == 1 else 0
        # _P43
        # =IF($I$13="是",M29,0)
        _P43 = _M29 if _I13 == 1 else 0

        res = _J43 + _K43 + _L43 + _M43 + _N43 + _O43 + _P43
        return res

    # _L51~_L
    def fit_upper_limit(annual_wholesale_rate_year, annual_wholesale_rate_period, period_1, period_2):
        # =IF($I$3=$D$27,$D29,IF($I$3=$E$27,$E29,"請選對應年度"))
        # res = "請選對應年度"
        res = 0
        # 年
        if annual_wholesale_rate_year == 111:
            if annual_wholesale_rate_period == 1:
                res = period_1
            elif annual_wholesale_rate_period == 2:
                res = period_2
        return res

    # def loan_disbursement_statement():
    #     # =IF(資料輸入!$D$21="本利平均攤還",IF(F12>=$C$12,0,ROUND(PMT($C$11/12,$C$12*12,D$10,0,0)*12,0)),
    #     # IF(銀行計算頁!D5="",0,-銀行計算頁!D5))
    #     _D21 =
    #     F12 =
    #     C12 =
    #     C11 =
    #     D10 =
    #     bank_D5 =

    #     res = 0 if bank_D5 == "" else bank_D5

    #     if _D21 == "本利平均攤還":
    #         if F12 >= C12:
    #             res = 0
    #         else:
    #             res = round(npf.pmt((C11/100)/12, C12*12, D10, 0, 0)*12, 0)
    #     return res
