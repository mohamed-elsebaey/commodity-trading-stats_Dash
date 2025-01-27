import dash
from dash import (
    html,
    dcc,
    Output,
    Input,
    State,
    clientside_callback,
    callback,
    no_update,
)


def Header():
    """
    Reusable header component for your Dash app.
    """
    return html.Section(
        className="headerSection",
        children=[
                    dcc.Location(id="url", refresh=False),
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
                                                id={"type": "nav-link", "index": page["name"]},
                                                className="nav-link"
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
    function(pathname, linksHref) {
        return linksHref.map(href => {
            return href === pathname ? 'nav-link active' : 'nav-link'
        })
    }
    """,
    Output({"type": "nav-link", "index": dash.ALL}, "className"),
    Input("url", "pathname"),
    State({"type": "nav-link", "index": dash.ALL}, "href"),
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
