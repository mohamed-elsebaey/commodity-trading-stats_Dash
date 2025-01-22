from dash import html, dcc, callback, Output, Input

import plotly.express as px
from dash_iconify import DashIconify

from components.GetData import GetData

df = GetData()


def balance_of_trades_card():
    return (
        html.Div(
            className="balance-of-trades",
            children=[
                html.Div(
                    className="pageTitle",
                    children=[
                        DashIconify(
                            icon="material-symbols:balance-sharp",
                            width=30,
                            color="#000000",
                        ),
                        html.H2("Balance of Trades (exports-imports)"),
                    ],
                ),
                html.Div(
                    [
                        html.Label("Country"),
                        dcc.Dropdown(
                            id="balance-of-trades-country-dropdown",
                            options=[
                                {
                                    "label": country,
                                    "value": country,
                                }
                                for country in df["country_or_area"].unique().tolist()
                            ],
                            value="Algeria",
                        ),
                    ],
                    style={
                        "width": "30%",
                        "min-width": "250px",
                    },
                ),
                dcc.Loading(
                    dcc.Graph(id="balance-of-trades-chart-output"),
                ),
            ],
        ),
    )


@callback(
    Output("balance-of-trades-chart-output", "figure"),
    Input("balance-of-trades-country-dropdown", "value"),
)
def update_chart(country):
    if country == None:
        country = "Egypt"

    filtered_df = df[df["country_or_area"] == country]

    trades_per_year = (
        filtered_df.groupby(["year", "flow"])["trade_usd"]
        .sum()
        .reset_index(name="Total Trade Value (USD)")
    )

    trades_wide = trades_per_year.pivot(
        index="year", columns="flow", values="Total Trade Value (USD)"
    ).fillna(0)

    trades_wide["Balance"] = trades_wide.get("Export", 0) - trades_wide.get("Import", 0)
    trades_wide = trades_wide.reset_index()
    
    fig = px.line(
        trades_wide,
        x="year",
        y="Balance",
    )

    fig.update_traces(
        hovertemplate="(%{x}, %{y})",
        line=dict(width=2),
        # this is show points in lines
        # mode="lines+markers",
    )

    fig.update_layout(
        xaxis_title="Years",
        yaxis_title="Balance of Trades (USD)",
        template="simple_white",
        height=350,
    )

    return fig
