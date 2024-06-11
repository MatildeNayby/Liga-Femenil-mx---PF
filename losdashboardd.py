# dashboard.py
import dash
from dash import dcc, html, dash_table
import plotly.express as px
from losdataframe import df_jornada_17, df_progreso_por_jornada, df_pg_jornada, top_5_teams, df_main

# lospuntos por jornada (tabla en barras)
bar_fig_jornada_17 = px.bar(df_jornada_17.head(5), x='Equipo', y='PTS', color='Equipo',
                            title="Puntos de los Top 5 Equipos en la Jornada 17")

# grafica de lineas de Juegos ganados por jornada
progreso_juegos_ganados_fig = px.line(df_progreso_por_jornada, x='Jornada', y='Juegos Ganados', color='Equipo',
                                      title="Progreso de Juegos Ganados por Jornada")

# Puntos ganados por jornada
pg_jornada_fig = px.bar(df_pg_jornada, x='Jornada', y='PTS_Ganados', color='Id_Equipo',
                        title="Puntos Ganados por Jornada para cada Equipo")

# La gráfica de pastel de los Juegos Ganados de los TOP 5 EQUIPOS
pie_fig_jg = px.pie(top_5_teams, names='Equipo', values='JG', title="Juegos Ganados de los Top 5 Equipos")
pie_fig_jg.update_traces(textinfo='label+value', textfont_size=20)

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.Img(src='https://cloudfront-us-east-1.images.arcpublishing.com/infobae/D4TBI7QQEVGX5LEAUYB5L4OPSI.jpg',
                 style={'width': '100%', 'height': 'auto'}),
        # ESTA ES LA IMAGEN PRINCIPAL NO CAMBIAR
    ]),

    html.Div(style={'height': '20px'}),

    html.Div([
        html.Div([
            html.H2("Sobre La Apertura 2023", style={'color': 'white'}),
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
            style_table={'maxHeight': '400px', 'overflowY': 'scroll'},
        ),
    ], style={'padding': '20px', 'backgroundColor': '#e9ecef', 'borderRadius': '10px', 'marginTop': '20px'}),

    html.Div(style={'height': '20px'}),

    html.Div([
        html.Div([
            dcc.Graph(id='jornada-17-bar', figure=bar_fig_jornada_17),
        ], style={'width': '50%', 'float': 'left'}),

        html.Div([
            dcc.Graph(id='progreso-por-jornada', figure=progreso_juegos_ganados_fig),
        ], style={'width': '50%', 'float': 'right'}),
    ], style={'overflow': 'hidden'}),

    html.Div([
        dcc.Graph(id='pg-jornada', figure=pg_jornada_fig),
    ], style={'padding': '20px', 'backgroundColor': '#e9ecef', 'borderRadius': '10px', 'marginTop': '20px'}),

    html.Div([
        dcc.Graph(id='top5-jg-pie', figure=pie_fig_jg),
    ], style={'padding': '20px', 'backgroundColor': '#e9ecef', 'borderRadius': '10px', 'marginTop': '20px'}),

])

if __name__ == '__main__':
    app.run_server(debug=True)
