from dash import html, register_page

from dash_iconify import DashIconify

from components.GetData import GetData
from components.components.number_of_trades_card import number_of_trades_card
from components.components.balance_of_trades_card import balance_of_trades_card
from components.components.top_10_countries_with_trades_card import (
    top_10_countries_with_trades_card,
)
from components.components.balance_of_trade_raw_data_card import (
    balance_of_trade_raw_data_card,
)


# --------------------------------------------------------------------------------
def card_item(icon, label, value):
    return (
        html.Div(
            className="cardItem",
            children=[
                html.Div(
                    className="iconCard",
                    children=DashIconify(icon=icon, width=25, color="#FFFFFF"),
                ),
                html.Div([html.P(label), html.H3(value)]),
            ],
        ),
    )


# --------------------------------------------------------------------------------

register_page(
    __name__,
    path="/",
    title="Historical Analysis",
    name="Historical Analysis",
)

df = GetData()
# 1
num_countries = df["country_or_area"].nunique()
# 2
min_year = df["year"].min()
max_year = df["year"].max()
years = f"{min_year} - {max_year}"
# 3
num_categories = df["category"].nunique()
# 4
num_products = df["commodity"].nunique()
# 5
num_imports = df["flow"].eq("Import").sum()
# 6
num_Export = df["flow"].eq("Export").sum()

# --------------------------------------------------------------------------------
# Layout Start
# --------------------------------------------------------------------------------
layout = html.Div(
    className="historicalCardSection",
    children=[
        html.Div(
            className="grid-container",
            children=[
                # -----------------------------------------------------------------------------
                # First row
                # -----------------------------------------------------------------------------
                html.Div(
                    card_item("material-symbols:globe", "No. Countries", num_countries),
                    className="grid-item",
                ),
                html.Div(
                    card_item("ic:twotone-date-range", "Years Range", years),
                    className="grid-item",
                ),
                html.Div(
                    card_item(
                        "material-symbols:category-rounded",
                        "No. Categories",
                        num_categories,
                    ),
                    className="grid-item",
                ),
                html.Div(
                    card_item(
                        "material-symbols:flowchart-sharp", "No. Products", num_products
                    ),
                    className="grid-item",
                ),
                html.Div(
                    card_item(
                        "ic:twotone-arrow-downward", "Total Imports", num_imports
                    ),
                    className="grid-item",
                ),
                html.Div(
                    card_item("ic:twotone-arrow-upward", "Total Exports", num_Export),
                    className="grid-item",
                ),
                # -----------------------------------------------------------------------------
                # Seconde row
                # -----------------------------------------------------------------------------
                html.Div(
                    number_of_trades_card(),
                    className="grid-item",
                ),
                html.Div(
                    balance_of_trades_card(),
                    className="grid-item",
                ),
                # -----------------------------------------------------------------------------
                # Third row
                # -----------------------------------------------------------------------------
                html.Div(
                    top_10_countries_with_trades_card(),
                    className="grid-item",
                ),
                html.Div(
                    balance_of_trade_raw_data_card(),
                    className="grid-item",
                ),
            ],
        )
    ],
)
# --------------------------------------------------------------------------------
# Layout End
# --------------------------------------------------------------------------------
