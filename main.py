import spider
import networkx as nx

source = spider.loadFromYaml('wip/source.yml')
serviceList = spider.createServiceList(source)
matrix = spider.createAdjacencyMatrix(source, serviceList)
G = spider.createGraph(matrix, serviceList)

# focus = source.keys()
# spider.drawFocused(G, focus=focus)

spider.drawSubGraphs(G,1,"wip/out/")