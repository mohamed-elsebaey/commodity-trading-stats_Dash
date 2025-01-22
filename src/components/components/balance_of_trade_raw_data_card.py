from dash import html, dcc, callback, Output, Input, State, dash_table
from dash_iconify import DashIconify

import pandas as pd
import io

from components.GetData import GetData

df = GetData()

trades_wide = (
    df.groupby(["country_or_area", "year", "flow"])["trade_usd"]
    .sum()
    .reset_index(name="Total Trade Value (USD)")
)

trades_wide = (
    trades_wide.pivot(
        index=["country_or_area", "year"],
        columns="flow",
        values="Total Trade Value (USD)",
    )
    .fillna(0)
    .reset_index()
)

trades_wide["Balance of Trade (USD)"] = trades_wide.get("Export", 0) - trades_wide.get(
    "Import", 0
)

trades_wide = trades_wide[["country_or_area", "year", "Balance of Trade (USD)"]]


def balance_of_trade_raw_data_card():
    return html.Div(
        className="balance-of-trade-raw-data",
        children=[
            html.Div(
                className="pageTitle",
                children=[
                    DashIconify(
                        icon="material-symbols:content-copy",
                        width=30,
                        color="#000000",
                    ),
                    html.H2("Balance of Trade Raw Data"),
                ],
            ),
            html.Div(
                children=[
                    html.Button(
                        children=[
                            DashIconify(
                                icon="material-symbols:download-rounded",
                                width=25,
                                color="#0096eb",
                            ),
                            "Export to Excel",
                        ],
                        id="download-button",
                    ),
                    dcc.Download(id="download-dataframe-xlsx"),
                ],
            ),
            dash_table.DataTable(
                id="balance-table",
                columns=[
                    {
                        "name": "Country or Area",
                        "id": "country_or_area",
                        "type": "text",
                        "editable": False,
                    },
                    {
                        "name": "Year",
                        "id": "year",
                        "type": "numeric",
                        "editable": False,
                    },
                    {
                        "name": "Balance of Trade (USD)",
                        "id": "Balance of Trade (USD)",
                        "type": "numeric",
                        "editable": False,
                    },
                ],
                data=trades_wide.to_dict("records"),
                filter_action="native",
                style_table={
                    "border": "1px solid black",
                    "overflowX": "auto",
                    "minWidth": "100%",
                },
                style_cell={
                    "textAlign": "center",
                    "padding": "5px",
                    "fontFamily": "Arial",
                    "fontSize": "12px",
                    "border": "1px solid black",
                    "width": "33.33%",
                    "maxWidth": "33.33%",
                    "minWidth": "33.33%",
                },
                style_header={
                    "backgroundColor": "#007BFF",
                    "color": "white",
                    "fontWeight": "bold",
                    "fontSize": "14px",
                    "textAlign": "center",
                    "border": "1px solid black",
                },
                style_data={
                    "border": "1px solid black",
                },
                style_data_conditional=[
                    {
                        "if": {
                            "column_id": "Balance of Trade (USD)",
                            "filter_query": "{Balance of Trade (USD)} < 0",
                        },
                        "backgroundColor": "#FFC0CB",
                        "color": "black",
                    },
                ],
                page_size=6,
            ),
        ],
    )


@callback(
    Output("download-dataframe-xlsx", "data"),
    Input("download-button", "n_clicks"),
    State("balance-table", "derived_virtual_data"),
    prevent_initial_call=True,
)
def download_excel(n_clicks, filtered_data):
    if filtered_data is None:
        filtered_data = []
    filtered_df = pd.DataFrame(filtered_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        filtered_df.to_excel(writer, index=False, sheet_name="Sheet1")
    output.seek(0)

    return dcc.send_bytes(output.getvalue(), "Balance_of_Trade.xlsx")
