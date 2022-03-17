import spider
import networkx as nx

source = spider.loadFromYaml('spider/source.yml')
serviceList = spider.createServiceList(source)
matrix = spider.createAdjacencyMatrix(source, serviceList)
G = spider.createGraph(matrix, serviceList)
labelText = dict([(i, "\n".join(i.split('-'))) for i in G.nodes()])


l = len(serviceList)
for i,service in enumerate(serviceList):
    print(f"{i}/{l}")
    try:
        
        focus = service
        Gs = spider.getSubGraph(G,focus)
        spider.drawFocused(Gs, focus,fileName=f"spider/{focus}.png")
    except:
        print(f"couldn't process {service}")

    # nodes = ['consent-api']+list(G.predecessors('consent-api'))+list(G.successors('consent-api'))
    # G2 = G.subgraph(nodes)


    

# G2.edges(data=True)


# pos = nx.shell_layout(G2, [innerShell, outerShell])
# pos = nx.circular_layout(G)

# nx.draw_circular(G2, with_labels=True)
# nx.draw_kamada_kawai(G2, with_labels=True)
# nx.draw_random(G2, with_labels=True)
# nx.draw_spring(G2, with_labels=True)
# nx.draw_shell(G2,[innerShell, outerShell] , node_size=1000, font_size=8, node_shape='o', with_labels=True)



# nx.draw
