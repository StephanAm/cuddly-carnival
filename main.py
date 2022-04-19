from signal import raise_signal
import spider
import markdowngen

source = spider.loadFromYaml('wip/out.yml')
# serviceList = spider.createServiceList(source)
matrix = spider.createAdjacencyMatrix(source)
G = spider.createGraph(matrix, source)
markdowngen.generatePage(G,'wip/out/service.md')
# G2 = spider.drawDependencyTree(G,'care-team-api','wip/out/test')
    

def drawdependencyTreesForAllService():
    l = len(source)
    for i,key in enumerate(source):
        print(f'{key} ({i}/{l})')
        service = source[key]
        # if service.owner != 'DAS':continue
        spider.drawDependencyTree(G,service,'wip/out/'+service.name)


# focus = filter(lambda x: x.owner == 'DAS',source.values())
# focus = map(lambda x: x.name, focus)
# focus = list(focus)
# # focus = source.keys()
# spider.drawFocused(G, focus=focus, filename='wip/out/DAScentric')
# spider.drawSubGraphs(G,1,"wip/out/")
