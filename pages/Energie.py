import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_import import (
    nb_install_tri, nb_install_PVD,
    nb_dep,
    nb_dep_pvd,
    nb_reg,
    nb_reg_pvd,
    pvd,
    prod,
    conso,
    data_dep_reg,
    reg_name,
    filiere_colors
)

dash.register_page(__name__, path='/energie', order = 6, display_name = '⚡️ Energie')

layout = html.Div([
    ### EN-TETE ###
    html.H1('Énergies Renouvelables'),
    html.Div(
        style={'height': '10px', 'background-color': '#4CAF50', 'margin-bottom': '10px', 'margin-top': '10px'}
    ),
    html.Div(
        children=[
            # Dropdowns :
            html.Div(
                children=[
                    dcc.Dropdown(
                        id='choix-region',
                        options=[{'label': region, 'value': region} for region in reg_name],
                        placeholder="Sélectionnez une région",
                        style={'flex': '1', 'margin-right': '10px'}
                    ),
                    dcc.Dropdown(
                        id='choix-departement',
                        placeholder="Sélectionnez un département",
                        style={'flex': '1', 'margin-right': '10px'}
                    ),
                    dcc.Dropdown(
                        id='choix-pvd',
                        placeholder="Sélectionnez une Petite Ville de Demain",
                        style={'flex': '1'}
                    )
                ],
                style={
                    'display': 'flex',  # dropdowns côte à côte
                    'justify-content': 'space-between',  # Espacement égal entre chaque dropdown
                    'align-items': 'center',
                    'margin-bottom': '10px',
                    'width': '100%'
                }
            ),
            # Compteur PVD :
            html.Div(
                id="compteur-pvd",
                style={
                    'text-align': 'center', 'font-size': '18px', 'margin-top': '10px',
                    'backgroundColor': '#f7f7f7', 'borderRadius': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                    'padding': '20px'
                }
            )
        ],
        style={
            'display': 'flex', 
            'flex-direction': 'column', 
            'align-items': 'center',
            'margin-bottom': '20px',
            'width': '80%', 
            'margin': '0 auto',
            'backgroundColor': '#f7f7f7',
            'borderRadius': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'padding': '20px'
        }
    ),
    ### TABS ###
    dcc.Tabs([
        ##### ONGLET 1 : INSTALLATIONS #####
        dcc.Tab(label="Installations de production d'énergies renouvelables", children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H3('Nombre d\'installations par filière renouvelable'),
                            dcc.Graph(id='graph-nb-install', style={'width': '100%', 'height': '100%'})
                        ],
                        style={'width': '31%', 'display': 'inline-block', 'margin-right': '2%',
                               'backgroundColor': '#f7f7f7', 'borderRadius': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                               'text-align': 'center', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        children=[
                            html.H3('Nombre d\'installations des PVD par filière renouvelable'),
                            dcc.Graph(id='graph-nb-install-pvd', style={'width': '100%', 'height': '100%'})
                        ],
                        style={'width': '31%', 'display': 'inline-block', 'margin-right': '2%',
                               'backgroundColor': '#f7f7f7', 'borderRadius': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                               'text-align': 'center', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        children=[
                            html.H3('Nombre d\'installations par filière renouvelable pour une PVD spécifique'),
                            dcc.Graph(id='graph-pvd-specific', style={'width': '100%', 'height': '100%'})
                        ],
                        style={'width': '31%', 'display': 'inline-block',
                               'backgroundColor': '#f7f7f7', 'borderRadius': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                               'text-align': 'center', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}
                    )
                ],
                style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'margin-bottom': '20px', 'margin-top': '20px'}
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H3("Taux d'installations de production d'énergie dans les PVD (%)"),
                                dcc.Graph(id='gauge-chart', style={'width': '100%', 'height': '100%'})
                        ],
                        style={'width': '31%', 'display': 'inline-block', 'margin-right': '2%',
                               'backgroundColor': '#f7f7f7', 'borderRadius': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                               'text-align': 'center', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        children=[
                            html.H3("Répartition des filières d'énergies renouvelables au sein PVD"),
                            dcc.Graph(id='pie-graph-filiere')
                        ],
                        style={'width': '31%', 'display': 'inline-block', 'margin-right': '2%',
                               'backgroundColor': '#f7f7f7', 'borderRadius': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                               'text-align': 'center', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        children=[
                            html.H3("Evolution du nombre d'installations d'énergie renouvelable dans les PVD au fil du temps"),
                            dcc.Graph(id='graph-nb-install-totale',figure={})
                        ],
                        style={'width': '31%', 'display': 'inline-block',
                               'backgroundColor': '#f7f7f7', 'borderRadius': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                               'text-align': 'center', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}
                    )
                ],
                style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'margin-bottom': '20px', 'margin-top': '20px'}
            )
        ], style={
            'font-size': '16px', 'font-weight': 'bold', 'color': '#333',
            'border': '2px solid #4CAF50', 'border-radius': '5px', 'background-color': '#fff',
            'padding': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-right': '10px'
        },
        selected_style={
            'background-color': '#4CAF50', 'color': '#fff', 'border': '2px solid #4CAF50', 'font-weight': 'bold'
        }),
        
        ###### ONGLET 2 : PRODUCTION & CONSO #####
        dcc.Tab(
            label="Production d'énergie renouvelable & consommation d'énergie",
            children=[
                html.Div(
                    children=[
                        # Section classements
                        html.Div(
                            children=[
                                html.Div(
                                    id='classement-prod',
                                    style={
                                        'width': '100%', 'backgroundColor': '#f7f7f7', 'borderRadius': '20px',
                                        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                                        'text-align': 'center', 'margin-bottom': '20px'
                                    }
                                ),
                                html.Div(
                                    id='classement-conso',
                                    style={
                                        'width': '100%', 'backgroundColor': '#f7f7f7', 'borderRadius': '20px',
                                        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                                        'text-align': 'center', 'margin-bottom': '20px'
                                    }
                                ),
                            ],
                            style={
                                'width': '32%', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between',
                                'margin-right': '20px'  # Espace entre les colonnes
                            }
                        ),
                        # Section jauges dans deux bulles différentes
                        html.Div(
                            children=[
                                # Première jauge
                                html.Div(
                                    children=[
                                        html.H3("Taux de production d'énergie renouvelable dans les PVD (%)"),
                                        dcc.Graph(id='gauge-chart-prod', style={'height': '300px'})
                                    ],
                                    style={
                                        'width': '48%', 'backgroundColor': '#f7f7f7', 'borderRadius': '20px',
                                        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px',
                                        'margin-right': '2%', 'text-align': 'center'
                                    }
                                ),
                                # Deuxième jauge
                                html.Div(
                                    children=[
                                        html.H3("Taux de consommation d'énergie dans les PVD (%)"),
                                        dcc.Graph(id='gauge-chart-conso', style={'height': '300px'})
                                    ],
                                    style={
                                        'width': '48%', 'backgroundColor': '#f7f7f7', 'borderRadius': '20px',
                                        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'padding': '20px', 'text-align': 'center'
                                    }
                                ),
                            ],
                            style={
                                'width': '64%', 'display': 'flex', 'justifyContent': 'space-between',
                                'alignItems': 'center'
                            }
                        ),
                    ],
                    style={
                        'display': 'flex', 'justifyContent': 'space-between', 'width': '100%', 'alignItems': 'flex-start', 'margin': '0px'
                    }
                )
            ],
            style={
                'font-size': '16px', 'font-weight': 'bold', 'color': '#333',
                'border': '2px solid #4CAF50', 'border-radius': '5px', 'background-color': '#fff',
                'padding': '10px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-right': '10px'
            },
            selected_style={
                'background-color': '#4CAF50', 'color': '#fff', 'border': '2px solid #4CAF50','font-weight': 'bold'
            }
        )
    ])
])

###################################################################################################################
###################################################################################################################
################################################# APPS & CALLBACKS :###############################################
###################################################################################################################
###################################################################################################################
##################################################### ENTETE ######################################################
###################################################################################################################
### Choix département : ###

@callback(
    Output('choix-departement', 'options'),
    Input('choix-region', 'value'))
def update_departements(region):
    if region is None:
        return []
    # Filtrer les départements pour la région sélectionnée
    dep_in_reg = data_dep_reg['dep_name'][data_dep_reg['region_name'] == region]
    return [{'label': dep, 'value': dep} for dep in dep_in_reg]

### Choix PVD : ###
@callback(
    Output('choix-pvd', 'options'),
    [Input('choix-departement', 'value')])
def update_pvd(departement):
    if departement is None:
        return []
    # Filtrer les PVD pour le département sélectionné
    pvd_in_dep = pvd['commune'][pvd["Nom Officiel Département"] == departement]
    return [{'label': pvd, 'value': pvd} for pvd in pvd_in_dep]

### Affichage nombre PVD : ###
@callback(
    Output('compteur-pvd', 'children'),
    Input('choix-region', 'value'),
    Input('choix-departement', 'value'))
def update_pvd_count(region, departement):
    if not region:
        return f"Nombre total de Petites Villes de Demain en France: {pvd.shape[0]}"
    if region and not departement:
        return f"Nombre total de Petites Villes de Demain dans la région {region} : {pvd[pvd['region'] == region].shape[0]}"
    if region and departement:
        return f"Nombre de Petites Villes de Demain dans le département {departement} : {pvd[pvd['Nom Officiel Département'] == departement].shape[0]}"
    return "Aucune information disponible pour la sélection actuelle."

###################################################################################################################
################################################### Onglet 1 ######################################################
###################################################################################################################
################################################
### Graphe - Nombre d'installation dep/reg : ###
################################################
@callback(
    Output('graph-nb-install', 'figure'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value')]
)
def update_graph(region, departement):
    if not region: 
        return go.Figure()
    # Si un département est sélectionné
    if departement:
        df, dates = nb_install_tri(departement, False, True)
        titre = f"En {departement} ({region})"
    else:
        # Si seulement la région est sélectionnée
        df, dates = nb_install_tri(region, False, False)
        titre = f"En {region}"
    # Création du graphique
    fig = go.Figure()
    for filiere in filiere_colors.keys():
        if filiere in df.columns:
            fig.add_trace(go.Scatter(
                x=dates,
                y=df[filiere],
                mode='lines+markers',  # Relie les points avec des lignes
                name=filiere,
                marker=dict(color=filiere_colors[filiere], size=8),
                line=dict(color=filiere_colors[filiere], width=2) 
            ))
    # Mise à jour du layout du graphique
    fig.update_layout(
        title=titre,
        xaxis_title="Année",
        yaxis_title="Nombre d'installations",
        legend_title="Filière",
        xaxis=dict(tickangle=45),
        height=400,  # Augmenter la hauteur du graphique
        width=550,   # Réduire la largeur du graphique
        margin=dict(l=50, r=50, t=50, b=50)  # Marges pour éviter que le texte soit coupé
    )
    return fig

####################################################
### Graphe - Nombre d'installation PVD dep/reg : ###
####################################################
@callback(
    Output('graph-nb-install-pvd', 'figure'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value')]
)
def update_graph_pvd(region, departement):
    if not region: 
        return go.Figure()
    # Si un département est sélectionné
    if departement:
        df, dates = nb_install_tri(departement, True, True)
        titre = f"En {departement} ({region})"
    else:
        # Si seulement la région est sélectionnée
        df, dates = nb_install_tri(region, True, False)
        titre = f"Au {region}"
    
    # Création du graphique
    fig = go.Figure()
    for filiere in filiere_colors.keys():
        if filiere in df.columns:
            fig.add_trace(go.Scatter(
                x=dates,
                y=df[filiere],
                mode='lines+markers',  # Relie les points avec des lignes
                name=filiere,
                marker=dict(color=filiere_colors[filiere], size=8),  # Points colorés
                line=dict(color=filiere_colors[filiere], width=2)  # Lignes colorées
            ))
    # Mise à jour du layout du graphique
    fig.update_layout(
        title=titre,
        xaxis_title="Année",
        yaxis_title="Nombre d'installations",
        legend_title="Filière",
        xaxis=dict(tickangle=45),
        height=400,  # Augmenter la hauteur du graphique
        width=550,   # Réduire la largeur du graphique
        margin=dict(l=50, r=50, t=50, b=50)  # Marges pour éviter que le texte soit coupé
    )
    return fig
######################################################
### Graphe - Nombre d'installation PVD spécifique: ###
######################################################
@callback(
    Output('graph-pvd-specific', 'figure'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value'),
     Input('choix-pvd', 'value')]
)
def update_graph_pvd_specific(region, departement, pvd_selection):
    if not region or not departement or not pvd_selection:
        # Si aucune sélection, retourner un graphique vide
        return go.Figure()
    # Filtrer les données pour la PVD sélectionnée
    df, dates = nb_install_PVD(pvd_selection)
    titre = f"Nombre d'installations par filière renouvelable de la PVD {pvd_selection} ({departement} - {region})"
    # Créer le graphique
    fig = go.Figure()
    for filiere in filiere_colors.keys():
        if filiere in df.columns:
            fig.add_trace(go.Scatter(
                x=dates,
                y=df[filiere],
                mode='lines+markers',
                name=filiere,
                marker=dict(color=filiere_colors[filiere], size=8),
                line=dict(color=filiere_colors[filiere], width=2)
            ))
    # Mise en page du graphique
    fig.update_layout(
        title=titre,
        xaxis_title="Année",
        yaxis_title="Nombre d'installations",
        legend_title="Filière",
        xaxis=dict(tickangle=45),
        height=400,
        width=550,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

#####################################
### Graphe part d'installations : ###
#####################################
@callback(
    Output('gauge-chart', 'figure'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value')])
def update_gauge(region, departement):
    # Si aucune région ni département n'est sélectionné, afficher une jauge vide
    if not region and not departement:
        return go.Figure()
    # Si une région ou un département est sélectionné, calculer les valeurs
    if region:
        nb_installations_pvd = (nb_reg_pvd[nb_reg_pvd["region"] == region])["NbRenouv"].sum()
        nb_installations_total = (nb_reg[nb_reg["region"] == region])["NbRenouv"].sum()
        titre = 'régional'
        lieu = region
    if departement:
        nb_installations_pvd = (nb_dep_pvd[nb_dep_pvd["departement"] == departement])["NbRenouv"].sum()
        nb_installations_total = (nb_dep[nb_dep["departement"] == departement])["NbRenouv"].sum()
        titre = 'départemental'
        lieu = departement
    # Éviter la division par zéro
    pourcentage_pvd = (nb_installations_pvd / nb_installations_total * 100) if nb_installations_total > 0 else 0
    # Créer le graphique de jauge avec les valeurs calculées
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pourcentage_pvd,
        title={'text': f"Niveau {titre} pour {lieu}"},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#f0830e"},  # Couleur de la jauge
            'steps': [
                {'range': [0, 100], 'color': "#d8dce3"}  # Couleur de la partie vide de la jauge
            ],
        }
    ))
    return fig

####################################################
### Graphe - Répartition des filières PVD : ###
####################################################
@callback(
    Output('pie-graph-filiere', 'figure'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value')]
)
def update_graph_pvd(region, departement):
    if not region: 
        return go.Figure()
    if departement:
        df, _ = nb_install_tri(departement, True, True)  
        titre = f"Répartition des filières d'énergies renouvelables au sein des PVD en {departement} ({region})"
    else:
        df, _ = nb_install_tri(region, True, False) 
        titre = f"Répartition des filières d'énergies renouvelables au sein des PVD en {region}"
    df_last = df.iloc[[-1]].melt(
        var_name='filiere',
        value_name='NbRenouv'
    )
    fig = px.pie(
        df_last, 
        names='filiere',      
        values='NbRenouv',    
        title=titre,
    )
    fig.update_traces(marker=dict(colors=[filiere_colors[f] for f in df_last['filiere']]))
    return fig

###############################################################
### Graphe - Evolution nombre d'installations PVD dep/reg : ###
###############################################################
@callback(
    Output('graph-nb-install-totale', 'figure'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value')]
)
def update_graph_totale(region, departement):
    if not region: 
        return go.Figure()
    if departement:
        code = 'departement'
        titre = f"En {departement} ({region})"
        df = nb_dep_pvd[nb_dep_pvd[code] == departement]
    else:
        code = 'region'
        titre = f"En {region}"
        df = nb_reg_pvd[nb_reg_pvd[code] == region]
    df_grouped = df.groupby([code, "dateMiseEnService"], as_index=False).agg({"NbRenouv": "sum"})
    # Création du graphique
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_grouped['dateMiseEnService'],
        y=df_grouped['NbRenouv'],
        mode='lines+markers',
        name=titre,
        line=dict(color='blue', width=2),
        marker=dict(size=6, color='blue', opacity=0.8)
    ))
    fig.update_layout(
        title=titre,
        xaxis_title='Année',
        yaxis_title='Nombre d\'installations',
        template='plotly',
        showlegend=True
    )
    return fig



###################################################################################################################
################################################### Onglet 2 ######################################################
###################################################################################################################
### Classement production : ###
###############################
@callback(
    Output('classement-prod', 'children'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value'),
     Input('choix-pvd', 'value')]
)
def update_classement_prod(region, departement, pvd_selection):
    if pvd_selection:
        # Classement de la PVD :
        ## Dep :
        dep_pvd = prod[prod['departement'] == departement]
        sorted_dep_pvd = pd.DataFrame(dep_pvd.groupby('commune')['energieAnnuelleGlissanteInjectee'].sum().sort_values(ascending=False)).reset_index()
        position_dep_max = sorted_dep_pvd.shape[0]
        sorted_dep_pvd['Rang'] = sorted_dep_pvd['energieAnnuelleGlissanteInjectee'].rank(ascending=False)
        sorted_dep_pvd = sorted_dep_pvd[sorted_dep_pvd['commune'] == pvd_selection]
        position_dep = int(sorted_dep_pvd.iloc[0, 2])
        ## Reg :
        reg_pvd = prod[prod['region'] == region]
        sorted_reg_pvd = pd.DataFrame(reg_pvd.groupby('commune')['energieAnnuelleGlissanteInjectee'].sum().sort_values(ascending=False)).reset_index()
        position_reg_max = sorted_reg_pvd.shape[0]
        sorted_reg_pvd['Rang'] = sorted_reg_pvd['energieAnnuelleGlissanteInjectee'].rank(ascending=False)
        sorted_reg_pvd = sorted_reg_pvd[sorted_reg_pvd['commune'] == pvd_selection]
        position_reg = int(sorted_reg_pvd.iloc[0, 2])
        ## Production : 
        production = sorted_dep_pvd.iloc[0, 1]
        return html.Div([
            html.H3(f"🏆 Classement de la PVD de {pvd_selection} en terme de production électrique:"),
            html.Ul(
                children=[
                    html.Li(f"🏅 Niveau départemental {position_dep}e / {position_dep_max}e"),
                    html.Li(f"🏅 Niveau régional : {position_reg}e / {position_reg_max}e"),
                    html.Li(f"⚡ Production: {production} kWh")],
                style={'list-style-type': 'none'}
            )
        ])
    elif departement:
        # Classement des communes pour un département :
        dep_prod = prod[prod['departement'] == departement]
        sorted_dep = dep_prod.groupby('commune')['energieAnnuelleGlissanteInjectee'].sum().sort_values(ascending=False).head(3)
        return html.Div([
            html.H3(f"🏆 Communes les plus productrices d'énergie renouvelable dans le département {departement}"),
            html.Ul([
                html.Li(f"🥇 {commune} - Production: {prod} kWh") if idx == 0 else
                html.Li(f"🥈 {commune} - Production: {prod} kWh") if idx == 1 else
                html.Li(f"🥉 {commune} - Production: {prod} kWh")
                for idx, (commune, prod) in enumerate(sorted_dep.items())
            ], style={'list-style-type': 'none'})
        ])
    elif region:
        # Classement des départements dans une région :
        reg_prod = prod[prod['region'] == region]
        sorted_reg = reg_prod.groupby('departement')['energieAnnuelleGlissanteInjectee'].sum().sort_values(ascending=False).head(3)
        return html.Div([
            html.H3(f"🏆 Départements les plus productrices d'énergie renouvelable dans la région {region}"),
            html.Ul([
                html.Li(f"🥇 {departement} - Production: {prod} kWh") if idx == 0 else
                html.Li(f"🥈 {departement} - Production: {prod} kWh") if idx == 1 else
                html.Li(f"🥉 {departement} - Production: {prod} kWh")
                for idx, (departement, prod) in enumerate(sorted_reg.items())
            ], style={'list-style-type': 'none'})
        ])
    else:
        # Classement des meilleures régions :
        reg_prod = prod.groupby('region')['energieAnnuelleGlissanteInjectee'].sum().sort_values(ascending=False).head(3)
        return html.Div([
            html.H3("🏆 Régions les plus productrices d'énergie renouvelable en France"),
            html.Ul([
                html.Li(f"🥇 {region} - Production: {prod} kWh") if idx == 0 else
                html.Li(f"🥈 {region} - Production: {prod} kWh") if idx == 1 else
                html.Li(f"🥉 {region} - Production: {prod} kWh")
                for idx, (region, prod) in enumerate(reg_prod.items())
            ], style={'list-style-type': 'none'})
        ])
        
#####################################
#### Graphe part de production : ####
#####################################
@callback(
    Output('gauge-chart-prod', 'figure'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value')])
def update_gauge_prod(region, departement):
    if not region and not departement:
        return go.Figure()
    if region:
        qtt_prod_total = (prod[prod["region"] == region])['energieAnnuelleGlissanteInjectee'].sum()
        qtt_prod_pvd = (prod[prod["region"] == region])
        qtt_prod_pvd = (qtt_prod_pvd[qtt_prod_pvd["commune"].isin(pvd['commune'])])['energieAnnuelleGlissanteInjectee'].sum()
        titre = 'régional'
        lieu = region
    if departement:
        qtt_prod_total = (prod[prod["departement"] == departement])['energieAnnuelleGlissanteInjectee'].sum()
        qtt_prod_pvd = (prod[prod["departement"] == departement])
        qtt_prod_pvd = (qtt_prod_pvd[qtt_prod_pvd["commune"].isin(pvd['commune'])])['energieAnnuelleGlissanteInjectee'].sum()
        titre = 'départemental'
        lieu = departement
    pourcentage_pvd = (qtt_prod_pvd / qtt_prod_total * 100) if qtt_prod_total > 0 else 0
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pourcentage_pvd,
        title={'text': f"Niveau {titre} pour {lieu}"},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#31b52a"},  # Couleur de la jauge
            'steps': [
                {'range': [0, 100], 'color': "#d8dce3"}  # Couleur de la partie vide de la jauge
            ],
        }
    ))
    return fig

#################################
### Classement consommation : ###
#################################
@callback(
    Output('classement-conso', 'children'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value'),
     Input('choix-pvd', 'value')]
)
def update_podium_conso(region, departement, pvd_selection):
    if pvd_selection:
        # Classement de la PVD :
        ## Dep :
        dep_pvd = conso[conso['Nom Département'] == departement]
        sorted_dep_pvd = pd.DataFrame(dep_pvd.groupby('commune')['Conso totale (MWh)'].sum().sort_values(ascending=False)).reset_index()
        position_dep_max = sorted_dep_pvd.shape[0]
        sorted_dep_pvd['Rang'] = sorted_dep_pvd['Conso totale (MWh)'].rank(ascending=False)
        sorted_dep_pvd = sorted_dep_pvd[sorted_dep_pvd['commune'] == pvd_selection]
        position_dep = int(sorted_dep_pvd.iloc[0, 2])
        ## Reg :
        reg_pvd = conso[conso['Nom Région'] == region]
        sorted_reg_pvd = pd.DataFrame(reg_pvd.groupby('commune')['Conso totale (MWh)'].sum().sort_values(ascending=False)).reset_index()
        position_reg_max = sorted_reg_pvd.shape[0]
        sorted_reg_pvd['Rang'] = sorted_reg_pvd['Conso totale (MWh)'].rank(ascending=False)
        sorted_reg_pvd = sorted_reg_pvd[sorted_reg_pvd['commune'] == pvd_selection]
        position_reg = int(sorted_reg_pvd.iloc[0, 2])
        ## Consommation :
        consommation = sorted_dep_pvd.iloc[0, 1]
        return html.Div([
            html.H3(f"🏆 Classement de la PVD de {pvd_selection} en terme de consommation électrique:"),
            html.Ul(
                children=[
                    html.Li(f"🔌 Niveau départemental {position_dep}e / {position_dep_max}e"),
                    html.Li(f"🔌 Niveau régional : {position_reg}e / {position_reg_max}e"),
                    html.Li(f"🔋 Consommation: {consommation} kWh")],
                style={'list-style-type': 'none'}
            )
        ])
    elif departement:
        # Classement des communes pour un département :
        dep_conso = conso[conso['Nom Département'] == departement]
        sorted_dep = dep_conso.groupby('commune')['Conso totale (MWh)'].sum().sort_values(ascending=False).head(3)
        return html.Div([
            html.H3(f"🏆 Communes les plus consommatrice d'énergie dans le département {departement}"),
            html.Ul([
                html.Li(f"🥇 {commune} - Consommation: {conso*100} kWh") if idx == 0 else
                html.Li(f"🥈 {commune} - Consommation: {conso*100} kWh") if idx == 1 else
                html.Li(f"🥉 {commune} - Consommation: {conso*100} kWh")
                for idx, (commune, conso) in enumerate(sorted_dep.items())
            ], style={'list-style-type': 'none'})
        ])
    elif region:
        # Classement des départements dans une région :
        reg_conso = conso[conso['Nom Région'] == region]
        sorted_reg = reg_conso.groupby('Nom Département')['Conso totale (MWh)'].sum().sort_values(ascending=False).head(3)
        return html.Div([
            html.H3(f"🏆 Départements les plus consommateurs d'énergie dans la région {region}"),
            html.Ul([
                html.Li(f"🥇 {departement} - Consommation: {(conso*100)/12} kWh") if idx == 0 else
                html.Li(f"🥈 {departement} - Consommation: {(conso*100)/12} kWh") if idx == 1 else
                html.Li(f"🥉 {departement} - Consommation: {(conso*100)/12} kWh")
                for idx, (departement, conso) in enumerate(sorted_reg.items())
            ], style={'list-style-type': 'none'})
        ])
    else:
        # Classement des meilleures régions :
        reg_conso = conso.groupby('Nom Région')['Conso totale (MWh)'].sum().sort_values(ascending=False).head(3)
        return html.Div([
            html.H3("🏆 Régions les plus consommatrices d'énergie renouvelable en France"),
            html.Ul([
                html.Li(f"🥇 {region} - Consommation: {(conso*100)/12} kWh") if idx == 0 else
                html.Li(f"🥈 {region} - Consommation: {(conso*100)/12} kWh") if idx == 1 else
                html.Li(f"🥉 {region} - Consommation: {(conso*100)/12} kWh")
                for idx, (region, conso) in enumerate(reg_conso.items())
            ], style={'list-style-type': 'none'})
        ])

#####################################
### Graphe part de consommation : ###
#####################################
@callback(
    Output('gauge-chart-conso', 'figure'),
    [Input('choix-region', 'value'),
     Input('choix-departement', 'value')])
def update_gauge_conso(region, departement):
    if not region and not departement:
        return go.Figure()
    if region:
        qtt_conso_total = (conso[conso["Nom Région"] == region])['Conso totale (MWh)'].sum()
        qtt_conso_pvd = (conso[conso["Nom Région"] == region])
        qtt_conso_pvd = (qtt_conso_pvd[qtt_conso_pvd["commune"].isin(pvd['commune'])])['Conso totale (MWh)'].sum()
        titre = 'régional'
        lieu = region
    if departement:
        qtt_conso_total = (conso[conso["Nom Département"] == departement])['Conso totale (MWh)'].sum()
        qtt_conso_pvd = (conso[conso["Nom Département"] == departement])
        qtt_conso_pvd = (qtt_conso_pvd[qtt_conso_pvd["commune"].isin(pvd['commune'])])['Conso totale (MWh)'].sum()
        titre = 'départemental'
        lieu = departement
    pourcentage_pvd = (qtt_conso_pvd / qtt_conso_total * 100) if qtt_conso_total > 0 else 0
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pourcentage_pvd,
        title={'text': f"Niveau {titre} pour {lieu}"},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#e30733"},  # Couleur de la jauge
            'steps': [
                {'range': [0, 100], 'color': "#d8dce3"}  # Couleur de la partie vide de la jauge
            ],
        }
    ))
    return fig
