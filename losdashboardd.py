import dash
from dash import dcc, html, dash_table, callback, Input, Output
import plotly.express as px
import pandas as pd
from pymongo import MongoClient
import dash_bootstrap_components as dbc

mongo_client = MongoClient('mongodb://localhost:27017/')
db_name = 'BddJornadas_MX2023'
mongo_db = mongo_client[db_name]
def mongodf(collection_name, numeric_cols=[]):
    collection = mongo_db[collection_name]
    data = list(collection.find())
    df = pd.DataFrame(data)
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)  # Llenar NaN con 0 antes de convertir a int
    df['_id'] = df['_id'].astype(str)  # Convertir '_id' a string
    return df
df_jornadas = mongodf('jornadas', ['JJ', 'JG', 'JE', 'JP', 'GF', 'GC', 'DG', 'PTS', 'Jornada'])
df_pg_jornada = mongodf('pg_jornada', ['PTS_Ganados', 'Jornada'])
df_progreso_por_jornada = mongodf('progreso_por_jornada', ['Jornada', 'Juegos Ganados'])
df_clasificacion_juego_limpio = mongodf('clasificacion_juego_limpio', ['Puntos', 'TarjetasAmarillas', 'TarjetasRojas'])
df_maximas_goleadoras = mongodf('maximas_goleadoras', ['Goles', 'Min.'])
df_sorted = df_jornadas.sort_values(by='PTS', ascending=False)
df_jornada_17 = df_jornadas[df_jornadas['Jornada'] == 17].sort_values(by='PTS', ascending=False)
df_jornada_17 = df_jornada_17.drop(columns=['_id', 'Posición', 'Jornada'])
df_main = df_jornadas.drop(columns=['_id', 'Posición'])
top_5_teams = df_sorted.drop_duplicates(subset=['Equipo']).head(5)

fig_goleadoras = px.bar(
    df_maximas_goleadoras,
    x="Jugadora",
    y="Goles",
    color="Club",
    title="Máximas Goleadoras",
    labels={"Jugadora": "Jugadora", "Goles": "Goles"}
)
fig_tarjetas_amarillas = px.bar(
    df_clasificacion_juego_limpio,
    x="Club",
    y="TarjetasAmarillas",
    title="Tarjetas Amarillas por Equipo",
    labels={"Club": "Club", "Yellow Cards": "Tarjetas Amarillas"}
)

df_clasificacion_juego_limpio['TarjetasRojas'] = df_clasificacion_juego_limpio['TarjetasRojas'].astype(int)
df_tarjetas_rojas = df_clasificacion_juego_limpio[df_clasificacion_juego_limpio["TarjetasRojas"] > 0]

fig_tarjetas_rojas = px.bar(
    df_tarjetas_rojas,
    x="Club",
    y="TarjetasRojas",
    title="Tarjetas Rojas por Equipo",
    labels={"Club": "Club", "Red Cards": "Tarjetas Rojas"}
)

bar_fig_jornada_17 = px.bar(df_jornada_17.head(5), x='Equipo', y='PTS', color='Equipo',
                            title="Puntos de los Top 5 Equipos en la Jornada 17")
progreso_juegos_ganados_fig = px.line(df_progreso_por_jornada, x='Jornada', y='Juegos Ganados', color='Equipo',
                                      title="Progreso de Juegos Ganados por Jornada")
pie_fig_jg = px.pie(top_5_teams, names='Equipo', values='JG', title="Juegos Ganados de los Top 5 Equipos")
pie_fig_jg.update_traces(textinfo='label+value', textfont_size=20)
eficiencia_juegos_ganados_fig = px.bar(df_jornadas, x='Equipo', y=['JG', 'JE', 'JP'], title="Eficiencia de Juegos Ganados, Empatados y Perdidos por Equipo",
labels={'value': 'Número de Juegos', 'variable': 'Resultado'}, color_discrete_map={'JG': 'green', 'JE': 'blue', 'JP': 'red'})
eficiencia_juegos_ganados_fig.update_layout(barmode='stack')
dropdown = dbc.DropdownMenu(
    label="Menu",
    menu_variant="dark",
    children=[
        dbc.DropdownMenuItem("Liga MX Dashboard", href="/"),
        dbc.DropdownMenuItem("Dashboard 2", href="/dashboard2"),
        dbc.DropdownMenuItem("Dashboard 3", href="/dashboard3"),
    ],
)
def liga_mx_dashboard():
    return html.Div([
        html.Div([
            html.Img(src='https://cloudfront-us-east-1.images.arcpublishing.com/infobae/D4TBI7QQEVGX5LEAUYB5L4OPSI.jpg',
                     style={'width': '100%', 'height': 'auto'}),
        ]),
        html.Div(style={'height': '20px'}),  # Espaciador
        html.Div([
            html.Div([
                html.Img(src='https://seeklogo.com/images/L/liga-bbva-mx-femenil-2019-logo-B7D6784AED-seeklogo.com.png',
                         style={'width': '150px'}),
                html.H2("Información", style={'color': 'white'}),
                html.P(
                    "La Liga MX Femenil Apertura 2023 ha sido una temporada memorable, destacada por la intensidad de los encuentros y el talento demostrado en cada jornada. Los equipos han competido ferozmente, ofreciendo un espectáculo lleno de emoción y calidad futbolística. Este torneo no solo ha consolidado la creciente popularidad del fútbol femenino en México, sino que también ha sido testigo de momentos históricos y actuaciones sobresalientes. Equipos como Tigres UANL y Monterrey han mostrado una vez más su dominio en la liga, mientras que otros como América y Chivas han sorprendido con su desempeño y estrategia en el campo. La final, llena de dramatismo y destreza, coronó a las campeonas de esta edición, reafirmando la importancia de la Liga MX Femenil en el desarrollo y visibilidad del fútbol femenino a nivel nacional e internacional."
                ),
                html.Img(
                    src='https://the18.com/sites/default/files/styles/x-large_square__4_3_/public/feature-images/20170720-The18-Image-Mexican-Women-League.jpg?itok=hbYzS0Qd',
                    style={'width': '100%', 'height': 'auto', 'marginTop': '20px'})
            ], style={'float': 'left', 'width': '55%', 'padding': '20px', 'backgroundColor': '#4b0082',
                      'borderRadius': '10px', 'color': 'white'}),
            html.Div([
                html.H2("Top 5 Equipos", style={'color': 'darkviolet'}),
                html.Div([
                    html.P(f"{i + 1}. {row['Equipo']} - {row['PTS']} puntos",
                           style={'margin': '5px', 'padding': '10px', 'backgroundColor': '#f0f8ff', 'borderRadius': '5px'})
                    for i, row in top_5_teams.iterrows()
                ]),
                html.Img(
                    src='https://cdn.forbes.com.mx/2021/06/2021-06-01T012803Z_1_MTZSPDEH6101ENBSCC_RTRFIPP_4_20210531201444-LMXF-G21-FV-UANL-GDL-ANTONIO-e1631299156537-640x360.jpg',
                    style={'width': '100%', 'height': 'auto', 'marginTop': '20px'})
            ], style={'float': 'right', 'width': '40%', 'padding': '20px', 'backgroundColor': '#e9ecef',
                      'borderRadius': '10px'}),
        ], style={'overflow': 'hidden'}),
        html.Div([
            html.H2("Tabla Completa de Todas las Jornadas", style={'color': 'darkviolet'}),
            dash_table.DataTable(
                id='complete-table',
                columns=[{"name": i, "id": i} for i in df_main.columns],
                data=df_main.to_dict('records'),
                page_size=18,  # Muestra 18 filas por página
                style_table={'height': '400px', 'overflowY': 'auto', 'backgroundColor': '#f8f9fa'},
                style_header={'backgroundColor': '#4b0082', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left', 'padding': '10px', 'backgroundColor': '#ffffff', 'color': '#000000'},
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f9f9f9'
                    }
                ]
            ),
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            html.H2("Equipo Ganador de Liga MX Femenil Apertura 2023: TIGRES", style={'color': 'darkviolet'}),
            html.Div([
                html.P("¡Felicidades a Tigres UANL por su victoria en el torneo!"),
                html.Img(
                    src='https://upload.wikimedia.org/wikipedia/en/thumb/0/00/UANL_Tigres_logo.svg/1200px-UANL_Tigres_logo.svg.png',
                    style={'width': '200px'}),
                html.Img(
                    src='https://images2.minutemediacdn.com/image/upload/c_fill,w_720,ar_16:9,f_auto,q_auto,g_auto/shape/cover/sport/Tigres-UANL-v-Chivas---Final-Torneo-Guard1anes-202-55d5e6261d6c15367cd5ff2092533c5c.jpg',
                    style={'width': '250px'}),
            ], style={'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            html.H2("Resumen y goles FINAL Liga Mx Femenil", style={'color': 'darkviolet'}),
            html.Iframe(
                src="https://www.youtube.com/embed/00hdjCXzYwo",
                style={"width": "100%", "height": "400px", "border": "none"}
            )
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            dcc.Graph(
                id='all-teams-graph',
                figure=px.bar(df_sorted, x='Equipo', y='PTS', color='Equipo', title="Puntos de Todos los Equipos")
            )
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            html.H2("Puntos de los Top 5 Equipos en la Jornada 17", style={'color': 'darkviolet'}),
            dcc.Graph(id='jornada-17-bar', figure=bar_fig_jornada_17),
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            html.H2("Tabla de Posiciones Finales", style={'color': 'darkviolet'}),
            dash_table.DataTable(
                id='final-standings-table',
                columns=[{"name": i, "id": i} for i in df_jornada_17.columns],
                data=df_jornada_17.to_dict('records'),
                page_size=18,  # Muestra 18 filas por página
                style_table={'height': '400px', 'overflowY': 'auto', 'backgroundColor': '#f8f9fa'},
                style_header={'backgroundColor': '#4b0082', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left', 'padding': '10px', 'backgroundColor': '#ffffff', 'color': '#000000'},
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f9f9f9'
                    }
                ]
            ),
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            html.H2("Video de Himno Oficial Liga BBVA Bancomer MX", style={'color': 'darkviolet'}),
            html.Iframe(
                src="https://www.youtube.com/embed/gjeMP5P63uc?autoplay=1&mute=1",
                width="560",
                height="315",
                title="YouTube video player",
                style={"border": "none"},
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            )
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Script("""
            document.addEventListener('DOMContentLoaded', function() {
                var iframe = document.querySelector('iframe');
                var src = iframe.src;
                iframe.src = src + "&autoplay=1";
            });
        """),
    ], style={'backgroundColor': '#d3d3d3', 'padding': '20px'})  # Cambiar color de fondo a gris
def dashboard_2():
    return html.Div([
        html.H2("Dashboard 2 - Gráficos de Juegos Ganados"),
        html.Div([
            dcc.Graph(id='progreso-por-jornada', figure=progreso_juegos_ganados_fig),
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            dcc.Graph(id='top5-jg-pie', figure=pie_fig_jg),
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            dcc.Graph(id='eficiencia-juegos-ganados', figure=eficiencia_juegos_ganados_fig),
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
    ])
def dashboard_3():
    return html.Div([
        html.H2("Dashboard 3 - Estadísticas de Juego Limpio y Goleadoras"),
        html.Div([
            dcc.Graph(id='bar-goleadoras', figure=fig_goleadoras),
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            dcc.Graph(id='bar-tarjetas-amarillas', figure=fig_tarjetas_amarillas),
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
        html.Div([
            dcc.Graph(id='bar-tarjetas-rojas', figure=fig_tarjetas_rojas),
        ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px'}),
    ])

def create_layout():
    return html.Div([
        dbc.NavbarSimple(
            children=[
                dropdown,
            ],
            brand="Liga MX Femenil Dashboards",
            brand_href="/",
            color="primary",
            dark=True,
        ),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
app.layout = create_layout()

@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return liga_mx_dashboard()
    elif pathname == '/dashboard2':
        return dashboard_2()
    elif pathname == '/dashboard3':
        return dashboard_3()
    else:
        return html.Div([html.H3('404 - Página no encontrada')])

if __name__ == '__main__':
    app.run_server(debug=True)
