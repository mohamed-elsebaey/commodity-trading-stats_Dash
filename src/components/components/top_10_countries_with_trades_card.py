from dash import html, dcc, callback, Output, Input, callback_context
from dash_iconify import DashIconify
import plotly.express as px

from components.GetData import GetData

df = GetData()


def top_10_countries_with_trades_card():
    return html.Div(
        className="top_10_countries_with_trades",
        children=[
            html.Div(
                className="pageTitle",
                children=[
                    DashIconify(
                        icon="material-symbols:chart-data-sharp",
                        width=30,
                        color="#000000",
                    ),
                    html.H2("Top 10 Countries with Trades"),
                ],
            ),
            html.Div(
                [
                    html.Button(
                        [
                            DashIconify(
                                icon="mdi-light:check",
                                width=18,
                                color="#007bff",
                                className="button-icon",
                            ),
                            "Exports",
                        ],
                        id="Export",
                        className="button selected",
                    ),
                    html.Button(
                        [
                            DashIconify(
                                icon="mdi-light:check",
                                width=18,
                                color="#007bff",
                                className="button-icon",
                            ),
                            "Imports",
                        ],
                        id="Import",
                        className="button",
                    ),
                    html.Button(
                        [
                            DashIconify(
                                icon="mdi-light:check",
                                width=18,
                                color="#007bff",
                                className="button-icon",
                            ),
                            "Re-Exports",
                        ],
                        id="Re-Export",
                        className="button",
                    ),
                    html.Button(
                        [
                            DashIconify(
                                icon="mdi-light:check",
                                width=18,
                                color="#007bff",
                                className="button-icon",
                            ),
                            "Re-Imports",
                        ],
                        id="Re-Import",
                        className="button",
                    ),
                ],
                className="button-group",
            ),
            dcc.Store(id="selected-button"),
            dcc.Loading(
                dcc.Graph(id="bar-chart"),
            ),
        ],
    )


# ********************************************************************************************
@callback(
    Output("Export", "className"),
    Output("Import", "className"),
    Output("Re-Export", "className"),
    Output("Re-Import", "className"),
    #
    Output("selected-button", "data"),
    #
    Input("Export", "n_clicks"),
    Input("Import", "n_clicks"),
    Input("Re-Export", "n_clicks"),
    Input("Re-Import", "n_clicks"),
)
def update_button_styles(
    exports_click, imports_click, reexport_clicks, reimport_clicks
):
    # Default classes for all buttons
    classes = ["button", "button", "button", "button"]

    # Get the button that triggered the callback
    triggered_id = (
        callback_context.triggered[0]["prop_id"].split(".")[0]
        if callback_context.triggered
        else None
    )

    if triggered_id == "Export":
        classes[0] = "button selected"
    elif triggered_id == "Import":
        classes[1] = "button selected"
    elif triggered_id == "Re-Export":
        classes[2] = "button selected"
    elif triggered_id == "Re-Import":
        classes[3] = "button selected"
    else:
        classes[0] = "button selected"

    return classes[0], classes[1], classes[2], classes[3], triggered_id


# ********************************************************************************************
@callback(
    Output("bar-chart", "figure"),
    Input("selected-button", "data"),
)
def update_chart(selected_value):
    if selected_value == None:
        selected_value = "Export"
        
    # Filter data by selected flow
    filtered_df = df[df["flow"] == selected_value]
    
    # Group by country and count the number of transactions per country
    grouped_df = filtered_df.groupby("country_or_area", as_index=False).size()

    top_10_countries_df = grouped_df.sort_values(by="size", ascending=False).head(10)

    # Create the bar chart
    fig = px.bar(
        top_10_countries_df,
        x="country_or_area",
        y="size",
        text="size",
    )

    # Update trace styles
    fig.update_traces(
        hovertemplate="(%{x}, %{y})",
        texttemplate="%{text}",
        textposition="inside",  # Display text inside bars
        textangle=0,
        marker_color="#0096eb",
    )

    # Update layout
    fig.update_layout(
        template="simple_white",
        uniformtext_minsize=12,  # Increase text size for better visibility
        uniformtext_mode="show",
        yaxis_title=None,  # Remove y-axis title
        xaxis_title=None,  # Remove x-axis title
        margin=dict(t=30, b=50, l=30, r=30),  # Adjust margins for better alignment
        height=300,
    )

    # Customize the axes
    # fig.update_xaxes(showgrid=False)  # Remove gridlines from x-axis
    # fig.update_yaxes(showgrid=True, gridcolor="lightgrey")  # Light gridlines for y-axis

    return fig
