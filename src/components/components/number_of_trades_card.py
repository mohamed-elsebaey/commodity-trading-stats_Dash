from dash import html, dcc, callback, Output, Input

import plotly.express as px
from dash_iconify import DashIconify

from components.GetData import GetData

df = GetData()


def number_of_trades_card():
    return (
        html.Div(
            className="number-of-trades",
            children=[
                html.Div(
                    className="pageTitle",
                    children=[
                        DashIconify(
                            icon="mdi:chart-areaspline",
                            width=30,
                            color="#000000",
                        ),
                        html.H2("Number of Trades"),
                    ],
                ),
                html.Div(
                    className="number-of-trades-options-section",
                    children=[
                        html.Div(
                            [
                                html.Label("Country"),
                                dcc.Dropdown(
                                    id="number-of-trades-country-dropdown",
                                    options=[
                                        {
                                            "label": country,
                                            "value": country,
                                        }
                                        for country in df["country_or_area"]
                                        .unique()
                                        .tolist()
                                    ],
                                    value="Argentina",
                                ),
                            ],
                            style={
                                "width": "30%",
                                "min-width": "200px",
                            },
                        ),
                        html.Div(
                            [
                                html.Label("Category"),
                                dcc.Dropdown(
                                    id="number-of-trades-category-dropdown",
                                    options=[
                                        {
                                            "label": "All Categories",
                                            "value": "All Categories",
                                        }
                                    ]
                                    + [
                                        {
                                            "label": category,
                                            "value": category,
                                        }
                                        for category in df["category"].unique().tolist()
                                    ],
                                    value="All Categories",
                                ),
                            ],
                            style={
                                "width": "30%",
                                "min-width": "200px",
                            },
                        ),
                        html.Div(
                            [
                                html.Label("Chart Type"),
                                dcc.RadioItems(
                                    id="number-of-trades-chart-type",
                                    options=[
                                        {
                                            "label": "Area Chart",
                                            "value": "area",
                                        },
                                        {
                                            "label": "Line Chart",
                                            "value": "line",
                                        },
                                    ],
                                    value="area",
                                    style={
                                        "display": "flex",
                                        "gap": "10px",
                                    },
                                ),
                            ],
                            style={
                                "width": "30%",
                                "min-width": "200px",
                            },
                        ),
                    ],
                ),
                dcc.Loading(
                    dcc.Graph(id="number-of-trades-chart-output"),
                ),
            ],
        ),
    )


@callback(
    Output("number-of-trades-chart-output", "figure"),
    Input("number-of-trades-country-dropdown", "value"),
    Input("number-of-trades-category-dropdown", "value"),
    Input("number-of-trades-chart-type", "value"),
)
def update_chart(country, category, chart_type):
    if country == None:
        country = "Egypt"
    if category == None:
        category = "All Categories"

    filtered_df = df[df["country_or_area"] == country]

    if category != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == category]

    trades_per_year = (
        filtered_df.groupby(["year", "flow"])
        .size()
        .reset_index(name="Number of Trades")
    )

    if chart_type == "area":
        fig = px.area(
            trades_per_year,
            x="year",
            y="Number of Trades",
            color="flow",
            color_discrete_map={
                "Import": "#FFA500",
                "Export": "#4169E1",
            },
        )
    else:
        fig = px.line(
            trades_per_year,
            x="year",
            y="Number of Trades",
            color="flow",
            color_discrete_map={
                "Import": "#FFA500",
                "Export": "#4169E1",
            },
        )

    fig.update_traces(
        hovertemplate="(%{x}, %{y})",
        line=dict(width=2),
        # this is show points in lines
        # mode="lines+markers",
    )

    fig.update_layout(
        # hovermode="x unified",
        xaxis_title="Years",
        yaxis_title="Number of Trades",
        legend_title="Flow Type",
        template="simple_white",
        height=350,
        # legend=dict(
        #     orientation="h",
        #     yanchor="bottom",
        #     y=1.02,
        #     xanchor="right",
        #     x=1,
        # ),
        # margin=dict(l=40, r=40, t=40, b=40),
    )

    return fig
