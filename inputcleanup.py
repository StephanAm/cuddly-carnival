from signal import raise_signal
import spider
import networkx as nx
import yaml

# source = spider.loadFromYaml('wip/source.yml')
# serviceList = spider.createServiceList(source)
# matrix = spider.createAdjacencyMatrix(source, serviceList)
# G = spider.createGraph(matrix, serviceList)

# # focus = source.keys()
# # spider.drawFocused(G, focus=focus)

# spider.drawSubGraphs(G,1,"wip/out/")

class Service(object):
    def __init__(self, name="", owner="", dependencies =None, url = None) -> None:
        self.dependencies = dependencies if dependencies is not None else []
        self.ownedBy = owner
        self.url = url
        self.name = name
    
    def asDict(self) -> dict:
        return{
            'name': self.name,
            'dependencies': self.dependencies,
            'url': self.url,
            'owner': self.ownedBy
        }


def checkDuplicateURL(services: dict, url):
    for service in services.values():
        if service.url == url:
            print(url)
            raise Exception("Duplicate URL")

services = {}
source = spider.loadFromYaml('wip/source.yml')
for toplevelService in source:
    service = Service(name=toplevelService,owner='DAS')
    services[service.name] = service

l = len(source)
for _i,toplevelService in enumerate(source):
    for sub in source[toplevelService]:
        i = sub.find(')')
        owner = sub[1:i]
        name = sub[i+1:]
        service = Service(name,owner,url=source[toplevelService][sub])
        if not service.name in services:
            checkDuplicateURL(services, service.url)
            services[service.name] = service
            
        services[toplevelService].dependencies.append(service.name)
        
for i in services:
    services[i] = services[i].asDict()

with open ('wip/out.yml','w') as f:
    yaml.dump(services, f)