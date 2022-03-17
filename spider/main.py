# import imp
import matplotlib.pyplot as plt
import networkx as nx
import yaml
import numpy


with open("source.yml", "r") as stream:
    try:
        source = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


downstreamList = []

serviceList = list(source.keys())

for service in source:
    for downstreamService in source[service]:
        if not downstreamService in serviceList: 
            serviceList.append(downstreamService)

matrix = []
innerShell = []
outerShell = []
for i,serviceX in enumerate(serviceList):
    line = []
    if serviceX in source:
        innerShell.append(serviceX)
        for serviceY in serviceList:
            if serviceY in source[serviceX]:
                line.append(1)
            else:
                line.append(0)
        matrix.append(line)
    else:
        outerShell.append(serviceX)
        matrix.append([0]*len(serviceList))

matrix = numpy.matrix(matrix)
lables = dict(enumerate(serviceList))

G2 = nx.from_numpy_matrix(matrix, 
                            parallel_edges=True, 
                            create_using=nx.MultiDiGraph())
G2 = nx.relabel_nodes(G2, lables)
G2.edges(data=True)


# nx.draw_circular(G2, with_labels=True)
# nx.draw_kamada_kawai(G2, with_labels=True)
# nx.draw_random(G2, with_labels=True)
# nx.draw_spring(G2, with_labels=True)
nx.draw_shell(G2,[innerShell, outerShell] ,with_labels=True, node_size=5000, font_size=8, node_shape='8')
# nx.draw(G2,pos=layout(G2))
# plt.axis('equal')
plt.show()
input()
print("done")