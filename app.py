import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    # Header
    html.Div(
        html.H1("Tableau de bord : Petites Villes de Demain", style={
            "textAlign": "center",
            "fontFamily": "Arial, sans-serif",
            "color": "#333",
            "backgroundColor": "#f7f7f7",
            "padding": "20px 0",
            "marginBottom": "20px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
        }),
        style={"borderBottom": "4px solid #4CAF50"}
    ),

    # Navigation Menu
    html.Div(
        [
            dcc.Link(
                f"{page.get('display_name', page['name']).upper()}", 
                href=page["relative_path"], 
                style={
                    'display': 'inline-block',
                    "margin": "0 15px",
                    "textDecoration": "none",
                    "color": "#4CAF50",
                    "fontSize": "18px",
                    "fontWeight": "bold",
                    "transition": "color 0.3s ease",
                },
                className="menu-link"
            ) 
            for page in dash.page_registry.values()
        ],
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "gap": "10px",
            "margin": "10px 0",
            "padding": "10px",
            "backgroundColor": "#e8f5e9",
            "borderRadius": "8px",
            "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
        }
    ),

    # Content Area
    html.Div(
        dash.page_container,
        style={
            "margin": "20px",
            "padding": "20px",
            "backgroundColor": "#fff",
            "borderRadius": "8px",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
            "fontFamily": "Arial, sans-serif",
            "lineHeight": "1.6"
        }
    ),
])


app.css.config.serve_locally = True 

if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)