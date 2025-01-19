import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
from utils.pretraitement import load_dataFestivals

dash.register_page(__name__, path='/culture', order = 5, display_name = '📚 Offre Culturelle')




departements, df, festivals_pvd = load_dataFestivals()

# Créer la carte initiale avec Plotly
fig = px.choropleth_mapbox(
    departements,
    geojson=departements.__geo_interface__,
    locations=departements.index,
    hover_name="nom",
    mapbox_style="carto-positron",
    title= "Veuillez sélectionner un département",
    center={"lat": 46.603354, "lon": 1.888334},
    zoom=3.8,
    opacity=0
)
df_grouped = df.groupby(["N_Département", "Type équipement ou lieu", "Latitude", "Longitude"])['Nom'].count().reset_index(name="Nombre d'équipements")

heatmap = px.density_mapbox(df, lat="Latitude", lon="Longitude", z="Nombre_fauteuils_de_cinema",
                        radius=30, zoom=4,
                        mapbox_style="open-street-map", title="Heatmap du nombre d\'équipements dans les PVD")

# Ajouter une couche pour les contours
fig.update_layout(
    mapbox=dict(
        layers=[{
            "source": departements.__geo_interface__,
            "type": "line",
            "color": "black",
            "line": {"width": 2}
        }]
    )
)

# Catégorisation
patrimoniaux = {'Monument', 'Lieu archéologique', 'Lieu de mémoire', 'Musée', 'Service d\'archives', 'Espace protégé', 'Parc et jardin'}
vivants = {'Bibliothèque', "Centre d'art", 'Cinéma', "Centre de création artistique", 'Conservatoire', "Établissement d'enseignement supérieur", 'Librairie', 'Scène', 'Théâtre', 'Centre culturel'}
df_grouped = df.groupby(["N_Département", "Type équipement ou lieu"]).size().reset_index(name="Nombre d'équipements")
df['Catégorie'] = df['Type équipement ou lieu'].apply(
    lambda x: 'Patrimonial' if x in patrimoniaux else 'Vivant'
)



# Layout de l'application
layout = html.Div([
    dcc.Tabs([
        ##### ONGLET 1 : Pricipal #####
        dcc.Tab(label="Offre Culturelle", 
            children=[
                html.Div([
                    html.Div(
                        children=[ 
                            dcc.Graph(id="map", figure=fig, style={"background-color": "#f9f9f9", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)", "margin-bottom": "10px","flex-grow": "1", "overflow": "auto"}),  
                            dcc.Graph(id="map2", style={"background-color": "#f9f9f9", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)", "margin-bottom": "10px","flex-grow": "1", "overflow": "auto"})
                        ],
                        style={"width": "40vw", "display": "grid", "grid-template-rows": "1fr 1fr", "top": "0", "left": "0", "flex": "none","height": "100vh","flex-grow": "1"}  # Ajusté à 40%
                    ),
                    html.Div([
                        html.Div([
                            html.H4(id="total-equipments", style={"font-size": "20px", "color": "blue", "background-color": "#f9f9f9", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)", "margin-bottom": "10px","flex-grow": "1", "overflow": "auto"}), 
                            html.H4(id="total-heritage", style={"font-size": "20px", "color": "blue", "background-color": "#f9f9f9", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)", "margin-bottom": "10px","flex-grow": "1", "overflow": "auto"}), 
                            html.H4(id="total-living", style={"font-size": "20px", "color": "blue", "background-color": "#f9f9f9", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)", "margin-bottom": "10px","flex-grow": "1", "overflow": "auto"})
                        ], style={"flex": "3", "display": "grid","width": "100%","grid-template-columns": "0.5fr 0.5fr 0.5fr", "padding": "20px", "background-color": "#f9f9f9", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)"}),

                        html.Div([
                            dcc.Graph(id="pie-chart", style={"background-color": "#f9f9f9", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)", "margin-bottom": "10px","flex-grow": "1", "overflow": "auto"}),
                            dcc.Graph(id="discipline-bar", style={"background-color": "#f9f9f9", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)", "margin-bottom": "10px","flex-grow": "1", "overflow": "auto"}),
                        ], style={"flex": "2", "display": "grid","width": "100%","grid-template-columns": "1.2fr 1.2fr"}),
                        html.Div([
                            dcc.Graph(id="stacked_bar_fig",style={"background-color": "#f9f9f9", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)", "margin-bottom": "10px","flex-grow": "1", "overflow": "auto"}),
                            dcc.Graph(id="domain-histogram", style={"background-color": "#f9f9f9", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)", "margin-bottom": "10px","flex-grow": "1", "overflow": "auto"})
                        ], style={"flex": "2", "display": "grid","width": "100%","grid-template-columns": "1.2fr 1.2fr"}),
                    ], style={"top": '0', 'right': '0', 'margin-right': '0', "width": "60vw","height": "100vh","display": "grid", "grid-template-rows": "1fr 1fr","flex-grow": "1"}) 
                ], style={"display": "flex", "flex-direction": "row","width": "100vw", "height": "5vh"}),
            ],
            style={
                'font-size': '16px', 'font-weight': 'bold', 'color': '#333',
                'border': '2px solid #4CAF50', 'border-radius': '5px', 'background-color': '#fff',
                'padding': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-right': '10px'
            },
            selected_style={
                'background-color': "#4CAF50", 'color': '#fff', 'border': '2px solid #4CAF50','font-weight': 'bold'
            }
        ),
    
        dcc.Tab(
            label="Comparaison",
            children=[
                html.Div([
                    html.Div([
                        html.H1("Comparaison des Départements", style={ "text-align": "center", "color": "#4CAF50", "margin-bottom": "20px"}),

                # Sélections des départements
                html.Div([
                    html.Label("Département 1:", style={"font-size": "16px", "margin-bottom": "10px", "font-weight": "bold"}),
                    dcc.Dropdown(
                    id="department1",  # ID utilisé pour le 1er département
                    options=[{"label": nom, "value": nom} for nom in departements["nom"]],
                    style={"width": "90%", "font-size": "14px", "padding": "10px"},
                    placeholder="Sélectionnez un département",
                    ),
                    html.Label("Département 2:", style={"font-size": "16px", "margin-top": "20px", "margin-bottom": "10px", "font-weight": "bold"}),
                    dcc.Dropdown(
                    id="department2",  # ID utilisé pour le 2nd département
                    options=[{"label": nom, "value": nom} for nom in departements["nom"]],
                    style={"width": "90%", "font-size": "14px", "padding": "10px"},
                    placeholder="Sélectionnez un département",
                    ),
                ], style={"padding": "20px","background-color": "#f9f9f9","border": "1px solid #ddd","border-radius": "5px","box-shadow": "0px 0px 10px rgba(0, 0, 0, 0.1)","margin": "10px","width": "300px"}),
            ], style={"text-align": "left", "width": "25%", "padding": "20px"}),

            # Graphiques principaux
            html.Div([
                html.Div([
                    dcc.Graph(id="bar-chart-comparison"),
                    dcc.Graph(id="pie-chart-comparison"),
                ], style={"display": "grid", "grid-template-columns": "1fr 1fr", "gap": "20px"}),

                html.Div([
                    dcc.Graph(id="stacked-bar-comparison"),
                    dcc.Graph(id="festival-comparison"),
                ], style={"display": "grid", "grid-template-columns": "1fr 1fr", "gap": "20px"}),
            ], style={"width": "75%", "padding": "20px"}),
            ], style={ "display": "flex","flex-direction": "row","width": "100vw","height": "100vh","font-family": "Arial, sans-serif","background-color": "#f5f5f5"})
            ],style={
                'font-size': '16px', 'font-weight': 'bold', 'color': '#333',
                'border': '2px solid #4CAF50', 'border-radius': '5px', 'background-color': '#fff',
                'padding': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-right': '10px'
            },
            selected_style={
                'background-color': "#4CAF50", 'color': '#fff', 'border': '2px solid #4CAF50','font-weight': 'bold'
            }
        )
                
     ])
])       

        
@callback(
    [Output('pie-chart', 'figure'),
     Output('stacked_bar_fig', 'figure'),
     Output('domain-histogram', 'figure'),
     Output('map2', 'figure'),
     Output('discipline-bar', 'figure'),
     Output('total-equipments', 'children'),
     Output('total-heritage', 'children'),
     Output('total-living', 'children')],
    Input("map", "clickData"),
)

def update_charts(click_data):
    if click_data:
        index = click_data["points"][0]["location"]
        dept = departements.iloc[int(index)]
        filtered_df = df[df['Département'] == dept['nom']]
        filtered_festivals = festivals_pvd[festivals_pvd['Département principal de déroulement'] == dept['nom']]
        #print(filtered_df['Département'])
        if not filtered_df.empty :
            # Nombre total d'équipements
            total_equipments = filtered_df.shape[0]
            total_heritage = filtered_df[filtered_df['Catégorie'] == 'Patrimonial'].shape[0]
            total_living = filtered_df[filtered_df['Catégorie'] == 'Vivant'].shape[0]
                
            # Pie chart
            proportions = filtered_df['Catégorie'].value_counts(normalize=True) * 100
            pie_fig = px.pie(
                names=proportions.index,
                values=proportions.values,
                title=f'Proportions des catégories : Patrimoniaux vs Actives',
                title_x=0.5,
                color_discrete_sequence=['skyblue', 'lightgreen'],
                hole=0.4
            )

            # Bar plot
            #bar_fig = px.histogram(filtered_df, x="Type équipement ou lieu", histfunc="sum", title="Proportions des équipements culturels")
            #bar_fig.update_layout(barmode='stack', xaxis_title="Type d'équipement", yaxis_title="Capacité totale")
            # New plot: Distribution of Disciplines 
            discipline_counts = filtered_festivals['Discipline dominante'].value_counts().reset_index() 
            discipline_counts.columns = ['Discipline', 'Count'] 
            discipline_fig = px.bar( 
                discipline_counts, 
                x='Discipline', 
                y='Count', 
                labels={'Discipline': 'Discipline Dominante', 'Count': 'Nombre de Festivals'}, 
                title=f"Répartition des Disciplines des Festivals dans les PVDs de {dept['nom']}", 
                color='Discipline' 
            ) 
            discipline_fig.update_layout( 
                xaxis_title="Discipline Dominante", 
                yaxis_title="Nombre de Festivals", 
                xaxis_tickangle=-45 
            )

            # Nouveau graphique : Répartition des équipements par type et catégorie
            stacked_bar_fig = px.bar(
                filtered_df.groupby(['Type équipement ou lieu', 'Catégorie']).size().reset_index(name='Count'),
                x="Type équipement ou lieu", y="Count", color="Catégorie", title=f"Répartition des équipements par type et catégorie dans les PVDs",
                barmode="stack",
                color_discrete_sequence=['skyblue', 'lightgreen']
            )
            stacked_bar_fig.update_layout(
                xaxis_title="Type d'équipement",
                yaxis_title="Nombre d'équipements",
                height=500
            )

            # Domain histogram
            domain_hist_fig = px.histogram(filtered_df, x="Domaine", color="Sous-domaine", title="Répartition des équipements par domaine et sous-domaine")

            #map density nbr de place au cinéma
            map2 = px.density_mapbox(filtered_df, lat="Latitude", lon="Longitude", z="Nombre_fauteuils_de_cinema",
                            radius=10, zoom=6,
                            mapbox_style="open-street-map", title="Heatmap du nombre d\'équipements dans les PVDs")

            

            return pie_fig, stacked_bar_fig, domain_hist_fig, map2, discipline_fig, f"Nombre total d'équipements : {total_equipments}", f"Nombre d'équipements patrimoniaux : {total_heritage}", f"Nombre d'équipements vivants : {total_living}"
        else:
            return px.pie(), "Cliquez sur un département pour afficher les informations.", px.histogram(), px.bar(), px.histogram(), px.density_mapbox(), {}, "", "", ""

    return px.pie(), "Cliquez sur un département pour afficher les informations.", px.histogram(), px.bar(), px.histogram(), px.density_mapbox(), {}, "", "", ""



#comparaison

@callback(
    [Output('bar-chart-comparison', 'figure'),
     Output('pie-chart-comparison', 'figure'),
     Output('stacked-bar-comparison', 'figure'),
     Output('festival-comparison', 'figure')],
    [Input('department1', 'value'),
     Input('department2', 'value')]
)

def update_charts_comparaison(dept1, dept2):
    # Vérifier si un département est sélectionné
    if not dept1 or not dept2:
        return px.bar(), px.pie(), px.bar(), px.bar()
    
    # Filtrer les données pour chaque département
    data1 = df[df["Département"] == dept1]
    data2 = df[df["Département"] == dept2]
    
    # Ajouter une colonne pour distinguer les départements
    data1['Département_Label'] = dept1
    data2['Département_Label'] = dept2
    
    # Fusionner les deux datasets pour les comparaisons
    combined_data = pd.concat([data1, data2])

    # 1. Bar chart comparatif
    bar_chart = px.bar(
        combined_data, 
        x="Type équipement ou lieu", 
        y="N_Département",  
        color="Département_Label",
        barmode="group",  # Barres juxtaposées
        title="Comparaison des équipements par type"
    )

    # 2. Diagramme circulaire de comparaison
    pie_chart = px.pie(
        combined_data, 
        names="Département_Label", 
        values="N_Département", 
        title="Répartition des équipements entre les deux départements"
    )
    
    # 3. Barres empilées comparatives
    stacked_bar = px.bar(
        combined_data, 
        x="Domaine", 
        y="N_Département",  
        color="Département_Label",
        barmode="stack",  # Barres empilées
        title="Répartition des domaines entre les départements"
    )

    # 4. Histogramme des festivals par département
    festival_comparison = px.histogram(
        combined_data, 
        x="Type équipement ou lieu", 
        y="N_Département",  
        color="Département_Label",
        title="Histogramme des festivals entre les deux départements"
    )

    return bar_chart, pie_chart, stacked_bar, festival_comparison
