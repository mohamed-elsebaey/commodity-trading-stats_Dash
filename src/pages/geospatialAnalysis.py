from dash import html, dcc, register_page
from dash_iconify import DashIconify
import plotly.express as px
import pandas as pd
from components.GetData import GetData

df = GetData()

country_data = df.groupby("country_or_area").size().reset_index(name="Total Trades")
hover_data = (
    df.groupby(["country_or_area", "flow"]).size().reset_index(name="Number of Trades")
)

hover_info = (
    hover_data.pivot(index="country_or_area", columns="flow", values="Number of Trades")
    .fillna(0)
    .reset_index()
)

# حساب النسب المئوية
flows = ["Export", "Import", "Re-Export", "Re-Import"]
hover_info["Total"] = hover_info[flows].sum(axis=1)
hover_info["Export%"] = (hover_info["Export"] / hover_info["Total"]) * 100
hover_info["Import%"] = (hover_info["Import"] / hover_info["Total"]) * 100
hover_info["Re-Export%"] = (hover_info["Re-Export"] / hover_info["Total"]) * 100
hover_info["Re-Import%"] = (hover_info["Re-Import"] / hover_info["Total"]) * 100

# إنشاء hover_text مع تنسيق HTML
hover_info["hover_text"] = hover_info.apply(
    lambda row: f"<b>Country:</b> {row['country_or_area']}<br>"
    + f"<b>Total Trades:</b> {row['Total']}<br>"
    + f"<b>Export:</b> {row['Export%']:.1f}%<br>"
    + f"<b>Import:</b> {row['Import%']:.1f}%<br>"
    + f"<b>Re-Export:</b> {row['Re-Export%']:.1f}%<br>"
    + f"<b>Re-Import:</b> {row['Re-Import%']:.1f}%",
    axis=1,
)

# دمج البيانات
merged_data = pd.merge(
    country_data,
    hover_info[["country_or_area", "hover_text"]],
    on="country_or_area",
    how="left",
)

# إنشاء الخريطة
fig = px.choropleth(
    merged_data,
    locations="country_or_area",
    locationmode="country names",
    color="Total Trades",
    hover_name="country_or_area",
    hover_data={"hover_text": True, "Total Trades": True},
    color_continuous_scale=["#440154", "#30678D", "#35B779", "#FDE725"],
)

# تحديث تنسيق الخريطة
fig.update_traces(
    hovertemplate="%{customdata[0]}<extra></extra>"
)

fig.update_layout(
    title=dict(
        text="Hover over a country to see more info..",
        font=dict(size=12),
        y=0.95,
    ),
    geo=dict(
        showframe=True,
        framecolor="black",
        showcoastlines=True,
        coastlinecolor="black",
        projection_type="equirectangular",
    ),
    height=680,
    coloraxis_colorbar=dict(
        title=dict(text="Number of Trades", side="bottom"),
        orientation="h",
        xanchor="center",
        x=0.5,
        y=-0.17,
        thickness=16,
        len=0.7,
    ),
)

register_page(
    __name__,
    path="/geospatialAnalysis",
    title="Geospatial analysis",
    name="Geospatial analysis",
)

layout = html.Div(
    className="geospatial-card-section",
    children=[
        html.Div(
            className="pageTitle",
            children=[
                DashIconify(icon="mdi:map-search", width=30, color="#094546"),
                html.H2("Countries Overall Number of Trades"),
            ],
        ),
        dcc.Graph(id="choropleth-map", figure=fig),
    ],
)