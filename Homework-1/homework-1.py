#%% [markdown]
# # Homework -1

#%% 
#### BFS route finding
#%%
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(0, 20, 100)
plt.plot(x, np.sin(x))
plt.show() 

#%% [markdown]
# ## BFS Path Searching

#%%
# define nodes in graph
BEIJING, CHANGCHUN, MULUMUQI, WUHAN, GUNAGHZOU, SHENZHEN, BANGKOK, SHANGHAI, NEWYORK = "BEIJING CHANGCHUN MULUMUQI WUHAN GUANGZHOU SHENZHEN BANGKOK SHANGHAI NEWYORK".split()

#%%
# initialize connections
dictionary = {}
connection = {
    CHANGCHUN: [BEIJING],
    MULUMUQI: [BEIJING], 
    BEIJING: [MULUMUQI, CHANGCHUN, WUHAN, SHENZHEN, NEWYORK],
    NEWYORK: [BEIJING, SHANGHAI],
    SHANGHAI: [NEWYORK, WUHAN],
    WUHAN: [SHANGHAI, BEIJING, GUNAGHZOU],
    GUNAGHZOU: [WUHAN, BANGKOK],
    SHENZHEN: [WUHAN, BANGKOK],
    BANGKOK: [SHENZHEN, GUNAGHZOU]
}


#%%
import networkx as nx
graph = connection
g = nx.Graph(graph)
nx.draw(g, with_labels=True)

#%%``
def navigator(start, destination, graph):
    paths = [[start]]
    seen = set()

    while paths:
        path = paths.pop(0)
        frontier = path[-1]

        if frontier in seen: continue

        next_nodes = graph[frontier]

        for s in next_nodes:
            if s == destination:
                path.append(s)
                return path
            else:
                paths.append(path + [s])
        
        paths = sorted(paths, key=len)
        seen.add(frontier)
#%%
path = navigator(BEIJING, GUNAGHZOU, graph)
for i in path:
    print(i)


#%% [markdown]
#### 2. Sentence Generation
#%% 
grammer = '''
sentence => noun_phrase verb_phrase 
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的'''

def parsed_grammmer(grammer_str, sep):
    grammer = {}
    for line in grammer_str.split('\n'):
        line = line.strip()

        if not line: continue
        
        target, rules = line.split(sep)
        grammer[target.strip()] = [r.split() for r in rules.split('|')]
    return grammer
g = parsed_grammmer(grammer, '=>')
print(g)

def gene(grammer_parsed, target='sentence'):
    if target not in grammer_parsed:
        return target
    rule = random.choice(grammer_parsed[target])
    return ''.join(gene(grammer_parsed, target=r) for r in rule if r != 'null')

#%%
gene(g)

