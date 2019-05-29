import networkx
import networkx as nx
from matplotlib import pyplot

osc_number = 200
neighbours = 4
connectionProb = 0.04

a = networkx.watts_strogatz_graph(osc_number, neighbours, connectionProb)
centrality = nx.degree_centrality(a).values()
print("graph degree_centrality, max: ", max(centrality), " ; min: ", min(centrality))
print("graph degree_histogram: ", a.degree())
print("graph diameter: ",nx.diameter(a))
print("graph clustering coefficient: ", nx.average_clustering(a))
# networkx.draw(a)
# pyplot.show()

b = networkx.scale_free_graph(osc_number)
networkx.draw(b)
pyplot.show()
centrality = nx.degree_centrality(b).values()
print("graph degree_centrality, max: ", max(centrality), " ; min: ", min(centrality))
print("graph degree_histogram: ", b.degree())
print("graph diameter: ",nx.diameter(nx.to_undirected(b)))
print("graph clustering coefficient: ", nx.average_clustering(nx.to_undirected(b))) #### EROR
# print(networkx.to_numpy_array(b))

c = networkx.fast_gnp_random_graph(osc_number, connectionProb)
# networkx.draw(c)
# pyplot.show()
centrality = nx.degree_centrality(c).values()
print("graph degree_centrality, max: ", max(centrality), " ; min: ", min(centrality))
print("graph degree_histogram: ", c.degree())
print("graph diameter: ",nx.diameter(c))
print("graph clustering coefficient: ", nx.average_clustering(c))
# print(networkx.to_numpy_array(c))

d = networkx.fast_gnp_random_graph(osc_number, p=1)
# networkx.draw(d)
# pyplot.show()
centrality = nx.degree_centrality(d).values()
print("graph degree_centrality, max: ", max(centrality), " ; min: ", min(centrality))
print("graph degree_histogram: ", d.degree())
print("graph diameter: ",nx.diameter(d))
print("graph clustering coefficient: ", nx.average_clustering(d))
# print(networkx.to_numpy_array(d))
