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

email_input = dbc.Input(
    type="email",
    placeholder="Enter email"
)

password_input = dbc.Input(
    type="password",
    placeholder="Enter password",
)


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


def group_text(frame, text):
    text = dbc.InputGroup([frame, text])
    return text


def input_frame(_id, _placeholder="Type something...", _type="number", **kwargs):
    frame = dbc.Input(id=_id, placeholder=_placeholder, type=_type, **kwargs)
    return frame


def label_name(label_text, _html_for, **kwargs):
    label = dbc.Label(label_text, html_for=_html_for, **kwargs)
    return label


def dropdown_item(_id, items: list, color):
    dropdown = dcc.Dropdown(
        items, items[0], id=_id, style={
            "background": color,
        })
    return dropdown


def input_frame_label_name(label_text, _id, unit=None, _width=3, __type="number"):
    if unit:
        _group = group_text(
            input_frame(_id, _type=__type),
            dbc.InputGroupText(unit)
        )
    else:
        _group = input_frame(_id, _type=__type)
    col = dbc.Col(
        [
            label_name(
                label_text, _id),
            _group
        ],
        width=_width,
        className="mb-4",
    )
    return col


def radio_items_label_name(label_text, _id, _options: list):
    col = dbc.Col(
        [
            label_name(label_text, _id),
            radio_items(_id, _options),
        ],
        width=3
    )
    return col


def dropdown_items_label_name_period(_id, items: list, label_text, color: list):
    col = dbc.Col(
        [
            label_name(label_text, _id),
            dbc.Row([dropdown_item(f"{_id}_year", items[0], color[0] ),dbc.InputGroupText("年"),
                     dropdown_item(f"{_id}_period", items[1], color[1]),dbc.InputGroupText("期"), ])

        ],
        width=3
    )
    return col
