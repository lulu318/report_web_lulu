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

project_costs_df = pd.DataFrame(
    {
        "項目": ["未稅建造費用(NT$/kW)", "銀行核貸費用(NT$/kW)", "實際支出費用(NT$/kW)", "工程總支出費用(NT$)",
               "實際總支出費用(NT$)", "客戶優惠專案", "銀行貸款", "貸款年利率(%)",
               "貸款年限", "貸款每年還款金額", "台電線路補助費(預估值)", "貸款手續費",
               "貸款後自付總費用(NT$)", "宣鼎開發費"],

        "說明": ["建造費用", "", "", "",
               "", "", "貸款成數", "",
               "", "本利攤還", "由台電收取", "",
               "", ""],

        "比例": ["100%", "C10", "C4-C5", "",
               "", "=資料輸入!D19",
               '=IF(資料輸入!D20="自付，貸款",資料輸入!D22,IF(資料輸入!D20="免出資",1,0))', '=IF(資料輸入!D20="自付，無貸款",0,資料輸入!D23)',
               "=IF(C10=0,0,資料輸入!D24)", "", "", '=IF(資料輸入!D20="自付，貸款",1%,0)',
               '=IF(資料輸入!D20="免出資",0,C4-C9-C10)', ""],

        "金額": ["=資料輸入!D7+資料輸入!D8", "=D4*C5", "=D4-D5", "=ROUND(D4*H3,0)",
               "=ROUND(D6*H3,0)", "=ROUND(D4*H3*C9,0)", "=ROUND((D4)*$C10*H$3,0)", "",
               "", '=IF(資料輸入!D20="自付，貸款",ROUND(PMT($C11/12,C12*12,D10,0,0)*12,0),0)',
               '=IF(資料輸入!I5="屋頂型",IF(資料輸入!I19="低壓",資料輸入!R52,IF(資料輸入!I19="高壓",資料輸入!Q52,0)),資料輸入!S52)', "=ROUND(D10*C15,0)",
               "=D8+D14-D9+D15+D17", ""],
    }
)

customer_offers_df = pd.DataFrame(
    {
        "項目": ["每年還款金額"],

        "說明": ["分期5年"],

        "比例": ["-"],

        "金額": ["=ROUND(D9/5,0)"],
    }
)

warranty_cost_df = pd.DataFrame(
    {
        "項目": ["預估1~5年每年維護費用", "預估第6年維護費用", "預估第7年維護費用","...",
        "預估第20年維護費用", "合計"],

        "說明": ['="售電收入"&C24*100&"%"', '="售電收入"&C25*100&"%"', '="售電收入"&C26*100&"%"', "...",
        '="售電收入"&C28*100&"%"', ""],

        "比例": ["0%", "6%", '=C25+資料輸入!D15', '...',
        "=C25+資料輸入!D15*14", ""],

        "金額": ["0", '=-K18', '=-K19',"...",
        "=-K32", "=-K33"],
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
