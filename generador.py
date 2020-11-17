import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objects as go
from random import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,  external_stylesheets=external_stylesheets)

def escampa(G):
  for n in G.nodes:
    if G.nodes[n]['infectat']:
      # busquem els veins
      for v in G[n]:
        if random() > contagirate :
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


G= nx.dual_barabasi_albert_graph(2000,2,1,0.1)
pos = nx.spring_layout(G, k=0.25, iterations=20)
nx.set_node_attributes(G,pos,'pos')

nx.set_node_attributes(G,"blue",'color')
nx.set_node_attributes(G,False,'infectat')
G.nodes[300]['color']="red"
G.nodes[300]['infectat']=True

# taula amb les colors a posar en segons el dia
estats=[]
contagirate=0.95
diesmax=30
contagiratemax=100
vacinespercentagemax=100
novacinespercentagemax=100
quarantinedpopulationmax=100

# poso el dia 0
estats.append(nx.get_node_attributes(G,"color"))
for i in range(1,diesmax) :
  G=escampa(G)  
  # poso a estats el color del node segons el dia 
  estats.append(nx.get_node_attributes(G,"color"))



nx.set_node_attributes(G,estats[0],'color')
# Hi ha parts del create_graph_plot que no varien
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
])


@app.callback(
    dash.dependencies.Output('contagirate-slider', 'children'),
    [dash.dependencies.Input('contagirate-slider', 'value')])

def update_output(value):
    return 'Heu seleccionat una taxa de contagi de {}'.format(value)

def update_graph(value):
    nx.set_node_attributes(G,estats[value],'color')
    fig = go.Figure(data=create_graph_plot(G))
    # retornem la figura, que s'ha de substituir
    return fig


# indiquem que el output d'aquest callback es la figure del component amb id xarxa
# # el callback te com a input un canvi en el dia--slider
@app.callback(dash.dependencies.Output('xarxa', 'figure'),

            [ dash.dependencies.Input('dia-slider', 'value')
            ])

def update_graph(dia):
    nx.set_node_attributes(G,estats[dia],'color')
    fig = go.Figure(data=create_graph_plot(G))
    # retornem la figura, que s'ha de substituir
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)