#https://en.wikipedia.org/wiki/Graph_property
#look to Example section

import matplotlib.pyplot as plt
from networkx import nx

G = nx.lollipop_graph(4, 6)

pathlengths = []

# Integer invariants
# Order, the number of vertices
# Size, the number of edges
# Number of connected components
# Circuit rank, a linear combination of the numbers of edges, vertices, and components
# diameter, the longest of the shortest path lengths between pairs of vertices
# girth, the length of the shortest cycle
# Vertex connectivity, the smallest number of vertices whose removal disconnects the graph
# Edge connectivity, the smallest number of edges whose removal disconnects the graph
# Chromatic number, the smallest number of colors for the vertices in a proper coloring
# Chromatic index, the smallest number of colors for the edges in a proper edge coloring
# Choosability (or list chromatic number), the least number k such that G is k-choosable
# Independence number, the largest size of an independent set of vertices
# Clique number, the largest order of a complete subgraph
# Arboricity
# Graph genus
# Pagenumber
# Hosoya index
# Wiener index
# Colin de Verdière graph invariant
# Boxicity

class Properties():
    def __init__(self, G):
        self.graph = G

    def Order(self):
        print(nx.nodes(self.graph))
        print(self.graph.order())
        print(self.graph.__len__())

    def Size(self):
        print(self.graph.size())
        print(self.graph.number_of_edges())

    def Conectivity(self):
        #https: // networkx.github.io / documentation / stable / reference / algorithms / component.html
        ...


if __name__ == '__main__':
    G = nx.lollipop_graph(4, 6)
    instance = Properties(G)
    instance.Size()