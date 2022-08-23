from enum import auto
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import datetime

import dash_bootstrap_components as dbc
import pandas as pd
from utility.utils import feature_fuc, form_func, callback_fuc

# 工程費用說明


def project_costs_df(bank_loan_fee_percent, actual_expenses_percent, customer_discount_program_percent, bank_loan_percent, loan_annual_interest_rate_percent, loan_term_percent, loan_fee_percent, pay_after_loan_percent,
                     tax_free_construction_costs, bank_loan_fee_costs, actual_expenses_costs, total_project_costs, actual_total_expenses_costs, customer_discount_program_costs, bank_loan_costs, annual_loan_repayment_amount_costs, taipower_line_subsidy_costs, loan_fee_costs, pay_after_loan_costs):

    # C5 =IF(資料輸入!D20="自付，貸款",資料輸入!D22,IF(資料輸入!D20="免出資",1,0))
    _bank_loan_fee_percent = feature_fuc.result(bank_loan_fee_percent)
    _actual_expenses_percent = feature_fuc.result(
        actual_expenses_percent)  # "C6 = C4-C5"
    _customer_discount_program_percent = feature_fuc.result(
        customer_discount_program_percent)  # "C9 =資料輸入!D19"
    _bank_loan_percent = feature_fuc.result(
        bank_loan_percent)  # C10'=IF(資料輸入!D20="自付，貸款",資料輸入!D22,IF(資料輸入!D20="免出資",1,0))'
    _loan_annual_interest_rate_percent = feature_fuc.result(
        loan_annual_interest_rate_percent)  # C11'=IF(資料輸入!D20="自付，無貸款",0,資料輸入!D23)'
    _loan_term_percent = feature_fuc.result(
        loan_term_percent)  # "C12 =IF(C10=0,0,資料輸入!D24)"
    _loan_fee_percent = feature_fuc.result(
        loan_fee_percent)  # 'C15 = IF(資料輸入!D20="自付，貸款",1%,0)'
    _pay_after_loan_percent = feature_fuc.result(
        pay_after_loan_percent)  # C16 = IF(資料輸入!D20="免出資",0,C4-C9-C10)

    _tax_free_construction_costs = feature_fuc.result(
        tax_free_construction_costs)  # D4 = 資料輸入!D7+資料輸入!D8
    _bank_loan_fee_costs = feature_fuc.result(
        bank_loan_fee_costs)  # "D5 = D4*C5"
    _actual_expenses_costs = feature_fuc.result(
        actual_expenses_costs)  # D6 = D4-D5
    _total_project_costs = feature_fuc.result(
        total_project_costs)  # D7 = "=ROUND(D4*H3,0)"
    _actual_total_expenses_costs = feature_fuc.result(
        actual_total_expenses_costs)  # D8 = "=ROUND(D6*H3,0)"
    _customer_discount_program_costs = feature_fuc.result(
        customer_discount_program_costs)  # D9 = "=ROUND(D4*H3*C9,0)"
    _bank_loan_costs = feature_fuc.result(
        bank_loan_costs)  # D10 = "=ROUND((D4)*$C10*H$3,0)"
    _annual_loan_repayment_amount_costs = feature_fuc.result(
        annual_loan_repayment_amount_costs)  # D13 = '=IF(資料輸入!D20="自付，貸款",ROUND(PMT($C11/12,C12*12,D10,0,0)*12,0),0)'
    # D14 = '=IF(資料輸入!I5="屋頂型",IF(資料輸入!I19="低壓",資料輸入!R52,IF(資料輸入!I19="高壓",資料輸入!Q52,0)),資料輸入!S52)'
    _taipower_line_subsidy_costs = feature_fuc.result(
        taipower_line_subsidy_costs)
    _loan_fee_costs = feature_fuc.result(
        loan_fee_costs)  # D15 = "=ROUND(D10*C15,0)
    _pay_after_loan_costs = feature_fuc.result(
        pay_after_loan_costs)  # D16 = "=D8+D14-D9+D15+D17"

    project_costs_df = pd.DataFrame(
        {
            "項目": ["未稅建造費用(NT$/kW)", "銀行核貸費用(NT$/kW)", "實際支出費用(NT$/kW)", "工程總支出費用(NT$)",
                   "實際總支出費用(NT$)", "客戶優惠專案", "銀行貸款", "貸款年利率(%)",
                   "貸款年限", "貸款每年還款金額", "台電線路補助費(預估值)", "貸款手續費",
                   "貸款後自付總費用(NT$)", "宣鼎開發費"],

            "說明": ["建造費用", "-", "-", "-",
                   "-", "-", "貸款成數", "-",
                   "-", "本利攤還", "由台電收取", "-",
                   "-", "-"],

            "比例 ( % )": [feature_fuc.result_type("100"), _bank_loan_fee_percent, _actual_expenses_percent, "-",
                         "-", _customer_discount_program_percent, _bank_loan_percent, _loan_annual_interest_rate_percent,
                         _loan_term_percent, "-", "-", _loan_fee_percent,
                         _pay_after_loan_percent, "-"],

            "金額": [_tax_free_construction_costs, _bank_loan_fee_costs, _actual_expenses_costs, _total_project_costs,
                   _actual_total_expenses_costs, _customer_discount_program_costs, _bank_loan_costs, "-",
                   "", _annual_loan_repayment_amount_costs, _taipower_line_subsidy_costs, _loan_fee_costs,
                   _pay_after_loan_costs,
                   form_func.input_frame_label_name("", "development_costs", _width=6)]
        }
    )
    return project_costs_df

# 客戶優惠專案


def customer_offers_df(customer_offers_costs):
    _customer_offers_costs = feature_fuc.result(
        customer_offers_costs)  # D20 "=ROUND(D9/5,0)"
    customer_offers_df = pd.DataFrame(
        {
            "項目": ["每年還款金額"],

            "說明": ["分期5年"],

            "比例或金額": ["-"],

            "經費": [_customer_offers_costs],
        }
    )
    return customer_offers_df

# 保固費用分析


def warranty_cost_df(illustrate_7years, illustrate_20years, scale_7years, scale_20years,
                     amount_6years, amount_7years, amount_20years, amount_total):
    _illustrate_5years = feature_fuc.result_type(
        f"售電收入{callback_fuc.illustrate_5years()} % ")  # '="售電收入"&C24*100&"%"'
    _illustrate_6years = feature_fuc.result_type(
        f"售電收入{callback_fuc.illustrate_6years()} % ")  # '="售電收入"&C25*100&"%"'
    _illustrate_7years = feature_fuc.result(
        illustrate_7years)  # '="售電收入"&C26*100&"%"'
    _illustrate_20years = feature_fuc.result(
        illustrate_20years)  # '="售電收入"&C28*100&"%"'

    _scale_5years = feature_fuc.result_type(f"{callback_fuc.scale_5years()} % ")  # "0%"
    _scale_6years = feature_fuc.result_type(f"{callback_fuc.scale_6years()} % ")  # "6%"
    _scale_7years = feature_fuc.result(scale_7years)  # '=C25+資料輸入!D15'
    _scale_20years = feature_fuc.result(scale_20years)  # "=C25+資料輸入!D15*14"

    _amount_5years = feature_fuc.result_type(callback_fuc.amount_5years())  # "0%"
    _amount_6years = feature_fuc.result(amount_6years)  # '=-K18'
    _amount_7years = feature_fuc.result(amount_7years)  # '=-K19'
    _amount_20years = feature_fuc.result(amount_20years)  # "=-K32"
    _amount_total = feature_fuc.result(amount_total)  # "=-K32"

    warranty_cost_df = pd.DataFrame(
        {
            "項目": ["預估1~5年每年維護費用", "預估第6年維護費用", "預估第7年維護費用", "...",
                   "預估第20年維護費用", "合計"],

            "說明": [_illustrate_5years, _illustrate_6years, _illustrate_7years, "...",
                   _illustrate_20years, "-"],

            "比例或金額": [_scale_5years, _scale_6years, _scale_7years, '...',
                      _scale_20years, "-"],

            "經費": [_amount_5years, _amount_6years, _amount_7years, "...",
                   _amount_20years, _amount_total],
        }
    )
    return warranty_cost_df

# 營運費用分析


def operating_expense_df(illustrate_cleaning_fee_water, illustrate_property_insurance_costs,
                         scale_cleaning_fee_water, scale_property_insurance_costs, scale_installation_space_cost, scale_module_recycling_fund, scale_removal_fee,
                         amount_cleaning_fee_water, amount_property_insurance_costs, amount_installation_space_cost, amount_operating_expense_total, amount_module_recycling_fund, amount_removal_fee):
    # _illustrate
    _illustrate_cleaning_fee_water = feature_fuc.result_type(
        f" 每年 {callback_fuc.illustrate_cleaning_fee_water()} %")  # B33="每年"&C33*100&"%"
    _illustrate_property_insurance_costs = feature_fuc.result_type(
        f" 每年 {callback_fuc.illustrate_property_insurance_costs()} %")  # B34="每年"&C34*100&"%""
    # _scale
    _scale_cleaning_fee_water = feature_fuc.result_type(
        f" {callback_fuc.scale_cleaning_fee_water()} % ")  # "C33 0.025%"
    _scale_property_insurance_costs = feature_fuc.result_type(
        f" {callback_fuc.scale_property_insurance_costs()} % ")  # "C34 0.5%"
    # 'C35=IF(資料輸入!D10>0,ROUND(D35/H34,4),IF(資料輸入!D9>0,資料輸入!D9,0))'
    _scale_installation_space_cost = feature_fuc.result(
        scale_installation_space_cost)
    _scale_module_recycling_fund = feature_fuc.result(
        scale_module_recycling_fund)  # 'C37=資料輸入!I8'
    _scale_removal_fee = feature_fuc.result(
        scale_removal_fee)  # 'C38=資料輸入!D13'
    # _amount
    _amount_cleaning_fee_water = feature_fuc.result(
        amount_cleaning_fee_water)  # 'D33 =ROUND(D7*C33,0)'
    _amount_property_insurance_costs = feature_fuc.result(
        amount_property_insurance_costs)  # 'D34=ROUND(D7*C34,0)'
    # 'D35=IF(資料輸入!D9>0,ROUND(C35*H34,0),IF(資料輸入!D10="",0,資料輸入!D10))'
    _amount_installation_space_cost = feature_fuc.result(
        amount_installation_space_cost)
    _amount_operating_expense_total = feature_fuc.result(
        amount_operating_expense_total)  # 'D36=SUM(D33:D35)'
    _amount_module_recycling_fund = feature_fuc.result(
        amount_module_recycling_fund)  # 'D37=ROUND(C37*H3/10,0)'
    _amount_removal_fee = feature_fuc.result(
        amount_removal_fee)  # ''D38=H3*C38'

    operating_expense_df = pd.DataFrame(
        {
            "項目": ["清潔費用(水費)", "產險費用(颱風 火災 地震 失竊)", "安裝空間成本(租賃金)", "合計",
                   "模組回收基金", "拆除費"],

            "說明": [_illustrate_cleaning_fee_water, _illustrate_property_insurance_costs, '年租金', '-',
                   '十年分期', '-'],

            "比例或金額": [_scale_cleaning_fee_water, _scale_property_insurance_costs, _scale_installation_space_cost, '-',
                      _scale_module_recycling_fund, _scale_removal_fee],

            "經費": [_amount_cleaning_fee_water, _amount_property_insurance_costs, _amount_installation_space_cost, _amount_operating_expense_total,
                   _amount_module_recycling_fund, _amount_removal_fee],
        }
    )
    return operating_expense_df

# 躉售費率
def wholesale_rate_df(fit_1, fit_2, fit_3, fit_4, fit_5, fit_6,
                      addition_1, addition_2, addition_3, addition_4, addition_5, addition_6,
                      plus_rate_total_1, plus_rate_total_2, plus_rate_total_3, plus_rate_total_4, plus_rate_total_5, plus_rate_total_6,
                      electricity_sales_rate_1, electricity_sales_rate_2, electricity_sales_rate_3, electricity_sales_rate_4, electricity_sales_rate_5, electricity_sales_rate_6):
    _fit_1, _fit_2, _fit_3, _fit_4, _fit_5, _fit_6 = list(
        map(feature_fuc.result, [fit_1, fit_2, fit_3, fit_4, fit_5, fit_6]))
    _addition_1, _addition_2, _addition_3, _addition_4, _addition_5, _addition_6 = list(
        map(feature_fuc.result, [addition_1, addition_2, addition_3, addition_4, addition_5, addition_6]))
    _plus_rate_total_1, _plus_rate_total_2, _plus_rate_total_3, _plus_rate_total_4, _plus_rate_total_5, _plus_rate_total_6 = list(
        map(feature_fuc.result, [plus_rate_total_1, plus_rate_total_2, plus_rate_total_3, plus_rate_total_4, plus_rate_total_5, plus_rate_total_6]))
    _electricity_sales_rate_1, _electricity_sales_rate_2, _electricity_sales_rate_3, _electricity_sales_rate_4, _electricity_sales_rate_5, _electricity_sales_rate_6 = list(
        map(feature_fuc.result, [electricity_sales_rate_1, electricity_sales_rate_2, electricity_sales_rate_3, electricity_sales_rate_4, electricity_sales_rate_5, electricity_sales_rate_6]))
    wholesale_rate_df = pd.DataFrame(
        {
            "容量": ["<20", "20-99", "100-499", ">500", "地面型", "水面型"],

            # fit
            "FIT上限": [_fit_1, _fit_2, _fit_3, _fit_4, _fit_5, _fit_6],

            # addition
            "北部加成": [_addition_1, _addition_2, _addition_3, _addition_4, _addition_5, _addition_6],

            # plus_rate_total
            "外加費率加總": [_plus_rate_total_1, _plus_rate_total_2, _plus_rate_total_3, _plus_rate_total_4, _plus_rate_total_5, _plus_rate_total_6],

            # electricity_sales_rate
            "售電費率": [_electricity_sales_rate_1, _electricity_sales_rate_2, _electricity_sales_rate_3, _electricity_sales_rate_4, _electricity_sales_rate_5, _electricity_sales_rate_6],
        }
    )
    return wholesale_rate_df

# 投資報酬分析表


def return_on_investment_df(ese_1, ese_2, ese_3, ese_4, ese_5, ese_6, ese_7, ese_8, ese_9, ese_10,
                            ese_11, ese_12, ese_13, ese_14, ese_15, ese_16, ese_17, ese_18, ese_19, ese_20, ese_sum, ese_average,
                            eis_1, eis_2, eis_3, eis_4, eis_5, eis_6, eis_7, eis_8, eis_9, eis_10,
                            eis_11, eis_12, eis_13, eis_14, eis_15, eis_16, eis_17, eis_18, eis_19, eis_20, eis_sum, eis_average,
                            lds_1, lds_2, lds_3, lds_4, lds_5, lds_6, lds_7, lds_8, lds_9, lds_10,
                            lds_11, lds_12, lds_13, lds_14, lds_15, lds_16, lds_17, lds_18, lds_19, lds_20, lds_sum,
                            cdp_1, cdp_2, cdp_3, cdp_4, cdp_5, cdp_sum,
                            warranty_1, warranty_2, warranty_3, warranty_4, warranty_5, warranty_6, warranty_7, warranty_8, warranty_9, warranty_10,
                            warranty_11, warranty_12, warranty_13, warranty_14, warranty_15, warranty_16, warranty_17, warranty_18, warranty_19, warranty_20, warranty_sum,
                            oe_1, oe_2, oe_3, oe_4, oe_5, oe_6, oe_7, oe_8, oe_9, oe_10,
                            oe_11, oe_12, oe_13, oe_14, oe_15, oe_16, oe_17, oe_18, oe_19, oe_20, oe_sum,
                            total_r_0, total_r_1, total_r_2, total_r_3, total_r_4, total_r_5, total_r_6, total_r_7, total_r_8, total_r_9, total_r_10,
                            total_r_11, total_r_12, total_r_13, total_r_14, total_r_15, _otal_r_16, total_r_17, total_r_18, total_r_19, total_r_20,  total_r_sum,
                            cash_flow_0, cash_flow_1, cash_flow_2, cash_flow_3, cash_flow_4, cash_flow_5, cash_flow_6, cash_flow_7, cash_flow_8, cash_flow_9, cash_flow_10,
                            cash_flow_11, cash_flow_12, cash_flow_13, cash_flow_14, cash_flow_15, cash_flow_16, cash_flow_17, cash_flow_18, cash_flow_19, cash_flow_20):

    # estimated_system_efficiency ese
    # # 1 G13 =資料輸入!D11
    # 2 G14 =G13-資料輸入!$D$14\
    # 3 G15 =G14-資料輸入!$D$14
    _ese_1, _ese_2, _ese_3, _ese_4, _ese_5, _ese_6, _ese_7, _ese_8, _ese_9, _ese_10, \
        _ese_11, _ese_12, _ese_13, _ese_14, _ese_15, _ese_16, _ese_17, _ese_18, _ese_19, _ese_20, \
        _ese_sum, _ese_average = list(
            map(feature_fuc.result, [ese_1, ese_2, ese_3, ese_4, ese_5, ese_6, ese_7, ese_8, ese_9, ese_10,
                                     ese_11, ese_12, ese_13, ese_14, ese_15, ese_16, ese_17, ese_18, ese_19, ese_20,
                                     ese_sum, ese_average]))

    # electricity_income_statement eis
    # "=投資試算表!$H$5*ROUND($H$6*$H$3*365*$G13,0)"
    # =投資試算表!$H$5*ROUND($H$6*$H$3*365*$G14,0)
    _eis_1, _eis_2, _eis_3, _eis_4, _eis_5, _eis_6, _eis_7, _eis_8, _eis_9, _eis_10, \
        _eis_11, _eis_12, _eis_13, _eis_14, _eis_15, _eis_16, _eis_17, _eis_18, _eis_19, _eis_20, \
        _eis_sum, _eis_average = list(
            map(feature_fuc.result, [eis_1, eis_2, eis_3, eis_4, eis_5, eis_6, eis_7, eis_8, eis_9, eis_10,
                                     eis_11, eis_12, eis_13, eis_14, eis_15, eis_16, eis_17, eis_18, eis_19, eis_20,
                                     eis_sum, eis_average]))

    # electricity_income_statement eis
    # "=投資試算表!$H$5*ROUND($H$6*$H$3*365*$G13,0)"
    # =投資試算表!$H$5*ROUND($H$6*$H$3*365*$G14,0)
    _lds_1, _lds_2, _lds_3, _lds_4, _lds_5, _lds_6, _lds_7, _lds_8, _lds_9, _lds_10, \
        _lds_11, _lds_12, _lds_13, _lds_14, _lds_15, _lds_16, _lds_17, _lds_18, _lds_19, _lds_20,\
        _lds_sum = list(
            map(feature_fuc.result, [lds_1, lds_2, lds_3, lds_4, lds_5, lds_6, lds_7, lds_8, lds_9, lds_10,
                                     lds_11, lds_12, lds_13, lds_14, lds_15, lds_16, lds_17, lds_18, lds_19, lds_20,
                                     lds_sum]))

    _cdp_1, _cdp_2, _cdp_3, _cdp_4, _cdp_5, _cdp_sum = list(map(
        feature_fuc.result, [cdp_1, cdp_2, cdp_3, cdp_4, cdp_5, cdp_sum]))

    _warranty_1, _warranty_2, _warranty_3, _warranty_4, _warranty_5, _warranty_6, _warranty_7, _warranty_8, _warranty_9, _warranty_10, \
        _warranty_11, _warranty_12, _warranty_13, _warranty_14, _warranty_15, _warranty_16, _warranty_17, _warranty_18, _warranty_19, _warranty_20, \
        _warranty_sum = list(
            map(feature_fuc.result, [warranty_1, warranty_2, warranty_3, warranty_4, warranty_5, warranty_6, warranty_7, warranty_8, warranty_9, warranty_10,
                                     warranty_11, warranty_12, warranty_13, warranty_14, warranty_15, warranty_16, warranty_17, warranty_18, warranty_19, warranty_20,
                                     warranty_sum]))

    _oe_1, _oe_2, _oe_3, _oe_4, _oe_5, _oe_6, _oe_7, _oe_8, _oe_9, _oe_10,\
        _oe_11, _oe_12, _oe_13, _oe_14, _oe_15, _oe_16, _oe_17, _oe_18, _oe_19, _oe_20, _oe_sum = list(
            map(feature_fuc.result, [oe_1, oe_2, oe_3, oe_4, oe_5, oe_6, oe_7, oe_8, oe_9, oe_10,
                                     oe_11, oe_12, oe_13, oe_14, oe_15, oe_16, oe_17, oe_18, oe_19, oe_20,
                                     oe_sum]))

    _total_r_0, _total_r_1, _total_r_2, _total_r_3, _total_r_4, _total_r_5, _total_r_6, _total_r_7, _total_r_8, _total_r_9, _total_r_10, \
        _total_r_11, _total_r_12, _total_r_13, _total_r_14, _total_r_15, _total_r_16, _total_r_17, _total_r_18, _total_r_19, _total_r_20,  _total_r_sum = \
        list(
            map(feature_fuc.result, [total_r_0, total_r_1, total_r_2, total_r_3, total_r_4, total_r_5, total_r_6, total_r_7, total_r_8, total_r_9, total_r_10,
                                     total_r_11, total_r_12, total_r_13, total_r_14, total_r_15, _otal_r_16, total_r_17, total_r_18, total_r_19, total_r_20,  total_r_sum]))

    _cash_flow_0, _cash_flow_1, _cash_flow_2, _cash_flow_3, _cash_flow_4, _cash_flow_5, _cash_flow_6, _cash_flow_7, _cash_flow_8, _cash_flow_9, _cash_flow_10, \
        _cash_flow_11, _cash_flow_12, _cash_flow_13, _cash_flow_14, _cash_flow_15, _cash_flow_16, _cash_flow_17, _cash_flow_18, _cash_flow_19, _cash_flow_20 = \
        list(map(feature_fuc.result, [cash_flow_0, cash_flow_1, cash_flow_2, cash_flow_3, cash_flow_4, cash_flow_5, cash_flow_6, cash_flow_7, cash_flow_8, cash_flow_9, cash_flow_10,
                                      cash_flow_11, cash_flow_12, cash_flow_13, cash_flow_14, cash_flow_15, cash_flow_16, cash_flow_17, cash_flow_18, cash_flow_19, cash_flow_20]))
    return_on_investment_df = pd.DataFrame(
        {
            "年度": [*list(range(0, 21)), "合計", "平均"],

            # estimated_system_efficiency ese
            "預估系統效率": ["-", _ese_1, _ese_2, _ese_3, _ese_4, _ese_5, _ese_6, _ese_7, _ese_8, _ese_9, _ese_10, \
                       _ese_11, _ese_12, _ese_13, _ese_14, _ese_15, _ese_16, _ese_17, _ese_18, _ese_19, _ese_20, \
                       _ese_sum, _ese_average],

            # electricity_income_statement eis
            "電費收入表": ["-", _eis_1, _eis_2, _eis_3, _eis_4, _eis_5, _eis_6, _eis_7, _eis_8, _eis_9, _eis_10, \
                      _eis_11, _eis_12, _eis_13, _eis_14, _eis_15, _eis_16, _eis_17, _eis_18, _eis_19, _eis_20, \
                      _eis_sum, _eis_average],

            # loan_disbursement_statement lds
            "貸款支出表": ["-", _lds_1, _lds_2, _lds_3, _lds_4, _lds_5, _lds_6, _lds_7, _lds_8, _lds_9, _lds_10, \
                      _lds_11, _lds_12, _lds_13, _lds_14, _lds_15, _lds_16, _lds_17, _lds_18, _lds_19, _lds_20, \
                      _lds_sum, "-"],

            # customer_discount_program cdp
            "客戶優惠專案": ["-", _cdp_1, _cdp_2, _cdp_3, _cdp_4, _cdp_5, "-", "-", "-", "-", "-", "-", \
                       "-", "-", "-", "-", "-", "-", "-", "-", "-", _cdp_sum, "-"],

            # warranty_fee warranty
            "保固費用": ["-", _warranty_1, _warranty_2, _warranty_3, _warranty_4, _warranty_5, _warranty_6, _warranty_7, _warranty_8, _warranty_9, _warranty_10, \
                     _warranty_11, _warranty_12, _warranty_13, _warranty_14, _warranty_15, _warranty_16, _warranty_17, _warranty_18, _warranty_19, _warranty_20, _warranty_sum, "-"],

            # operating_expenses oe
            "營運費用": ["-", _oe_1, _oe_2, _oe_3, _oe_4, _oe_5, _oe_6, _oe_7, _oe_8, _oe_9, _oe_10,
                     _oe_11, _oe_12, _oe_13, _oe_14, _oe_15, _oe_16, _oe_17, _oe_18, _oe_19, _oe_20, _oe_sum, "-"],

            # total_return_on_investment total_r
            "合計表": [_total_r_0, _total_r_1, _total_r_2, _total_r_3, _total_r_4, _total_r_5, _total_r_6, _total_r_7, _total_r_8, _total_r_9, _total_r_10,
                    _total_r_11, _total_r_12, _total_r_13, _total_r_14, _total_r_15, _total_r_16, _total_r_17, _total_r_18, _total_r_19, _total_r_20,  _total_r_sum, "-"],

            # cash_flow
            "現金流": [_cash_flow_0, _cash_flow_1, _cash_flow_2, _cash_flow_3, _cash_flow_4, _cash_flow_5, _cash_flow_6, _cash_flow_7, _cash_flow_8, _cash_flow_9, _cash_flow_10,
                    _cash_flow_11, _cash_flow_12, _cash_flow_13, _cash_flow_14, _cash_flow_15, _cash_flow_16, _cash_flow_17, _cash_flow_18, _cash_flow_19, _cash_flow_20, "-", "-"],
        }
    )
    return return_on_investment_df

# table = dbc.Table.from_dataframe(
#     df,
#     striped=True,
#     bordered=True,
#     hover=True,
#     )

# table_header = [
#     html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
# ]

# row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
# row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
# row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
# row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

# table_body = [html.Tbody([row1, row2, row3, row4])]

# table1 = dbc.Table(
#     # using the same table as in the above example
#     table_header + table_body,
#     bordered=True,
#     dark=True,
#     hover=True,
#     # responsive=True,
#     # striped=True,
#     # color="dark",
# )
