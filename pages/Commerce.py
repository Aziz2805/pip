import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from utils.pretraitement import (
    load_data_commerces,
    load_PVD_infos,
    load_data_commerces_typesCleaned,
)


dash.register_page(__name__, path='/commerces', order = 4, display_name = "🛍️ Commerce")


# ========= 1) Chargement des données =============

df_com = load_data_commerces()
df_ville = load_PVD_infos()
da_com = load_data_commerces_typesCleaned()

ville_com = pd.merge(df_ville, df_com, left_on="insee_com", right_on="com_insee") # jointure commerce et pvd
villa_com = pd.merge(df_ville, da_com, left_on="insee_com", right_on="com_insee") # jointure commerce et pvd avec types regroupé 

# convertit les dates si nécessaire
if "date_signature" in ville_com.columns:
    ville_com["date_signature"] = pd.to_datetime(ville_com["date_signature"], errors="coerce")



# ========== 3) Création des onglets (Tabs) ========



tabs = dcc.Tabs(
    id="main-tabs",
    value="kpi",  # onglet par défaut
    children=[
        dcc.Tab(label="PVD", value="kpi",),
        dcc.Tab(label="Commerces", value="commerces"),
        dcc.Tab(label="Départements", value="departements"),
        dcc.Tab(label="Explorer", value="explorer"),
        dcc.Tab(label="Comparatif Communes", value="comparative_communes"),
        dcc.Tab(label="À propos", value="about"),
    ]
)

# Un conteneur pour le contenu dynamique des onglets
content = html.Div(id="tab-content")


# ========== 4) Layout global ======================
layout = html.Div([
    dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(html.H1("Commerce")),
            html.Div(
                style={'height': '10px', 'background-color': '#4CAF50', 'margin-bottom': '10px', 'margin-top': '10px'}
            )
        ]),
        dbc.Row([
            dbc.Col(tabs, width=12)
        ]),
        dbc.Row([
            dbc.Col(content, width=12)
        ])
    ])
])



# ========== 5) Générer le layout par onglet =======
def render_tab_content(tab):
    """
    Fonction qui retourne le layout Dash correspondant à la valeur de l'onglet sélectionné
    (similaire à la logique tabItem(...) dans Shiny).
    """
    if tab == "kpi": 
        return dbc.Container([
            # Première rangée de "valueBox"
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Total des commerces", className="card-title"),
                        html.H2(id="total_commerces", className="card-text")
                    ])
                ], color="primary", inverse=True), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Type dominant", className="card-title"),
                        html.H2(id="dominant_type", className="card-text")
                    ])
                ], color="success", inverse=True), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Région la plus active", className="card-title"),
                        html.H2(id="top_region", className="card-text")
                    ])
                ], color="dark", inverse=True), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Département le plus actif", className="card-title"),
                        html.H2(id="top_departement", className="card-text")
                    ])
                ], color="warning", inverse=True), width=3),
            ]),

            # Deuxième rangée de "valueBox"
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Période la plus active (2020-2024)", className="card-title"),
                        html.H2(id="period_2020_2024", className="card-text")
                    ])
                ], color="secondary", inverse=True), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Nombre de départements", className="card-title"),
                        html.H2(id="total_departements", className="card-text")
                    ])
                ], color="info", inverse=True), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Nombre de régions", className="card-title"),
                        html.H2(id="total_regions", className="card-text")
                    ])
                ], color="danger", inverse=True), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Nombre de communes", className="card-title"),
                        html.H2(id="total_communes", className="card-text")
                    ])
                ], color="purple", inverse=True), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Commune la plus active", className="card-title"),
                        html.H2(id="top_commune", className="card-text")
                    ])
                ], color="pink", inverse=True), width=3),
            ]),
        ], fluid=True)

    elif tab == "commerces":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Graph(id="hist_types"), width=12),
                
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="top_10_commerces"), width=6),
                dbc.Col(dcc.Graph(id="trend_commerces"), width=6),
            ])
        ], fluid=True)

    elif tab == "departements":
        return dbc.Container([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id="selected_dept",
                        options=[{"label": d, "value": d} for d in sorted(villa_com["Nom Officiel Département"].unique())],
                        value=sorted(villa_com["Nom Officiel Département"].unique())[0],
                        placeholder="Choisir un département",
                    ), width=6
                ),
                dbc.Col(dcc.Graph(id="concentration_dept"), width=12),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="repartition_types_dept"), width=12),
            ])
        ], fluid=True)

    elif tab == "explorer": 
        return dbc.Container([
        html.H3("Explorer les commerces par région, département et commune"),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id="explore_region",
                    options=[{"label": r, "value": r} for r in sorted(ville_com["Nom Officiel Région"].unique())],
                    value=sorted(ville_com["Nom Officiel Région"].unique())[0],
                    placeholder="Choisir une région"
                ), width=4
            ),
            dbc.Col(
                dcc.Dropdown(id="explore_dept", placeholder="Choisir un département"),
                width=4
            ),
            dbc.Col(
                dcc.Dropdown(id="explore_commune", placeholder="Choisir une commune"),
                width=4
            ),
        ]),
        dbc.Row([
             dbc.Col(dcc.Graph(id="explore_map"), width=12),
            
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="explore_commerce_distribution"), width=6),
            dbc.Col(dcc.Graph(id="explore_top_types"), width=6),
            
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="explore_category_distribution"), width=6),
            dbc.Col(dcc.Graph(id="diversity_commune"), width=6),
        ])
    ], fluid=True)

    elif tab == "comparative_communes":
        return dbc.Container([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id="compare_commune1",
                        options=[{"label": c, "value": c} for c in sorted(ville_com["com_nom"].unique())],
                        value=sorted(ville_com["com_nom"].unique())[0],
                        placeholder="Commune 1"
                    ), width=6
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="compare_commune2",
                        options=[{"label": c, "value": c} for c in sorted(df_com["com_nom"].unique())],
                        value=sorted(df_com["com_nom"].unique())[1],
                        placeholder="Commune 2"
                    ), width=6
                ),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="commune_comparison_chart"), width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="commune1_wordcloud"), width=6),
                dbc.Col(dcc.Graph(id="commune2_wordcloud"), width=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="commune1_div"), width=6),
                dbc.Col(dcc.Graph(id="commune2_div"), width=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="commune1_chaine"), width=6),
                dbc.Col(dcc.Graph(id="commune2_chaine"), width=6),
            ])
        ], fluid=True)

    elif tab == "about":
        return dbc.Container([
            html.H3("Description du tableau de bord"),
            html.P("Ce tableau de bord présente des analyses sur les types de commerces dans l'ensemble des Petites Villes de Demain (PVD)."),
            html.P("Les principales fonctionnalités comprennent la répartition des types de commerces par commune (PVD) et par département, ainsi qu'une comparaison entre communes selon les types de commerces."),
            html.P("Le but est de permettre une exploration interactive des données, offrant aux utilisateurs une meilleure compréhension des dynamiques commerciales locales et des spécificités territoriales."),
            html.P("Des visualisations intuitives et des outils de filtrage facilitent l'identification des tendances, aidant ainsi les décideurs locaux à orienter leurs stratégies."),

        ], fluid=True)
    
    
    return html.Div() # Si aucun onglet ne correspond, on renvoie un contenu vide


# ========== 6) Callback pour mettre à jour le layout de chaque onglet ==========

@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value")
)
def update_tab_content(selected_tab):
    return render_tab_content(selected_tab)

# ========== 7) Callbacks pour les PVD (onglet "kpi") ===========================
@app.callback(
    Output("total_regions", "children"),
    Output("total_departements", "children"),
    Output("total_communes", "children"),
    Output("total_commerces", "children"),
    Output("dominant_type", "children"),
    Output("top_commune", "children"),
    Output("top_departement", "children"),
    Output("top_region", "children"),
    Output("period_2020_2024", "children"),
    Input("main-tabs", "value")  # Utilisation de l'onglet pour “déclencher” la mise à jour
)
def update_kpi_values(tab):
    """
    Met à jour les indicateurs clés de performance (KPI).
    """
    if tab != "kpi":
        # Si on n'est pas sur l'onglet KPI, renvoyer des chaînes vides
        return [""] * 9

    df = ville_com.copy()

    # 1) Total des régions
    if "Nom Officiel Région" in df.columns:
        total_regions = df["Nom Officiel Région"].nunique()
    else:
        total_regions = 0

    # 2) Total des départements
    if "Nom Officiel Département" in df.columns:
        total_departements = df["Nom Officiel Département"].nunique()
    else:
        total_departements = 0

    # 3) Total des communes
    if "lib_com" in df.columns:
        total_communes = df["lib_com"].nunique()
    else:
        total_communes = 0

    # 4) Total des commerces
    total_commerces = len(df)

    # 5) Type dominant
    if "type" in df.columns and not df.empty:
        dominant_type = df["type"].value_counts().idxmax()
    else:
        dominant_type = "N/A"

    # 6) Commune avec le plus de commerces
    if "lib_com" in df.columns and not df.empty:
        top_commune = df["lib_com"].value_counts().idxmax()
    else:
        top_commune = "N/A"

    # 7) Département avec le plus de commerces
    if "Nom Officiel Département" in df.columns and not df.empty:
        top_departement = df["Nom Officiel Département"].value_counts().idxmax()
    else:
        top_departement = "N/A"

    # 8) Région avec le plus de commerces
    if "Nom Officiel Région" in df.columns and not df.empty:
        top_region = df["Nom Officiel Région"].value_counts().idxmax()
    else:
        top_region = "N/A"

    # 9) Période la plus active (2020-2024)
    if "date_signature" in df.columns:
        df_2020_2024 = df[
            (df["date_signature"].dt.year >= 2020) &
            (df["date_signature"].dt.year <= 2024)
        ]
        if not df_2020_2024.empty:
            active_period = int(df_2020_2024["date_signature"].dt.year.value_counts().idxmax())
        else:
            active_period = "N/A"
    else:
        active_period = "N/A"

    return (
        str(total_regions),      # 1
        str(total_departements), # 2
        str(total_communes),     # 3
        str(total_commerces),    # 4
        str(dominant_type),      # 5
        str(top_commune),        # 6
        str(top_departement),    # 7
        str(top_region),         # 8
        str(active_period),      # 9
)



# ========== 8) Callbacks pour l’onglet "commerces" =========================

@app.callback(
    Output("hist_types", "figure"),
    Output("trend_commerces", "figure"),
    Output("top_10_commerces", "figure"),
    Input("main-tabs", "value")
)
def update_commerces_charts(tab):
    """
    Regroupe les 3 graphiques de l'onglet "Commerces" dans un seul callback.
    """
    if tab != "commerces":
        return go.Figure(), go.Figure(), go.Figure()

    df = ville_com.copy()

   # diagramme des types
    df_type_count = df["type"].value_counts().reset_index()
    df_type_count.columns = ["type", "count"]  # Adapter le nom de la colonne correctement

    fig_treemap = px.treemap(
    df_type_count,
    path=["type"],
    values="count",  # Utiliser le nom correct de la colonne
    title="Répartition des types de commerces dans l'ensemble des PVD ",
    color="count",  # Optionnel : colorer les rectangles en fonction des valeurs
    color_continuous_scale="Viridis"
)




    # Tendance par année (cumulative)
    if "date_signature" in df.columns:
        df["year"] = df["date_signature"].dt.year
        df_year_count = df["year"].value_counts().reset_index()
        df_year_count.columns = ["year", "n"]
        df_year_count = df_year_count.sort_values("year")
        df_year_count["cumulative"] = df_year_count["n"].cumsum()
    else:
        df_year_count = pd.DataFrame({"year": [], "cumulative": []})

    fig_trend = go.Figure()
    if not df_year_count.empty:
        fig_trend = px.line(
            df_year_count,
            x="year",
            y="cumulative",
            markers=True,
            title="Croissance du nombre de commerces annuellement"
        )
        fig_trend.update_layout(xaxis_title="Année", yaxis_title="Effectifs cumulés")

    # Top 10 des types (diagramme circulaire)
    df_top_10 = df_type_count.head(10)
    fig_top_10 = go.Figure()

    if not df_top_10.empty:
       fig_top_10 = px.pie(
        df_top_10,
        names="type",
        values="count",  # Utiliser le nom correct de la colonne
        title="Top 10 des types de commerces",
        color="type",
    )



    return fig_treemap, fig_trend, fig_top_10

# ========== 9) Callbacks pour l’onglet "departements" ======================

@app.callback(
    Output("concentration_dept", "figure"),
    Output("repartition_types_dept", "figure"),
    Input("main-tabs", "value"),
    Input("selected_dept", "value")
)
def update_dept_charts(tab, selected_dept):
    if tab != "departements" or selected_dept is None:
        return go.Figure(), go.Figure()

    df = villa_com[villa_com["Nom Officiel Département"] == selected_dept].copy()
    if df.empty:
        return go.Figure(), go.Figure()

    # 1) concentration_dept
    ## Bar chart empilé pour plusieurs communes
    df_stacked = df.groupby(["lib_com", "type"]).size().reset_index(name="count")
    fig_stacked = px.bar(
    df_stacked,
    x="lib_com",
    y="count",
    color="type",
    title=f"Répartition des types de commerces par commune pour le departement de {selected_dept}",
    labels={"lib_com": "Commune", "count": "Nombre de commerces", "type": "Type de commerce"}
)

    # 2) repartition_types_dept (top 10)
    df_dept_count = df["type"].value_counts().reset_index()
    df_dept_count.columns = ["type", "n"]
    df_dept_top10 = df_dept_count.head(10)
    fig_repartition = px.pie(
        df_dept_top10,
        names="type",
        values="n",
        title="Répartition des 10 principaux types de commerces"
)

    return fig_stacked, fig_repartition

# ========== 12) Callbacks Explorer (cascade Région -> Dept -> Commune) =====

@app.callback(
    Output("explore_dept", "options"),
    Output("explore_dept", "value"),
    Input("explore_region", "value")
)
def update_dept_options(selected_region):
    """ Met à jour la liste des départements en fonction de la région choisie. """
    if not selected_region:
        return [], None
    df_region = ville_com[ville_com["Nom Officiel Région"] == selected_region]
    depts = sorted(df_region["Nom Officiel Département"].unique())
    opts = [{"label": d, "value": d} for d in depts]
    val = depts[0] if len(depts) > 0 else None
    return opts, val

@app.callback(
    Output("explore_commune", "options"),
    Output("explore_commune", "value"),
    Input("explore_region", "value"),
    Input("explore_dept", "value")
)
def update_commune_options(selected_region, selected_dept):
    """ Met à jour la liste des communes en fonction du département choisi. """
    if not selected_region or not selected_dept:
        return [], None
    df_dept = ville_com[
        (ville_com["Nom Officiel Région"] == selected_region) &
        (ville_com["Nom Officiel Département"] == selected_dept)
    ]
    communes = sorted(df_dept["lib_com"].unique())
    opts = [{"label": c, "value": c} for c in communes]
    val = communes[0] if len(communes) > 0 else None
    return opts, val

@app.callback(
    Output("explore_commerce_distribution", "figure"),
    Output("explore_top_types", "figure"),
    Output("diversity_commune", "figure"),
    Output("explore_map", "figure"),
    Output("explore_category_distribution", "figure"),
    Input("explore_region", "value"),
    Input("explore_dept", "value"),
    Input("explore_commune", "value"),
    Input("main-tabs", "value")
)
def update_explorer_charts(region, dept, commune, tab):
    if tab != "explorer":
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure

    if not commune:
        return go.Figure(), go.Figure(), go.Figure(),go.Figure(), go.Figure

    df = ville_com[
        (ville_com["Nom Officiel Région"] == region) &
        (ville_com["Nom Officiel Département"] == dept) &
        (ville_com["lib_com"] == commune)
    ]
    if df.empty:
        return go.Figure(), go.Figure(), go.Figure(),go.Figure(), go.Figure

    # 1) Distribution (bar chart)
    df_count = df["type"].value_counts().reset_index()
    df_count.columns = ["type", "n"]
    fig_dist = px.bar(
    df_count,
    x="type",    # Les types de commerces
    y="n",       # Le nombre de commerces pour chaque type
    title=f"Répartition des types de  commerces à {commune}",
    labels={"type": "Type de commerce", "n": "Nombre de commerces"}
    )
    # 2) Top types (pie chart)
    df_top = df_count.head(10).sort_values("n", ascending=True)
    fig_top = px.pie(
    df_top,
    names="type",  # Les types de commerces
    values="n",    # Le nombre de commerces pour chaque type
    title=f"Top 10 des types de commerces à {commune}"
    )
    # 3) Map of commerce locations
    fig_map = px.scatter_mapbox(
        df,
        lat="Y",
        lon="X",
        hover_name="name",
        hover_data={"type": True, "address": True},
        color="type",
        zoom=12,
        title=f"Localisation des commerces à {commune}",
        labels={"type": "Type de commerce"}
    )
    fig_map.update_layout(mapbox_style="open-street-map")

    # 1) Diversité
    total_types_commerce = ville_com['type'].nunique()
    types_par_commune = df['type'].nunique()
    diversite_commune = (types_par_commune / total_types_commerce) * 100

    # 1) Diagramme en anneau
    fig_diversite = px.pie(
    values=[diversite_commune, 100 - diversite_commune],
    names=["Diversité des commerces", "Manque de diversité"],
    color_discrete_sequence=["skyblue", "orange"],
    title=f"Diversité des types de commerces à {commune}"
)
    fig_diversite.update_traces(hole=0.4, textinfo="percent+label")

    # 5) Répartition Grandes chaînes vs Indépendants
    df["category"] = df["brand"].apply(lambda x: "Grande chaîne" if pd.notna(x) else "Commerce indépendant")
    category_counts = df["category"].value_counts(normalize=True)
    fig_category = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title=f"Répartition des types commerces : Grandes chaînes vs Indépendants à {commune}",
        color_discrete_map={"Grande chaîne": "yellow", "Commerce indépendant": "purple"}
    )

    return fig_dist.to_dict(), fig_top.to_dict(), fig_diversite.to_dict(), fig_map.to_dict(), fig_category.to_dict()


# ========== 13) Callbacks comparatif communes ==============================
@app.callback(
    Output("commune_comparison_chart", "figure"),
    Output("commune1_wordcloud", "figure"),
    Output("commune2_wordcloud", "figure"),
    Output("commune1_div", "figure"),
    Output("commune2_div", "figure"),
    Output("commune1_chaine", "figure"),
    Output("commune2_chaine", "figure"),
    Input("compare_commune1", "value"),
    Input("compare_commune2", "value"),
    Input("main-tabs", "value")
)
def update_compare_communes_chart(commune1, commune2, tab):
    # Vérification si l'onglet est incorrect
    if tab != "comparative_communes":
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()

    # Vérification si une commune est manquante
    if not commune1 or not commune2:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()
    df=ville_com.copy()
    # Fonction utilitaire pour calculer diversité et répartition des catégories
    def calculate_diversity_and_category(commune_df):
        total_types_commerce = df["type"].nunique()
        types_par_commune = commune_df["type"].nunique()
        diversite_commune = (types_par_commune / total_types_commerce) * 100

        # Répartition Grandes chaînes vs Indépendants
        commune_df["category"] = commune_df["brand"].apply(
            lambda x: "Grande chaîne" if pd.notna(x) else "Commerce indépendant"
        )
        category_counts = commune_df["category"].value_counts(normalize=True)

        return diversite_commune, category_counts

    # Chargement des données pour chaque commune
    commune1_df = ville_com[ville_com["com_nom"] == commune1]
    commune2_df = df_com[df_com["com_nom"] == commune2]

    # Création du bar chart comparatif
    df1 = commune1_df["type"].value_counts().reset_index()
    df1.columns = ["type", "n_commune1"]

    df2 = commune2_df["type"].value_counts().reset_index()
    df2.columns = ["type", "n_commune2"]

    df_merged = pd.merge(df1, df2, on="type", how="outer").fillna(0)

    fig_compare = go.Figure()
    fig_compare.add_bar(x=df_merged["type"], y=df_merged["n_commune1"], name=commune1)
    fig_compare.add_bar(x=df_merged["type"], y=df_merged["n_commune2"], name=commune2)
    fig_compare.update_layout(
        barmode="group",
        title=f"Comparaison des types de commerces entre {commune1} et {commune2}",
        xaxis_title="Type de commerce",
        yaxis_title="Nombre de commerces"
    )

    # Diagrammes circulaires des top 10 types
    fig_c1 = px.pie(
        df1.sort_values("n_commune1", ascending=False).head(10),
        names="type",
        values="n_commune1",
        title=f"Top 10 des commerces dans {commune1}"
    )
    fig_c2 = px.pie(
        df2.sort_values("n_commune2", ascending=False).head(10),
        names="type",
        values="n_commune2",
        title=f"Top 10 des commerces dans {commune2}"
    )

    # Calculs diversité et répartition pour commune1
    diversite1, category_counts1 = calculate_diversity_and_category(commune1_df)
    fig_div1 = px.pie(
        values=[diversite1, 100 - diversite1],
        names=["Diversité des commerces", "Manque de diversité"],
        color_discrete_sequence=["skyblue", "orange"],
        title=f"Diversité des types de commerces à {commune1}"
    )
    fig_div1.update_traces(hole=0.4, textinfo="percent+label")

    fig_cat1 = px.pie(
        values=category_counts1.values,
        names=category_counts1.index,
        title=f"Grandes chaînes vs Indépendants à {commune1}",
        color_discrete_map={"Grande chaîne": "yellow", "Commerce indépendant": "purple"}
    )

    # Calculs diversité et répartition pour commune2
    diversite2, category_counts2 = calculate_diversity_and_category(commune2_df)
    fig_div2 = px.pie(
        values=[diversite2, 100 - diversite2],
        names=["Diversité des commerces", "Manque de diversité"],
        color_discrete_sequence=["skyblue", "orange"],
        title=f"Diversité des types de commerces à {commune2}"
    )
    fig_div2.update_traces(hole=0.4, textinfo="percent+label")

    fig_cat2 = px.pie(
        values=category_counts2.values,
        names=category_counts2.index,
        title=f"Grandes chaînes vs Indépendants à {commune2}",
        color_discrete_map={"Grande chaîne": "yellow", "Commerce indépendant": "purple"}
    )

    # Retour des figures pour tous les graphes
    return (
        fig_compare.to_dict(),  # Comparaison
        fig_c1.to_dict(),      # Wordcloud commune1
        fig_c2.to_dict(),      # Wordcloud commune2
        fig_div1.to_dict(),    # Diversité commune1
        fig_div2.to_dict(),    # Diversité commune2
        fig_cat1.to_dict(),    # Grandes chaînes vs Indépendants commune1
        fig_cat2.to_dict()     # Grandes chaînes vs Indépendants commune2
    )