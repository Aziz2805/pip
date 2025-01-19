from dash import Dash, html, dcc, Input, Output, callback

import json
import dash
import pandas as pd


from dash import dcc
import plotly.graph_objects as go

from dash import html, Input, Output
import plotly.express as px

from shapely.geometry import shape

from utils.pretraitement import(
    load_PVD_infos_2,
    load_contours,
)


dash.register_page(__name__, path='/departements', order = 3, display_name = '🌎 Visualisation Départementale')

geojson_data_dep , geojson_data_com = load_contours()

# Extraction des propriétés GeoJSON
features_dep = geojson_data_dep['features']
features_com = geojson_data_com['features']

# Liste des départements
locations = [
    {
        "name": feature["properties"].get("NOM", "Unknown"),
        "insee": feature["properties"].get("INSEE_DEP", "Unknown"),
    }
    for feature in features_dep
]

# Chargement des fichiers CSV
pvd = load_PVD_infos_2()


# Layout principal
layout = html.Div(

    style={"display": "flex", "height": "100%", "gap": "10px", "padding": "10px"},
    children=[
        # Carte des départements
        html.Div(
            style={"flex": "1", "display": "flex", "flex-direction": "column", "gap": "10px"},
            children=[
                html.Div(
                    style={
                        "flex": "1",
                        "background-color": "#c3e6cb",
                        "border-radius": "5px",
                    },
                    children=[html.Div(id="output", style={"marginTop": "2px"})]
                ),
                html.Label("Sélectionnez la département :"),
                dcc.Dropdown(
                    id="dep-dropdown",
                    options=[
                        {"label": location["name"], "value": location["insee"]}
                        for location in locations
                    ],
                    value=None,
                    clearable=True,
                    placeholder="Sélectionnez une département"
                ),

                html.Div(
                    style={
                        "flex": "5",
                        "background-color": "#d1ecf1",
                        "border-radius": "5px",
                    },
                    children=[dcc.Graph(
                        id="map",
                        config={"scrollZoom": False},
                        style={"width": "100%", "height": "100%", "margin": "0", "padding": "0"}
                    ),
                        dcc.Store(id="insee_department", storage_type="memory")
                    ]
                ),

            ],
        ),

        html.Div(
            style={"flex": "1", "display": "flex", "flex-direction": "column", "gap": "10px"},
            children=[
                html.Div(
                    style={
                        "flex": "8",
                        "background-color": "#c3e6cb",
                        "border-radius": "5px",
                    },
                    children=[dcc.Graph(
                        id="map_dep",
                        config={"scrollZoom": False},
                        style={"width": "100%", "height": "100%", "margin": "0", "padding": "0"}
                    )]
                ),
                html.Div(
                    style={
                        "flex": "7",
                        "background-color": "#d1ecf1",
                        "border-radius": "5px",
                    },
                    children=[html.Div(id="timeline_gragh", style={"marginTop": "2px"})]
                ),

            ],
        ),

        html.Div(
            style={"flex": "1", "display": "flex", "flex-direction": "column", "gap": "10px"},
            children=[
                html.Div(
                    style={
                        "flex": "1",
                        "background-color": "#ffeeba",
                        "border-radius": "5px",
                    },
                    children=[html.Div(id="Chart_gragh", style={"marginTop": "2px"})]
                ),

            ],
        ),
    ],
)

@callback(
    [Output("map", "figure"), Output("insee_department", "data"), Output("dep-dropdown", "value")],
    [Input("map", "clickData"), Input("dep-dropdown", "value")],
)
def update_map_nation_and_dropdown(click_data, dropdown_value):
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]["prop_id"] if ctx.triggered else None

    # 初始化颜色映射
    colors = {feature["properties"]["INSEE_DEP"]: "blue" for feature in features_dep}
    selected_insee = None

    # 如果点击了地图
    if triggered_input == "map.clickData" and click_data:
        selected_insee = click_data["points"][0]["location"]
        colors[selected_insee] = "red"

    # 如果选择了下拉菜单
    elif triggered_input == "dep-dropdown.value":
        selected_insee = dropdown_value
        if selected_insee:  # 确保选中值不为空
            colors[selected_insee] = "red"

    # 如果没有任何触发，且下拉菜单为空，不进行强制默认值
    if not selected_insee and dropdown_value is None:
        # 保持地图颜色为默认状态
        fig = px.choropleth_mapbox(
            geojson=geojson_data_dep,
            locations=list(colors.keys()),
            color=list(colors.values()),
            featureidkey="properties.INSEE_DEP",
            mapbox_style="open-street-map",
            center={"lat": 46.603354, "lon": 1.988334},  # 法国中心坐标
            zoom=4.6,
            opacity=0.5,
            color_discrete_map={"blue": "blue", "red": "red"})  # 离散颜色映射
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False  # 禁用图例显示

        )

        # 返回地图、None（没有选中值）和 None（保持下拉为空）
        return fig, None, None

    # 更新地图
    fig = px.choropleth_mapbox(
        geojson=geojson_data_dep,
        locations=list(colors.keys()),
        color=list(colors.values()),
        featureidkey="properties.INSEE_DEP",
        mapbox_style="open-street-map",
        center={"lat": 46.603354, "lon": 1.988334},  # 法国中心坐标
        zoom=4.6,
        opacity=0.5,
        color_discrete_map={"blue": "blue", "red": "red"}  # 离散颜色映射
    )

    # 更新地图布局
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False  # 禁用图例显示
    )

    # 返回地图、选中的 INSEE 值和下拉菜单值
    return fig, selected_insee, selected_insee


@callback(
    Output("map_dep", "figure"),
    Input("insee_department", "data")
)

def update_map_dep(insee_dep):
    # 过滤 GeoJSON 数据
    filtered_geojson = {
        "type": "FeatureCollection",
        "features": [
            feature for feature in geojson_data_com["features"]
            if feature["properties"].get("INSEE_DEP") == insee_dep
        ]
    }

    # 默认的中心点和缩放级别
    default_center = {"lat": 46.603354, "lon": 1.988334}
    default_zoom = 6

    # 如果没有匹配的数据，返回空地图
    if not filtered_geojson["features"]:
        fig = px.choropleth_mapbox(
            geojson={"type": "FeatureCollection", "features": []},
            locations=[],
            mapbox_style="open-street-map",
            center=default_center,
            zoom=default_zoom,
            opacity=0.5
        )
    else:
        # 计算边界框
        geometries = [shape(feature["geometry"]) for feature in filtered_geojson["features"]]
        min_lon = min(geom.bounds[0] for geom in geometries)
        min_lat = min(geom.bounds[1] for geom in geometries)
        max_lon = max(geom.bounds[2] for geom in geometries)
        max_lat = max(geom.bounds[3] for geom in geometries)

        # 计算中心点
        center_lon = (min_lon + max_lon) / 2
        center_lat = (min_lat + max_lat) / 2

        # 计算缩放级别
        map_width, map_height = 90, 90  # 假设地图容器的宽度和高度
        lon_diff = max_lon - min_lon
        lat_diff = max_lat - min_lat
        zoom = min(
            max(0, 8 - (lon_diff / 360) * map_width),
            max(0, 8 - (lat_diff / 180) * map_height)
        )

        # PVD 数据过滤
        filtered_pvd_df = pvd[
            pvd["Code Officiel Département"] == insee_dep
            ]
        pvd_insee_codes = set(filtered_pvd_df["insee_com"].values)

        # 为每个 INSEE_COM 设置类别
        categories = {
            feature["properties"]["INSEE_COM"]: "PVD" if feature["properties"][
                                                             "INSEE_COM"] in pvd_insee_codes else "Non PVD"
            for feature in filtered_geojson["features"]
        }

        # 创建地图图形
        fig = px.choropleth_mapbox(
            geojson=filtered_geojson,
            locations=list(categories.keys()),
            color=list(categories.values()),
            featureidkey="properties.INSEE_COM",
            mapbox_style="open-street-map",
            center={"lat": center_lat, "lon": center_lon},
            zoom=zoom,
            opacity=0.5,
            color_discrete_map={"PVD": "red", "Non PVD": "blue"}
        )

    # 更新布局，确保图例和边距一致
    fig.update_layout(
        title={
            "text": "Carte de la répartition des PVD",
            "y": 0.95,  # 标题垂直位置
            "x": 0.5,  # 标题水平位置
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20},  # 字体大小
        },
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=0.05,
            xanchor="right",
            x=0.95,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        )
    )

    return fig


@callback(
    Output("output", "children"),
    Input("insee_department", "data")
)
def up_date_txt(selected_dep):
    filtered_dep_df = pvd[pvd["Code Officiel Département"] == selected_dep]
    total_count = filtered_dep_df.shape[0]

    # 格式化数字并返回内容
    return html.Div(
        children=[
            html.Div("Nombre de PVD", style={
                "fontSize": "20px",  # 标题字体更大
                "fontWeight": "bold",
                "color": "#155724",
                "marginBottom": "10px"  # 增加标题与数字之间的间距
            }),
            html.Div(f"{total_count:,}", style={
                "fontSize": "40px",  # 数字字体更大
                "fontWeight": "bold",
                "color": "#155724",
                "textAlign": "center"
            })
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "justifyContent": "center",
            "height": "100%",  # 确保容器占满高度
            "width": "100%",  # 确保容器占满宽度
        }
    )


@callback(
    Output("timeline_gragh", "children"),
    Input("insee_department", "data")
)

def update_timeline(selected_insee):
    if not selected_insee:
        return html.Div(
            "Veuillez sélectionner un département.",
            style={
                "textAlign": "center",  # 水平居中
                "verticalAlign": "middle",  # 垂直居中
                "fontSize": "20px",  # 字体大小
                "fontWeight": "bold",  # 加粗
                "color": "#343a40",  # 字体颜色
                "height": "100%",  # 高度占满
                "display": "flex",  # 使用 Flexbox 布局
                "alignItems": "center",  # 垂直居中
                "justifyContent": "center",  # 水平居中
            },
        )

    # 筛选省份数据
    filtered_df = pvd[
        pvd["Code Officiel Département"] == selected_insee
        ]

    # 如果数据中没有 "year" 列，先从 "date_signature" 提取年份
    if "year" not in pvd.columns:
        pvd["year"] = pd.to_datetime(
            pvd["date_signature"]
        ).dt.year

    # 按年份统计增量
    project_count_by_year = (
        filtered_df.groupby("year")
            .size()
            .reindex(
            range(
                int(pvd["year"].min()),
                int(pvd["year"].max()) + 1,
            ),  # 确保时间范围完整
            fill_value=0,  # 没有数据的年份填充为 0
        )
    )

    # 计算累计总量
    cumulative_total = project_count_by_year.cumsum()

    # 构建折线图
    fig = go.Figure(
        data=go.Scatter(
            x=cumulative_total.index,
            y=cumulative_total.values,
            mode="lines+markers",
            name="Nombre total cumulé de projets PVD",
            line=dict(color="#17a2b8", width=2),
            marker=dict(color="#17a2b8", size=8),
        )
    )

    # 更新布局
    fig.update_layout(
        title={
            "text": "Nombre total cumulé de projets PVD",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 18, "color": "#343a40"},
        },
        xaxis_title="Année",
        yaxis_title="Nombre total de projets (cumulatif)",
        xaxis=dict(
            tickmode="linear",
            dtick=1,  # 每年显示一个刻度
            range=[
                int(pvd["year"].min()),
                int(pvd["year"].max()),
            ],  # 确保时间范围一致
            showgrid=True,
            gridcolor="rgba(200, 200, 200, 0.3)",
            linecolor="rgba(50, 50, 50, 0.5)",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(200, 200, 200, 0.3)",
            linecolor="rgba(50, 50, 50, 0.5)",
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        height=390,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8f9fa",
    )

    # 返回图表组件
    return dcc.Graph(figure=fig)


@callback(
    Output("Chart_gragh", "children"),
    Input("insee_department", "data")
)
def update_horizontal_bar_chart(selected_insee):
    # 数据统计
    pvd_count_by_dep = pvd.groupby(
        ["Code Officiel Département", "Nom Officiel Département"]).size().reset_index()
    pvd_count_by_dep.columns = ["Code Officiel Département", "Nom Officiel Département", "Nombre de PVD"]

    # 添加颜色列，标记选中项为红色，其余为蓝色
    pvd_count_by_dep["color"] = pvd_count_by_dep["Code Officiel Département"].apply(
        lambda dep: "red" if dep == selected_insee else "blue"
    )

    # 构建水平条形图，保持原始顺序
    fig = px.bar(
        pvd_count_by_dep,
        y="Nom Officiel Département",  # 使用部门名称作为 Y 轴
        x="Nombre de PVD",
        orientation="h",  # 水平条形
        title="Nombre de PVD par Département",
        labels={"Nom Officiel Département": "Département", "Nombre de PVD": "Nombre de PVD"},
        text_auto=True,
    )

    # 使用颜色列自定义颜色
    fig.update_traces(marker=dict(color=pvd_count_by_dep["color"]))

    # 更新布局
    fig.update_layout(
        xaxis_title="Nombre de PVD",
        yaxis_title="Département",

        margin=dict(l=20, r=20, t=50, b=20),
        height=2000,  # 增加高度以容纳更多条目
        paper_bgcolor="rgba(0, 0, 0, 0)",  # 设置纸张背景为透明
        plot_bgcolor="rgba(0, 0, 0, 0)",  # 设置绘图区域背景为透明
        showlegend=False,
    )

    # 添加 CSS 样式以支持滚动条
    graph_style = {
        "overflowY": "scroll",  # 垂直滚动条
        "height": "800px",  # 显示区域高度
    }

    return html.Div(dcc.Graph(figure=fig), style=graph_style)
