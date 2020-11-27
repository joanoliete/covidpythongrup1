import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import random
from random import seed
import plotly.express as px
from dash.dash import no_update
import dash_bootstrap_components as dbc
import dash_html_components as html
import os
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.CYBORG])

def escampa(G, contagirate):
        for n in G.nodes:
            if G.nodes[n]['infectat']:
                # busquem els veins
                for v in G[n]:
                    if random.uniform(0,1) > 1-contagirate :
                        if G.nodes[v]['color']=="green":
                            break
                        else:
                            G.nodes[v]['infectat']=True
                            G.nodes[v]['color']="red"
        return (G)

def create_graph_plot(G):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
    # en realitat només caldria regenerar aquesta part. però caldria refer la funció, o fer una classe
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='none',
        marker=dict(
            color=list(nx.get_node_attributes(G,'color').values()),
            size=8,
            line_width=0))
    return (edge_trace,node_trace)

#Variables maximes
diesmax=15
contagiratemax=100
vacinespercentagemax=100
novacinespercentagemax=100
quarantinedpopulationmax=100
infecteddpopulationmax=100

#Variable boolean
tocat=False

#Generem aleatoriament el graph
global G 
G = nx.dual_barabasi_albert_graph(2000,2,1,0.1)
pos = nx.spring_layout(G, k=0.25, iterations=20)
nx.set_node_attributes(G,pos,'pos')

nx.set_node_attributes(G,"blue",'color')
nx.set_node_attributes(G,False,'infectat')
nx.set_node_attributes(G,False,'vacunat')
nx.set_node_attributes(G,True,'vacunable')

#Generem estats 
estats=[]
estats.append(nx.get_node_attributes(G,"color"))

nx.set_node_attributes(G,estats[0],"color")
fig = go.Figure(data=create_graph_plot(G))
fig.update_layout(plot_bgcolor='rgb(10,10,10)')

#Boxplot KPIs
kpicontagis=[]
kpicostvacuna=[]
kpicostcuarantena=[]
with open('kpis.txt','r') as fin:
    lines = fin.readlines()
    for line in lines:
        # do something
        text=line.split(',')
        kpicontagis.append(text[0])
        kpicostvacuna.append(text[1])
        kpicostcuarantena.append(text[2])

d={'kpicontagis': kpicontagis,'kpicostvacuna':kpicostvacuna, 'kpicostcuarantena':kpicostcuarantena }
np.random.seed(1234)
df = pd.DataFrame(data = np.random.random(size=(4,3)), columns = ['kpicontagis','kpicostvacuna','kpicostcuarantena'])
df.plot(kind='box')


alerts = html.Div(
    [
        dbc.Alert("This is a primary alert", color="primary"),
        dbc.Alert("This is a secondary alert", color="secondary"),
        dbc.Alert("This is a success alert! Well done!", color="success"),
        dbc.Alert("This is a warning alert... be careful...", color="warning"),
        dbc.Alert("This is a danger alert. Scary!", color="danger"),
        dbc.Alert("This is an info alert. Good to know!", color="info"),
        dbc.Alert("This is a light alert", color="light"),
        dbc.Alert("This is a dark alert", color="dark"),
    ]
)
app.layout = html.Div(children=[

    html.H1(children='Evolució covid, mapa interactiu',style={'text-align': 'center'},),
    dbc.Card(
    [
        dbc.CardBody(
            [
                html.P("Un cop entrades les dades i generat el gràfic, es podrà anar pasant de dies en el slider automàticament", className="card-text"),
                dcc.Graph(
                    id='xarxa',
                    figure=fig,
                    style={'color': '#FFFFFF'}
                )
            ]
        ),
    ],
     className='col-lg-12 text-center'
    ),
    
dbc.Row([
    dbc.Col(

        dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P("Decidex els valors que vulguis i mira com evoluciona la pandèmia", className="card-text"),
                    html.Div(children='''Day''',
                        style={'margin-top': '10px'}
                    ),
                    html.Div(
                        dcc.Slider(
                            id='dia-slider',
                            min=0,
                            max=diesmax,
                            value=0,
                            marks={str(i): str(i) for  i in range(0,diesmax)},
                            step=None,
                        )
                    ),
                
                
                    html.Div(children='''Contagium rate (%)'''),
                    html.Div(
                        dcc.Slider(
                            id='contagirate-slider',
                            min=0,
                            max=contagiratemax,
                            step=0.1,
                            value=0,
                        )
                    ),
                    html.Div(id='contagi-output-container',style={'margin-left': 'auto','margin-right': 'auto'}),
                    html.Div(children='''Percentage of vaccined population (%)'''),
                    html.Div(
                        dcc.Slider(
                            id='vacinespercentage-slider',
                            min=0,
                            max=vacinespercentagemax,
                            value=0,
                            step=1,
                        )
                    ), 
                    html.Div(id='vacines-output-container'),
                    html.Div(children='''Percentage of impracticable vaccination on population (%)'''),
                    html.Div(
                        dcc.Slider(
                            id='novacinespercentage-slider',
                            min=0,
                            max=novacinespercentagemax,
                            value=0,
                            step=1,
                        )
                    ),
                    html.Div(id='novacines-output-container'),
                
                    html.Div(children='''Percentage of population in quarantine (%)'''),
                    html.Div(
                        dcc.Slider(
                            id='quarantinedpopulation-slider',
                            min=0,
                            max=quarantinedpopulationmax,
                            value=0,
                            step=1,
                        )
                    ),
                    html.Div(id='quarantine-output-container'),
    
                    html.Div(children='''Percentage of infected (%)'''),
                    html.Div(
                        dcc.Slider(
                            id='infectedpopulation-slider',
                            min=0,
                            max=infecteddpopulationmax,
                            value=0,
                            step=0.5,
                        )
                    ),
                    html.Div(id='infected-output-container'),
                    html.Div(
                    dbc.Button('Generate graph', id='button', n_clicks=0),
                        style={'padding': '10px'}
                    )
                ]
            ),
        ],
        className='text-center',
        style={'margin-top':'24px'}
        ),
        width=6,
    ),

    dbc.Col(
        dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P("BOXPLOT GOES HERE", className="card-text")
                ]
            ),
        ],
        style={'margin-top':'24px'},
        className='text-center'
        ),
        width=6
    ),
]),   


    html.Div(id='container-button-basic'),

],
style={'padding': '50px'},
className='text-center')

# indiquem que el output d'aquest callback es la figure del component amb id xarxa
# # el callback te com a input un canvi en el dia--slider
@app.callback(dash.dependencies.Output('xarxa', 'figure'),dash.dependencies.Output('contagi-output-container', 'children'),
            dash.dependencies.Output('vacines-output-container', 'children'),dash.dependencies.Output('novacines-output-container', 'children'),
            dash.dependencies.Output('quarantine-output-container', 'children'),
            dash.dependencies.Output('infected-output-container', 'children'),
            [ dash.dependencies.Input('dia-slider', 'value'),
            dash.dependencies.Input('contagirate-slider', 'value'),
            dash.dependencies.Input('quarantinedpopulation-slider', 'value'),
            dash.dependencies.Input('novacinespercentage-slider', 'value'),
            dash.dependencies.Input('vacinespercentage-slider', 'value'),
            dash.dependencies.Input('infectedpopulation-slider', 'value'),
            dash.dependencies.Input('button', 'n_clicks'),
            ])
def update_graph(dia, contagirate, quarantine, novacines, vacines, infected, n_clicks):
        global estats
        global tocat 
        if tocat:
            nx.set_node_attributes(G,estats[dia],"color")
            fig = go.Figure(data=create_graph_plot(G))
            fig.update_layout(plot_bgcolor='rgb(10,10,10)')
            return fig, contagirate, vacines, novacines, quarantine, infected
        if n_clicks == 1 and tocat==False:
            tocat = True
            #Primer eliminar aletoriament els nodes que estan en quarentena del graph depenent del input del usuari (exemple input 33)
            seed(1)
            sequenceeliminate = random.sample(range(round(len(list(G.nodes)))), round(len(list(G.nodes))*quarantine/100))
            for x in sequenceeliminate:
                G.remove_node(x)

            #Aqui cambiar l'estat dels nodes per 'novacunable' aleatoriament depenen del % del input del usuari (exemple input 33)
            sequencenovaccinate = random.sample(list(G.nodes), round(len(list(G.nodes))*novacines/100))
            for x in sequencenovaccinate:
                G.nodes[x]['vacunable']=False
                G.nodes[x]['color']="green"

            #Depenenet del anterior posar aleatoriament els nodes l'estat 'vacunat' depenen del % del input
            sequencevaccinate = random.sample(list(G.nodes), round(len(list(G.nodes))*vacines/100))
            for x in sequencevaccinate:
                if G.nodes[x]['color']!="green":
                    G.nodes[x]['vacunat']=True
                    G.nodes[x]['color']="green"

            #Infected people
            sequenceinfected = random.sample(list(G.nodes), round(len(list(G.nodes))*infected/100))
            for x in sequenceinfected:
                if G.nodes[x]['color']!="green":
                    G.nodes[x]['color']="red"
                    G.nodes[x]['infectat']=True

            #Generem estats 
            for i in range(1,diesmax) :
                G1 = G
                G1 = escampa(G, contagirate)
                # poso a estats el color del node segons el dia 
                estats.append(nx.get_node_attributes(G,"color"))

            nx.set_node_attributes(G,estats[dia],"color")
            fig = go.Figure(data=create_graph_plot(G))
            fig.update_layout(plot_bgcolor='rgb(10,10,10)')
            #KPIs
            infectedtotal=0

            #nx.set_node_attributes(G,estats[14],"color")
            #for i in range(1, round(len(list(G.nodes)))):
            #    if G.nodes[i]['color']=='red':
            #        infected=infected+1

            file = open("kpis.txt", "a") 
            file.write(str(infected)+",")
            file.write(str(quarantine/100*2000*500)+",") #Cost de posar en quarentena 14 dies 500$
            file.write(str(vacines/100*2000*50)) #Cost de vacunar una persona 50$
                                          #Maxim infectat amb un dia
            file.write("\n")
            file.close() 

            # retornem la figura, que s'ha de substituir
            return fig, contagirate, vacines, novacines, quarantine, infected
        return no_update, contagirate, vacines, novacines, quarantine, infected

if __name__ == '__main__':
    app.run_server(debug=True)