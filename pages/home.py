import dash
from dash import Dash, dcc, html, Input, Output, callback

dash.register_page(__name__, path='/home', order = 1, display_name = "🏠 Home")

layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'margin': '0 auto',
        'maxWidth': '800px',
        'padding': '20px',
        'textAlign': 'center'
    },
    children=[
        html.P(
            "Bienvenue sur notre tableau de bord interactif dédié aux Petites Villes de Demain ! 🏙️ \n " 
            "Utilisez les onglets pour explorer les visualisations par thématique souhaitée.",
            style={'fontSize': '1.2em', 'color': '#34495e'}
        ),
        html.Footer(
            "Développé par CHENNOUFI Aziz, GARCIA Quentin, AZEBAZE KAGHO Richel, LI Hanchen, TRAIBI Ranya, EL ARRACH Najwa,  © 2025",
            style={'marginTop': '50px', 'fontSize': '0.9em', 'color': '#95a5a6'}
        )
    ]
)
