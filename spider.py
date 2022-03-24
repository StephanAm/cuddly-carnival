import yaml
import numpy
import networkx as nx
import matplotlib.pyplot as plt
from collections import Iterable




def loadFromYaml(filename):
    with open(filename, "r") as stream:
        try:
            source = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            raise exc
    return source

def createServiceList(source):
    serviceList = list(source.keys())

    for service in source:
        for downstreamService in source[service]:
            if not downstreamService in serviceList: 
                serviceList.append(downstreamService)
    return serviceList


def createAdjacencyMatrix(source, serviceList):
    matrix = []
    for i,serviceX in enumerate(serviceList):
        line = []
        if serviceX in source:
            for serviceY in serviceList:
                if serviceY in source[serviceX]:
                    line.append(1)
                else:
                    line.append(0)
                
            matrix.append(line)
        else:
            matrix.append([0]*len(serviceList))
    matrix = numpy.matrix(matrix)
    return matrix

def createGraph(matrix, serviceList):
    G = nx.from_numpy_matrix(matrix, 
                            parallel_edges=True, 
                            create_using=nx.MultiDiGraph())

    lables = dict(enumerate(serviceList))
    G = nx.relabel_nodes(G, lables)
    return G

def drawFocused(G, focus, filename=None):
    labelText = dict([(i, "\n".join(i.split('-'))) for i in G.nodes()])
    innerShell = focus if isinstance(focus, Iterable) else [focus]
    outerShell = list(G.nodes())
    for node in focus:
        outerShell.remove(node)
    # pos = nx.shell_layout(G, [innerShell, outerShell])
    pos = nx.bipartite_layout(G, innerShell)
    draw(G, pos, labelText = labelText, filename=filename)

def draw(G, pos, labelText = None, filename=None):
    plt.cla()
    plt.clf()
    plt.axis('equal')
    nx.draw(G,pos=pos,node_size=200,node_shape='o')
    nx.draw_networkx_labels(G,pos,labelText,font_size=1)
    if filename is None:
        plt.show()        
        input()
    else:
        plt.savefig(fname=filename,dpi=2000,transparent=True,bbox_inches='tight',)

def getEdgesForNode(G,node):
    ei = list(G.in_edges(node, keys=True))
    eo = list(G.out_edges(node, keys=True))
    edges = ei+eo
    return edges

def getSubGraph(G, focus):
    if not isinstance(focus, Iterable): focus = (focus,)
    edges=[]
    for node in focus:
        edges += getEdgesForNode(G, node)
    return G.edge_subgraph(edges)


def _drawSubGraphs(G, focus, filename=None):
    try:
        Gs = getSubGraph(G,focus)

        drawFocused(Gs, focus, filename=filename)
    except Exception as x:
        print(f"couldn't process {focus}: {x}")


def drawSubGraphs(G, batchSize, outputDir = None):
    serviceList = list(G.nodes())
    count = 0
    while len(serviceList) > 10:
        focus = serviceList[:10]
        serviceList = serviceList[10:]
        _drawSubGraphs(G,focus=focus, filename=f'{outputDir}/{count}.png')
        count += 1

    focus = serviceList
    _drawSubGraphs(G,focus=focus,filename=f'{outputDir}/{count}.png')
    