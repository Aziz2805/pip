import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import json
from shapely.geometry import shape

from utils.pretraitement import (
    load_contours_regions,
    load_PVDs_per_region,
    load_signatures_par_annee_region,
    load_superficies_regions,
    load_PVD_infos
)


dash.register_page(__name__, path='/regions', order = 2, display_name = "🌎 Visualisation Régionale")


# Données statiques globales
regions = load_contours_regions()
PVDs_per_region = load_PVDs_per_region()
superficies_regions = load_superficies_regions()

# Données combinées statiques
df = pd.merge(regions, PVDs_per_region, how='inner', left_on='code_insee', right_on='Code Officiel Région')
geojson_data = json.loads(df.to_json())

center = {
    "lat": 46.603354,  # Latitude du centre de la France
    "lon": 1.888334    # Longitude du centre de la France
}

# Carte des régions statique
fig1 = px.choropleth_mapbox(
    df,
    geojson=geojson_data,
    locations=df.index,
    mapbox_style="open-street-map",
    center=center,
    zoom=3.5,
    hover_name="nom",
    color='nb_PVDs',
    title = "Degré de répartition des PVDs sur la France",
    labels={'nb_PVDs': 'Nombre de PVDs'}
).update_layout(title_x = 0.5)

# Layout statique
layout = html.Div(
    [
        # Dropdown pour choisir la région
        html.Div(
            dcc.Dropdown(
                id="region",
                options=[
                    {"label": region, "value": region} for region in regions["nom"].values
                ],
                value=regions["nom"].iloc[0],
                style={"width": "60%", "margin": "20px auto", "padding": "10px"},
            ),
            style={"text-align": "center"},
        ),
        
        # Conteneur principal
        html.Div(
            [
                # Carte des régions (à gauche)
                html.Div(
                    dcc.Graph(id="f5", figure={},style={"height": "870px"}),
                    style={
                        "flex": "1",
                        "margin": "10px",
                        "padding": "30px",
                        "border": "0.5px solid #ddd",
                        "border-radius": "10px",
                        "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "background-color": "#f9f9f9",
                        "height": "900px"
                    },
                ),

                # Graphiques descriptifs (à droite)
                html.Div(
                    [
                        dcc.Graph(id="f2", figure={}, style={}),
                        dcc.Graph(id="f3", figure={}, style={}),
                        dcc.Graph(id="f4", figure={}, style={}),
                        dcc.Graph(id="carte-regions", figure=fig1, style={}),
                    ],
                    style={
                        "flex": "2",
                        "display": "grid",
                        "grid-template-columns": "1fr 1fr",
                        "gap": "15px",
                        "padding": "10px",
                        "border": "0.5px solid #ddd",
                        "border-radius": "5px",
                        "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "background-color": "#ffffff",
                    },
                ),
            ],
            style={
                "display": "flex",
                "gap": "5px",
                "padding": "30px",
                "align-items": "flex-start",
            },
        ),
    ],
    style={"font-family": "Arial, sans-serif", "background-color": "#f4f6f9"},
)


# Mise à jour des graphiques en fonction de la région sélectionnée
@callback(
    [Output("f2", "figure"),
     Output("f3", "figure"),
     Output("f4", "figure"),
     Output("f5", "figure"),
    ],
    Input("region", "value")
)
def update_carte(selection):
    # Nombre de PVDs dans la région sélectionnée
    nb_PVDs = df[df['Nom Officiel Région'] == selection]['nb_PVDs'].iloc[0]
    total_PVDs = PVDs_per_region['nb_PVDs'].sum()

    # Gauge chart
    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=nb_PVDs,
        gauge={'axis': {'range': [None, total_PVDs]}},
        title={'text': f"Petites Villes sur {selection}", 'font': {'size': 20}}
    ))

    # Bar chart comparatif
    df['couleur'] = 'blue'
    df.loc[df['Nom Officiel Région'] == selection, 'couleur'] = 'red'

    fig3 = px.bar(df, x='Nom Officiel Région', y='nb_PVDs', color='couleur', title="PVDs par Région")
    fig3.update_layout(
        showlegend=False,
        title=f"Positionnement aux autres régions", 
        title_x=0.5, 
        yaxis_title="Nombre de PVDs",
    )

    # Pie chart des signatures par année
    data_selection = load_signatures_par_annee_region().loc[selection]
    fig4 = px.pie(
        data_selection,
        names=data_selection.index,
        values=selection,
        title="Proportion des signatures par année",
        hole=0.6
    ).update_layout(title={"text": "Proportion des signatures par année", "x": 0.5})

    # Carte des PVDs de la région sélectionnée
    PVD = load_PVD_infos()
    region_pvds = PVD[PVD['Nom Officiel Région'] == selection][['lib_com', 'Geo Shape']]
    region_pvds['geometry'] = region_pvds['Geo Shape'].apply(lambda x: shape(json.loads(x)))
    gdf = gpd.GeoDataFrame(region_pvds, geometry='geometry')

    fig5 = px.choropleth_mapbox(
        gdf,
        geojson=gdf.__geo_interface__,
        locations=gdf.index,
        mapbox_style="open-street-map",
        center={"lat": gdf.geometry.centroid.y.mean(), "lon": gdf.geometry.centroid.x.mean()},
        zoom=5,
        hover_name="lib_com",
        title=f"Explorer les PVDs sur {selection}"
    ).update_layout(title_x = 0.5)

    return fig2, fig3, fig4, fig5
