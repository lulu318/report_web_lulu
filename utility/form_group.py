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
from utility.utils import email_input, password_input, label_name, input_frame, input_frame_label_name, radio_items_label_name, radio_items, dropdown_items_label_name_period, year_list


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
                                        input_frame_label_name(
                                            "案名", "case_name_row", __type="text"),
                                        input_frame_label_name(
                                            "預估等效日照小時", "estimated_sunshine", "hr"),
                                        input_frame_label_name(
                                            "系統容量", "system_capacity", "kW"),
                                        input_frame_label_name(
                                            "未稅建造費用", "construction_cost", "NT$/kW"),
                                        input_frame_label_name(
                                            "其他費用", "other_costs", "NT$/kW"),
                                        input_frame_label_name(
                                            "年租金", "annual_rent", "%"),
                                        input_frame_label_name(
                                            "預估初年系統PR值", "estimated_first_year_system", "%"),
                                        radio_items_label_name("期末是否拆除↓", "whether_to_remove", [
                                            {"label": "是", "value": 1}, {"label": "否", "value": 2}]),
                                        input_frame_label_name(
                                            "拆除費用", "demolition_cost", "NT$/kW"),
                                        input_frame_label_name(
                                            "PR年遞減率", "pr_annual_decline_rate", "%"),
                                        input_frame_label_name(
                                            "保固費年遞增率", "warranty_annual_increment_rate", "%"),
                                        dropdown_items_label_name_period("estimated_calendar_year", [year_list, [1,2]], "預估掛表年度", ["#4682B4", "#4682B4"])
                                    ],
                                    className="mb-3",
                                ),
                            ],
                            className='m-3',

                        ),
                        html.Div(id='case_name_row_output'),
                    ],
                    className='m-4',
                ),
                dbc.ListGroupItem(
                    [
                        html.H5("融資條件"),
                        dbc.Form(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Email", html_for="example-email-row"),
                                            email_input,
                                        ],
                                        width=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Password", html_for="example-password-row"),
                                            password_input,
                                        ],
                                        width=6,
                                    )

                                ],
                                className="mb-3",
                            ),
                            className='m-3',
                        ),
                    ], className='m-4',
                ),
                dbc.ListGroupItem(
                    [
                        html.H5("費率條件"),
                        dbc.Form(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Email", html_for="example-email-row"),
                                            email_input,
                                        ],
                                        width=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Password", html_for="example-password-row"),
                                            password_input,
                                        ],
                                        width=6,
                                    )

                                ],
                                className="mb-3",
                            ),
                            className='m-3',
                        ),
                    ], className='m-4',
                ),
                dbc.ListGroupItem(
                    [
                        html.H5("地面型"),
                        dbc.Form(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Email", html_for="example-email-row"),
                                            email_input,
                                        ],
                                        width=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label(
                                                "Password", html_for="example-password-row"),
                                            password_input,
                                        ],
                                        width=6,
                                    )

                                ],
                                className="mb-3",
                            ),
                            className='m-3',
                        ),
                    ], className='m-4',
                ),
            ],
            flush=True,
        ),
        className="w-100",  # 0 - 100
    ),
)
