import dash
from dash import html, dcc, Output, Input, State, clientside_callback


def Header():
    """
    Reusable header component for your Dash app.
    """
    return html.Section(
        className="headerSection",
        children=[
            html.Div(
                className="headerItems container",
                children=[
                    dcc.Link(
                        className="headerLogo",
                        href="/",
                        children=[
                            html.Img(src="assets/images/logo/logo.png"),
                            html.H2("Commodity Trading Stats"),
                        ],
                    ),
                    html.Nav(
                        children=[
                            html.Div(
                                className="menu",
                                id="menu",
                                children=[
                                    html.Span(),
                                    html.Span(),
                                    html.Span(),
                                ],
                            ),
                            html.Ul(
                                className="",
                                id="open-in-small-devices",
                                children=[
                                    html.Li(
                                        children=[
                                            dcc.Link(
                                                href=page["relative_path"],
                                                children=f"{page['name']}",
                                            )
                                        ]
                                    )
                                    for page in dash.page_registry.values()
                                ],
                            ),
                        ]
                    ),
                ],
            )
        ],
    )


clientside_callback(
    """
    function(n_clicks, current_class) {
        if (n_clicks === null) {
            return current_class;
        }
        if (n_clicks % 2 === 1) {
            return "open";
        } else {
            return "initial-class";
        }
    }
    """,
    Output("open-in-small-devices", "className"),
    Input("menu", "n_clicks"),
    State("open-in-small-devices", "className"),
)
