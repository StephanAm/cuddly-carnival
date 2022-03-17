from fileinput import filename
import yaml
import numpy
import networkx as nx
import matplotlib.pyplot as plt


def loadFromYaml(filename):
    with open(filename, "r") as stream:
        try:
            source = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
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

def drawFocused(G, focus,fileName=None):
    innerShell = [focus]
    outerShell = list(G.nodes())
    outerShell.remove(focus)
    pos = nx.shell_layout(G, [innerShell, outerShell])
    draw(G, pos,fileName=fileName)

def draw(G, pos, labelText = None, fileName=None):
    plt.cla()
    plt.clf()
    plt.axis('equal')
    nx.draw(G,pos=pos,node_size=3000,node_shape='s')
    nx.draw_networkx_labels(G,pos,labelText,font_size=8)
    if fileName is None:
        plt.show()        
        input()
    else:
        plt.savefig(fname=fileName,dpi=200,transparent=True,bbox_inches='tight')

def getSubGraph(G, node):
    ei = list(G.in_edges(node, keys=True))
    eo = list(G.out_edges(node, keys=True))
    edges = ei+eo
    return G.edge_subgraph(edges)
