from enum import auto
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import datetime

year_list = [i for i in range(109, int(datetime.datetime.today().year)-1911+3)]


class feature_fuc:
    def result(value_id):
        res = html.H5(id=value_id)
        return res


    @staticmethod
    def judge_is_none(value):
        if value is None:
            value = 0
        return value

    @staticmethod
    def radio_items(_id, _options: list):
        items = dbc.RadioItems(
            options=_options,
            value=1,
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
    @staticmethod
    def regional_bonus(area):
        bonus = 0
        if area == "北部地區":
            bonus = 15
        elif area == "台東":
            bonus = 8
        return bonus

    @staticmethod
    def tax_free_construction_costs(construction, other):
        construction = feature_fuc.judge_is_none(construction)
        other = feature_fuc.judge_is_none(other)
        res = construction+other
        return res

    
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

    @staticmethod
    def customer_discount_program_percent(customer_offers):
        customer_offers = feature_fuc.judge_is_none(customer_offers)
        return customer_offers

    @staticmethod
    def actual_expenses_percent(program_type, bank_loan_ratio):
        program_type = feature_fuc.judge_is_none(program_type)
        bank_loan_ratio = feature_fuc.judge_is_none(bank_loan_ratio)
        res = 100 - callback_fuc.bank_loan_percent(program_type, bank_loan_ratio)
        return res

