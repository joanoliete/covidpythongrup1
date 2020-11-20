import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import random
from random import seed
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,  external_stylesheets=external_stylesheets)

def escampa(G, contagirate):
        for n in G.nodes:
            if G.nodes[n]['infectat']:
                # busquem els veins
                for v in G[n]:
                    if random.uniform(0,1) > 1-contagirate :
                        if G.nodes[v]['vacunat']==True:
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
contagirate=1
diesmax=15
contagiratemax=100
vacinespercentagemax=100
novacinespercentagemax=100
quarantinedpopulationmax=100

#Generem aleatoriament el graph
global G 
G = nx.dual_barabasi_albert_graph(2000,2,1,0.1)
pos = nx.spring_layout(G, k=0.25, iterations=20)
nx.set_node_attributes(G,pos,'pos')

nx.set_node_attributes(G,"blue",'color')
nx.set_node_attributes(G,False,'infectat')
nx.set_node_attributes(G,False,'vacunat')
nx.set_node_attributes(G,True,'vacunable')
G.nodes[300]['color']="red"
G.nodes[300]['infectat']=True

#Generem estats 
estats=[]
estats.append(nx.get_node_attributes(G,"color"))

nx.set_node_attributes(G,estats[0],"color")
fig = go.Figure(data=create_graph_plot(G))

app.layout = html.Div(children=[
    html.H1(children='Evolució covid'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
    id='xarxa',
    figure=fig
    ),
    html.Div(children='''
        Day
    '''),
    html.Div(
        dcc.Slider(
            id='dia-slider',
            min=0,
            max=diesmax,
            value=0,
            marks={str(i): str(i) for  i in range(0,diesmax)},
            step=None
            ), 
        style={'width': '49%', 'padding': '0px 20px 20px 20px'}),

    html.Div(children='''
        Contagium rate
    '''),
            html.Div(
        dcc.Slider(
            id='contagirate-slider',
            min=0,
            max=contagiratemax,
            step=0.05,
            value=0,
            ), 
        style={'width': '49%', 'padding': '0px 20px 20px 20px'}),

        html.Div(children='''
        Percentage of vaccined population
    '''),
            html.Div(
        dcc.Slider(
            id='vacinespercentage-slider',
            min=0,
            max=vacinespercentagemax,
            value=0,
            step=1
            ), 
        style={'width': '49%', 'padding': '0px 20px 20px 20px'})
       ,

        html.Div(children='''
        Percentage of impracticable vaccination on population
    '''),
            html.Div(
        dcc.Slider(
            id='novacinespercentage-slider',
            min=0,
            max=novacinespercentagemax,
            value=0,
            step=1
            ), 
        style={'width': '49%', 'padding': '0px 20px 20px 20px'}),

                html.Div(children='''
        Percentage of population in quarantine
    '''),
            html.Div(
        dcc.Slider(
            id='quarantinedpopulation-slider',
            min=0,
            max=quarantinedpopulationmax,
            value=0,
            step=1
            ), 
        style={'width': '49%', 'padding': '0px 20px 20px 20px'}),
    html.Button('Generate graph', id='button', n_clicks=0),
    html.Div(id='container-button-basic')
])

# indiquem que el output d'aquest callback es la figure del component amb id xarxa
# # el callback te com a input un canvi en el dia--slider
@app.callback(dash.dependencies.Output('xarxa', 'figure'), dash.dependencies.Output('container-button-basic', 'children'),
            [ dash.dependencies.Input('dia-slider', 'value'),
            dash.dependencies.Input('contagirate-slider', 'value'),
            dash.dependencies.Input('quarantinedpopulation-slider', 'value'),
            dash.dependencies.Input('novacinespercentage-slider', 'value'),
            dash.dependencies.Input('vacinespercentage-slider', 'value'),
            dash.dependencies.Input('button', 'n_clicks')
            ])
def update_graph(dia, contagirate, quarantine, novacines, vacines, n_clicks):
        if n_clicks > 0:
            #Primer eliminar aletoriament els nodes que estan en quarentena del graph depenent del input del usuari (exemple input 33)
            seed(1)
            sequenceeliminate = random.sample(range(round(len(list(G.nodes)))), round(len(list(G.nodes))*quarantine/100))
            for x in sequenceeliminate:
                G.remove_node(x)

            #Aqui cambiar l'estat dels nodes per 'novacunable' aleatoriament depenen del % del input del usuari (exemple input 33)
            sequencenovaccinate = random.sample(range(round(len(list(G.nodes)))), round(len(list(G.nodes))*novacines/100))
            for x in sequencenovaccinate:
                G.nodes[x]['vacunable']=False
                G.nodes[x]['color']="green"

            #Depenenet del anterior posar aleatoriament els nodes l'estat 'vacunat' depenen del % del input
            sequencevaccinate = random.sample(range(round(len(list(G.nodes)))), round(len(list(G.nodes))*vacines/100))
            for x in sequencevaccinate:
                if G.nodes[x]['color']!='green':
                    G.nodes[x]['vacunat']=True
                    G.nodes[x]['color']="green"

            #Generem estats 
            estats=[]
            for i in range(1,diesmax) :
                G1 = G
                G1 = escampa(G, contagirate)
                # poso a estats el color del node segons el dia 
                estats.append(nx.get_node_attributes(G,"color"))

            nx.set_node_attributes(G,estats[dia],"color")
            fig = go.Figure(data=create_graph_plot(G))
            # retornem la figura, que s'ha de substituir
            return fig, n_clicks
        return

if __name__ == '__main__':
    app.run_server(debug=True)