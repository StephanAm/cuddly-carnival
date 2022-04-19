from pyparsing import col
import yaml
import numpy
import networkx as nx
import matplotlib.pyplot as plt
from collections import Iterable

class Service(object):
    def __init__(self, name, url, dependencies, owner) -> None:
        self.name= name
        self.url = url
        self.dependencies = dependencies
        self.owner = owner
    @classmethod
    def fromDict(cls, source):
        return cls(**source)


def loadFromYaml(filename):
    with open(filename, "r") as stream:
        try:
            source = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            raise exc
    r = {}
    for key in source:
        r[key] = Service.fromDict(source[key])
    return r

def createServiceList(source):
    serviceList = list(source.keys())

    for service in source:
        for downstreamService in source[service].dependencies:
            if not downstreamService in serviceList: 
                serviceList.append(downstreamService)
    return serviceList


def createAdjacencyMatrix(source):
    matrix = []
    for serviceX in source:
        line = []
        for serviceY in source:
            if serviceY in source[serviceX].dependencies:
                line.append(1)
            else:
                line.append(0)
                
        matrix.append(line)
        # else:
        #     matrix.append([0]*len(serviceList))
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
    innerShell = [n.name if isinstance(n,Service) else n for n in innerShell]
    outerShell = list(G.nodes())
    for node in innerShell:
        if node in outerShell: outerShell.remove(node)
    pos = nx.shell_layout(G, [innerShell, outerShell])
    # pos = nx.bipartite_layout(G, innerShell)
    draw(G, pos, labelText = labelText, filename=filename)

def draw(G, pos, labelText = None, filename=None, color=None):
    if filename is None:
        node_size = 2000
        font_size = 8
        linewidths = 0.01
        width = 0.1
        arrowsize = 1
    else:
        node_size = 150
        font_size = 1.5
        linewidths = 0.01
        width = 0.3
        arrowsize = 2
    plt.cla()
    plt.clf()
    plt.axis('equal')

    nx.draw(G,pos=pos,node_size=node_size,node_shape='o',linewidths=linewidths, width=width, arrowsize=arrowsize, node_color=color)
    nx.draw_networkx_labels(G,pos,labelText,font_size=font_size)
    if filename is None:
        plt.show()        
        input()
    else:
        plt.savefig(fname=filename,dpi=1000,transparent=True,bbox_inches='tight',figsize=(8,8))

def getEdgesForNode(G,node):
    if isinstance(node, Service): node = node.name
    ei = list(G.in_edges(node, keys=True))
    eo = list(G.out_edges(node, keys=True))
    edges = ei+eo
    return edges


def getDescendants(G, nodes):
    if isinstance(nodes, str): nodes = nodes,
    if not isinstance(nodes,Iterable): nodes = nodes,

    a = set()
    for node in nodes:
        a = a.union(G.successors(node))
    
    b = a.difference(nodes)
    if len(b) == 0:
        return None
    
    c = getDescendants(G, b.union(nodes))
    if c is None:
        return [list(b)]
    else:
        return [list(b)]+c
    
def getAncestors(G, nodes):
    if isinstance(nodes, str): nodes = nodes,
    if not isinstance(nodes,Iterable): nodes = nodes,

    a = set()
    for node in nodes:
        a = a.union(G.predecessors(node))
    
    b = a.difference(nodes)
    if len(b) == 0:
        return None
    
    c = getAncestors(G, b.union(nodes))
    if c is None:
        return [list(b)]
    else:
        return c+[list(b)]

    
# def markDesc(G,node,generation=1):
#     s = G.successors(node)
#     nx.set_node_attributes(G,{
#         node: {
#             'gen':generation,
#             'type': 's'
#         }
#         })
#     for node in G.successors(node):


def drawDependencyTree(G, node, filename = None):
    if isinstance(node, Service): node = node.name
    d = getDescendants(G, node) 
    a = getAncestors(G, node)
    if d is None: d = []
    if a is None: a = []
    generations = a + [[node]] + d
    G2 = nx.DiGraph()

    
    for i, gen in enumerate(generations):
        G2.add_nodes_from(gen, x=str(i))
        
    for i in range(len(generations)-1):
        g1 = generations[i]
        g2 = generations[i+1]
        e1 = set(G.out_edges(g1))
        e2 = set(G.in_edges(g2))
        e = e2.intersection(e1)
        G2.add_edges_from(e)

    color = ['green' if i == node else '#1f78b4' for i in G2.nodes()]
    labelText = dict([(i, "\n".join(i.split('-'))) for i in G2.nodes()])
    nx.set_node_attributes(G2, {node: {'color':'green'}} )
    # nx.set_node_attributes(G2,sub,'subset')
    # pos = nx.spring_layout(G2)
    # pos = nx.kamada_kawai_layout(G2)
    pos = nx.multipartite_layout(G2, align='vertical', scale=1, subset_key='x')
    # pos = nx.shell_layout(G2,generations)
    draw(G2, pos, labelText = labelText, filename=filename, color= color)
    


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
    while len(serviceList) > batchSize:
        focus = serviceList[:batchSize]
        serviceList = serviceList[batchSize:]
        _drawSubGraphs(G,focus=focus, filename=f'{outputDir}/{count}.png')
        count += 1

    focus = serviceList
    _drawSubGraphs(G,focus=focus,filename=f'{outputDir}/{count}.png')
    