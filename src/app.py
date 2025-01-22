from dash import Dash, dcc, html, page_container

from components.header.Header import Header

app = Dash(__name__, use_pages=True)
server = app.server


app.layout = html.Div(
    [Header(), html.Div(className="container", children=page_container)]
)

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
