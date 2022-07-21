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

df = pd.DataFrame(
    {
        "項目": ["未稅建造費用(NT$/kW)", "銀行核貸費用(NT$/kW)", "實際支出費用(NT$/kW)", "工程總支出費用(NT$)"],
        "說明": ["建造費用", "", "", ""],
        "比例": ["100%", "C10", "C4-C5", ""],
        "金額": ["=資料輸入!D7+資料輸入!D8", "=D4*C5", "=D4-D5", "=ROUND(D4*=資料輸入!D6,0)"],
    }
)

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
