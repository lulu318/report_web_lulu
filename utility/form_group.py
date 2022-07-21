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
from utility.table import df

table = feature_fuc.table_dataframe(df)

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
                                        form_func.dropdown_items_label_name_period("annual_wholesale_rate", [year_list, [
                                            1, 2]], "躉購費率年度↓", ["#4682B4", "#4682B4"]),
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
                                    [form_func.modal_table("工程費用說明", "header", df), table],
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
