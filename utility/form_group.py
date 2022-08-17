import imp
from turtle import width
import dash
from datetime import datetime as dt
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import datetime

from pyparsing import White
from utility.utils import form_func, year_list, feature_fuc
from utility.table import project_costs_df, customer_offers_df, warranty_cost_df, operating_expense_df, wholesale_rate_df, return_on_investment_df

# table1 = feature_fuc.table_dataframe(customer_offers_df)
# table = feature_fuc.table_dataframe(project_costs_df("tax_free_construction_costs_output"))


def get_date():
    # Function to check for dynamic date change, for testing purpose only
    import random
    change = random.randint(1, 20)
    return (datetime.datetime.today() - datetime.timedelta(change)).date()


formGroup = html.Div(
    dbc.Card(
        dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    [
                        html.H5("系統條件"),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        form_func.input_frame_label_name(
                                            "案名", "case_name_row", type_="text"),
                                        form_func.input_frame_label_name(
                                            "預估等效日照小時", "estimated_sunshine", "hr"),
                                        form_func.input_frame_label_name(
                                            "系統容量", "system_capacity", "kW"),
                                        form_func.input_frame_label_name(
                                            "未稅建造費用", "construction_cost", "NT$/kW"),
                                        form_func.input_frame_label_name(
                                            "其他費用", "other_costs", "NT$/kW"),
                                        form_func.input_frame_label_name(
                                            "年租金", "annual_rent", "%"),
                                        form_func.input_frame_label_name(
                                            "預估初年系統PR值", "estimated_first_year_system", "%"),
                                        form_func.radio_items_label_name("期末是否拆除↓", "whether_to_remove", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.input_frame_label_name(
                                            "拆除費用", "demolition_cost", "NT$/kW"),
                                        form_func.input_frame_label_name(
                                            "PR年遞減率", "pr_annual_decline_rate", "%"),
                                        form_func.input_frame_label_name(
                                            "保固費年遞增率", "warranty_annual_increment_rate", "%"),
                                        form_func.dropdown_items_label_name_period("estimated_calendar_year", [year_list, [
                                            1, 2]], "預估掛表年度", ["#4682B4", "#4682B4"])
                                    ],
                                    className="mb-3",
                                ),
                            ],
                            className='m-3',

                        ),
                    ],
                    className='m-4',
                ),
                dbc.ListGroupItem(
                    [
                        html.H5("融資條件"),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        form_func.input_frame_label_name(
                                            "客戶優惠專案", "customer_offers", "%"),
                                        form_func.dropdown_items_label_name(
                                            "program_type", ["自付，貸款", "自付，無貸款", "免出資"], "方案類型↓", "#4682B4"),
                                        form_func.dropdown_items_label_name(
                                            "repayment_type", ["本利平均攤還", "本金平均攤還"], "還款類型↓", "#4682B4"),
                                        form_func.input_frame_label_name(
                                            "銀行貸款成數", "bank_loan_ratio", "%"),
                                        form_func.input_frame_label_name(
                                            "銀行貸款利率", "bank_loan_rate", "%"),
                                        form_func.input_frame_label_name(
                                            "銀行貸款年限", "bank_loan_term", "年"),
                                    ],
                                    className="mb-3",
                                ),
                            ],
                            className='m-3',

                        ),
                    ], className='m-4',
                ),
                dbc.ListGroupItem(
                    [
                        html.H5("費率條件"),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                feature_fuc.label_name(
                                                    "躉購費率年度↓", "annual_wholesale_rate"),
                                                dbc.Row([
                                                    feature_fuc.dropdown_item(
                                                        "annual_wholesale_rate_year", year_list, "#4682B4"),
                                                    dbc.InputGroupText("年"),
                                                    feature_fuc.dropdown_item(
                                                        "annual_wholesale_rate_period", [1, 2],"#4682B4"),
                                                    dbc.InputGroupText("期"), ])

                                            ],
                                            width=3
                                        ),
                                        # form_func.dropdown_items_label_name_period("annual_wholesale_rate", [year_list, [
                                        #     1, 2]], "躉購費率年度↓", ["#4682B4", "#4682B4"]),
                                        form_func.input_frame_label_name(
                                            "隔年費率降幅預估", "estimated_rate_reduction_next_year", "%"),
                                        form_func.dropdown_items_label_name(
                                            "shape", ["屋頂型", "地面型", "水面型"], "形式↓", "#4682B4"),
                                        form_func.dropdown_items_label_name(
                                            "area", ["北部地區", "中南部地區", "台東"], "地區↓", "#4682B4"),
                                        # dbc.InputGroupText(id="area_output")
                                        form_func.label_name_text(
                                            "regional_bonus", "地區加成％數", "area_output", "%"),
                                        form_func.input_frame_label_name(
                                            "模組回收基金", "module_recycling_fund"),
                                        form_func.radio_items_label_name("高效能加成↓", "high_efficiency_bonus", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.radio_items_label_name("併聯特高壓昇壓站↓", "parallel_uhv_booster_station", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.radio_items_label_name("原住民↓", "aboriginal", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.radio_items_label_name("漁業環境", "fishing_environment", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.radio_items_label_name("農/漁結合綠能↓", "agriculture_fishing_green_energy", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.radio_items_label_name("高速公路服務區停車場↓", "expressway_service_parking_lot", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.radio_items_label_name("風雨球場↓", "wind_rain_course", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.radio_items_label_name("風雨球場+浪板↓", "wind_rain_course_wave_board", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.input_frame_label_name(
                                            "已安裝KW數", "installed_kw", "KW"),
                                        form_func.radio_items_label_name("電業費率↓", "electricity_rates", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.dropdown_items_label_name(
                                            "roof_type_parallel_connection_method", ["高壓", "低壓"], "屋頂型併接方式↓", "#4682B4"),
                                        form_func.radio_items_label_name("屋頂型併網工程費", "roof_type_grid_connection_engineering", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        form_func.dropdown_items_label_name(
                                            "strengthen_power_grid", ["輸電級", "配電級", "否"], "加強電力網↓", "#4682B4"),
                                        form_func.dropdown_items_label_name(
                                            "gis_booster_station_form", ["屋內", "戶外", "否"], "GIS昇壓站形式↓", "#4682B4"),
                                        form_func.input_frame_label_name(
                                            "輸電線路長度", "transmission_line_length", "km"),
                                        form_func.dropdown_items_label_name(
                                            "transmission_line_form", ["架空", "地下電纜"], "輸電線路形式", "#4682B4"),

                                    ],
                                    className="mb-3",
                                ),
                            ],
                            className='m-3',

                        ),
                    ], className='m-4',
                ),
                dbc.ListGroupItem(
                    [
                        dbc.Alert([html.H5("投資報酬分析")], color="primary"),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        # html.Div(
                                        #     id='shape_output'),
                                        # html.H5('aaaa'),
                                        form_func.modal_table(
                                            "project_costs", "工程費用說明", "工程費用說明",  project_costs_df(
                                                "bank_loan_fee_percent_output", "actual_expenses_percent_output", "customer_discount_program_percent_output", "bank_loan_percent_output",
                                                "loan_annual_interest_rate_percent_output", "loan_term_percent_output", "loan_fee_percent_output", "pay_after_loan_percent_output",

                                                "tax_free_construction_costs_output", "bank_loan_fee_costs_output", "actual_expenses_costs_output", "total_project_costs_output",
                                                "actual_total_expenses_costs_output", 'customer_discount_program_costs_output', 'bank_loan_costs_output', "annual_loan_repayment_amount_costs_output",
                                                "taipower_line_subsidy_costs_output", "loan_fee_costs_output", "pay_after_loan_costs_output")),
                                        form_func.modal_table(
                                            "customer_offers", "客戶優惠專案", "客戶優惠專案", customer_offers_df("customer_offers_costs_output")),
                                        form_func.modal_table(
                                            "warranty_cost", "保固費用分析", "保固費用分析", warranty_cost_df("illustrate_7years_output", "illustrate_20years_output", "scale_7years_output", "scale_20years_output",
                                                                                                  "amount_6years_output", "amount_7years_output", "amount_20years_output", "amount_total_output")),
                                        form_func.modal_table(
                                            "operating_expense", "營運費用分析", "營運費用分析", operating_expense_df("illustrate_cleaning_fee_water_output", "illustrate_property_insurance_costs_output",
                                                                                                          "scale_cleaning_fee_water_output", "scale_property_insurance_costs_output", "scale_installation_space_cost_output", "scale_module_recycling_fund_output", "scale_removal_fee_output",
                                                                                                          "amount_cleaning_fee_water_output", "amount_property_insurance_costs_output", "amount_installation_space_cost_output", "amount_operating_expense_total_output", "amount_module_recycling_fund_output", "amount_removal_fee_output")),
                                        form_func.modal_table(
                                            "wholesale_rate", "躉售費率", "躉售費率", wholesale_rate_df()),
                                        form_func.modal_table(
                                            "return_on_investment", "投資報酬分析表", "投資報酬分析表", return_on_investment_df(*[f"ese_{num}_output" for num in range(1, 21)], "ese_sum", "ese_average",
                                                                                                                  *[f"eis_{num}_output" for num in range(1, 21)], "eis_sum", "eis_average",
                                                                                                                  *[f"lds_{num}_output" for num in range(1, 21)], "lds_sum", "lds_average")),

                                        # form_func.modal_table(
                                        # "return_on_investment", "投資報酬分析表", "投資報酬分析表", return_on_investment_df("ese_1_output", "ese_2_output", "ese_3_output", "ese_4_output", "ese_5_output", "ese_6_output", "ese_7_output", "ese_8_output", "ese_9_output", "ese_10_output",
                                        #                                                                       "ese_11_output", "ese_12_output", "ese_13_output", "ese_14_output", "ese_15_output", "ese_16_output", "ese_17_output", "ese_18_output", "ese_19_output", "ese_20_output", "ese_sum_output", "ese_average_output")),

                                        # feature_fuc.table_dataframe(
                                        #     project_costs_df(
                                        #         "bank_loan_fee_percent_output", "actual_expenses_percent_output", "customer_discount_program_percent_output", "bank_loan_percent_output",
                                        #         "loan_annual_interest_rate_percent_output", "loan_term_percent_output", "loan_fee_percent_output", "pay_after_loan_percent_output",

                                        #         "tax_free_construction_costs_output", "bank_loan_fee_costs_output", "actual_expenses_costs_output", "total_project_costs_output",
                                        #         "actual_total_expenses_costs_output", 'customer_discount_program_costs_output', 'bank_loan_costs_output', "annual_loan_repayment_amount_costs_output",
                                        #         "taipower_line_subsidy_costs_output", "loan_fee_costs_output", "pay_after_loan_costs_output")
                                        # ),
                                        # html.H5('aaaa'),
                                        # feature_fuc.result("bank_loan_costs_output")
                                    ],
                                    className="m-3",)
                            ]
                        )
                    ]
                )
            ],
            flush=True,
        ),
        className="w-100",  # 0 - 100
    ),
)
