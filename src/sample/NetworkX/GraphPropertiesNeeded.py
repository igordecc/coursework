import matplotlib.pyplot as plt
from networkx import nx

#G = nx.lollipop_graph(4, 6)
nodes = 10
probability = 0.6
G = nx.fast_gnp_random_graph(nodes, p=1)

# All properties (look to Example section):
# https://en.wikipedia.org/wiki/Graph_property

# центральность
# https://networkx.github.io/documentation/stable/reference/algorithms/centrality.html
print(nx.degree_centrality(G))

# распределение узлов
# https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_degree_histogram.html
print(G.degree())

# коэффициент кластеризации
#https://networkx.github.io/documentation/stable/reference/algorithms/clustering.html
print(nx.average_clustering(G))

# средняя длинна между узлами
# https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.diameter.html
print(nx.diameter(G))


nx.draw(G, with_labels=True)
plt.show()