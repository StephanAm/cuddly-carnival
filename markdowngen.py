
import spider


ordinal = ['first', 'second', 'third','fourth','sixth','seventh']
def getOrdinal(i:int):
    if i < len(ordinal):
        return ordinal[i]
    else:
        return f'{i}th'

class BaseWriter(object):
    def output(self, text):
        print(text)

    def Hn(self, n:int, text:str):
        # self.output(f'h{n}. {text}')
        self.output(f'{"#"*n} {text}')

    def H1(self, text):self.Hn(1,text)    
    def H2(self, text):self.Hn(2,text)    
    def H3(self, text):self.Hn(3,text)    
    def H4(self, text):self.Hn(4,text)   

    def ul(self, text):
        self.output(f"* {text}")
    
    def ulAnchor(self, text):
        self.output(f"* [{text}](#{text})")
    
    def image(self, text, ext='png'):
        # self.output(f'!{text}.{ext}!')
        self.output(f'![{text}]({text}.{ext})')
    def close(self):
        pass

class DummyWriter(BaseWriter):
    def output(self, text):
        raise Exception('writer not initialized')

class FileWriter(BaseWriter):
    def __init__(self, stream) -> None:
        self.stream = stream
    def output(self, text):
        self.stream.write(text+"\n\n")
    def close(self):
        self.stream.close()

def generateDependants(w,G,node):
    a = spider.getAncestors(G, node)
    w.H3('Dependent services')
    if a is None:
        w.ul('None')
    else:
        a.reverse()
        for i,_a in enumerate(a):
            w.H4(ordinal[i] + ' order')
            for __a in _a:
                w.ulAnchor(__a)

def generateDependancies(w,G,node):
    a = spider.getDescendants(G, node)
    w.H3('Dependencies')
    if a is None:
        w.ul('None')
    else:
        for i,_a in enumerate(a):
            w.H4(ordinal[i] + ' order')
            for __a in _a:
                w.ulAnchor(__a)

def generateSection(w, G, node):
    w.H2(node)
    w.image(node)
    generateDependants(w, G, node)
    generateDependancies(w, G, node)



def generatePage(G, filename):
    with open(filename,'w') as f:
        w = FileWriter(f)
        w.H1('Services')
    
        for node in G.nodes:
            generateSection(w, G, node)
# markdown2pdf3.convert_markdown_to_pdf(filename)